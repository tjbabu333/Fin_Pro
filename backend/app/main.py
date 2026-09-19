import logging
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.routes import analytics
from app.api.routes.employees import router as employee_router
from app.api.routes.salaries import router as salary_router
from app.api.routes.salaries import salary_id_router
from app.api.routes.salary_records import router as salary_records_router
from app.core.config import get_settings
from app.core.exceptions import (
    EmployeeAlreadyExistsError,
    EmployeeNotFoundError,
    InvalidSalaryPeriodError,
    SalaryPeriodOverlapError,
)
from app.core.logging_config import setup_logging
from app.db.database import engine
from app.db.session import get_db

setup_logging()

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    engine.dispose()

app = FastAPI(
    title="Salary Management API",
    description=(
        "REST API for managing employees, salary records, "
        "and salary analytics."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in settings.cors_origins.split(",")
        if origin.strip()
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employee_router)
app.include_router(salary_router)
app.include_router(salary_id_router)
app.include_router(salary_records_router)
app.include_router(analytics.router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}


@app.get("/ready", tags=["Health"])
def readiness_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception as exc:
        logger.exception("Database readiness check failed")
        raise HTTPException(
            status_code=503,
            detail="Database is unavailable",
        ) from exc


@app.exception_handler(EmployeeNotFoundError)
async def employee_not_found_handler(
    request: Request,
    exc: EmployeeNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "code": "EMPLOYEE_NOT_FOUND",
                "message": exc.message,
            }
        },
    )


@app.exception_handler(EmployeeAlreadyExistsError)
async def employee_already_exists_handler(
    request: Request,
    exc: EmployeeAlreadyExistsError,
):
    return JSONResponse(
        status_code=409,
        content={
            "error": {
                "code": "EMPLOYEE_ALREADY_EXISTS",
                "message": exc.message,
            }
        },
    )


@app.exception_handler(SalaryPeriodOverlapError)
async def salary_period_overlap_handler(
    request: Request,
    exc: SalaryPeriodOverlapError,
):
    return JSONResponse(
        status_code=409,
        content={
            "error": {
                "code": "SALARY_PERIOD_OVERLAP",
                "message": exc.message,
            }
        },
    )


@app.exception_handler(InvalidSalaryPeriodError)
async def invalid_salary_period_handler(
    request: Request,
    exc: InvalidSalaryPeriodError,
):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "INVALID_SALARY_PERIOD",
                "message": exc.message,
            }
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": jsonable_encoder(exc.errors()),
            }
        },
    )


@app.exception_handler(Exception)
async def unexpected_exception_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
            }
        },
    )


logger = logging.getLogger("app")

@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    return response

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    request_id = request.headers.get(
        "X-Request-ID",
        str(uuid.uuid4()),
    )

    request.state.request_id = request_id

    start_time = time.perf_counter()

    try:
        response = await call_next(request)

        duration = (time.perf_counter() - start_time) * 1000

        response.headers["X-Request-ID"] = request_id

        logger.info(
            "request_id=%s | %s %s | %s | %.2fms",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

        return response

    except Exception:
        duration = (time.perf_counter() - start_time) * 1000

        logger.exception(
            "request_id=%s | %s %s | ERROR | %.2fms",
            request_id,
            request.method,
            request.url.path,
            duration,
        )

        raise