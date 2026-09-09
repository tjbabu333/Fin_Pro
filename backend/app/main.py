from fastapi import FastAPI, Request

from app.api.routes.employees import router as employee_router
from app.api.routes.salaries import router as salary_router

from app.api.routes.salary_records import router as salary_records_router

import logging
import time

from app.core.logging_config import setup_logging

setup_logging()

app = FastAPI(
    title="Salary Management API",
    version="1.0.0",
    description="Employee salary management system",
)

app.include_router(employee_router)
app.include_router(salary_router)
app.include_router(salary_records_router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    EmployeeNotFoundError,
    EmployeeAlreadyExistsError,
    SalaryPeriodOverlapError,
)

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
async def logging_middleware(request: Request, call_next):

    start_time = time.perf_counter()

    try:
        response = await call_next(request)

        duration = (time.perf_counter() - start_time) * 1000

        logger.info(
            "%s %s | %s | %.2fms",
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

        return response

    except Exception:
        duration = (time.perf_counter() - start_time) * 1000

        logger.exception(
            "%s %s | ERROR | %.2fms",
            request.method,
            request.url.path,
            duration,
        )

        raise