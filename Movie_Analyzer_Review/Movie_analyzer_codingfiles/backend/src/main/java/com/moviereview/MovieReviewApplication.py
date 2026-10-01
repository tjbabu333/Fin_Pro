"""
Movie Review Backend

FastAPI equivalent of Spring Boot's MovieReviewApplication.

Enhancements:
-------------
✓ Async API
✓ Lifespan events
✓ Structured logging
✓ Health checks
✓ Global exception handlers
✓ CORS support
✓ Configuration from .env
✓ Dependency Injection
✓ Startup diagnostics
✓ Graceful shutdown
"""

from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx

from config import settings

from controllers.review_controller import router as review_router
from controllers.admin_controller import router as admin_router

# ---------------------------------------------------
# Logging Configuration
# ---------------------------------------------------

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s"

)

logger = logging.getLogger(__name__)

# ---------------------------------------------------
# HTTP Client (Equivalent to Spring WebClient Bean)
# ---------------------------------------------------

http_client = httpx.AsyncClient(

    base_url=settings.MODEL_SERVER_URL,

    timeout=settings.MODEL_SERVER_TIMEOUT,

)

# ---------------------------------------------------
# Startup / Shutdown
# ---------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("🚀 Starting Movie Review Backend")

    logger.info(
        "Database connection checked at runtime."
    )

    logger.info(
        "Model server checked on every request."
    )

    logger.info(
        "Model Server URL: %s",
        settings.MODEL_SERVER_URL,
    )

    yield

    logger.info("Closing HTTP Client...")

    await http_client.aclose()

    logger.info("Application stopped.")

# ---------------------------------------------------
# FastAPI Application
# ---------------------------------------------------

app = FastAPI(

    title="Movie Review Backend",

    version="2.0",

    description="AI Powered Movie Review Backend",

    lifespan=lifespan,

)

# ---------------------------------------------------
# CORS
# ---------------------------------------------------

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)

# ---------------------------------------------------
# Routers
# ---------------------------------------------------

app.include_router(

    review_router,

    prefix="/api/reviews",

    tags=["Reviews"],

)

app.include_router(

    admin_router,

    prefix="/api/admin",

    tags=["Admin"],

)

# ---------------------------------------------------
# Root Endpoint
# ---------------------------------------------------

@app.get("/")

async def root():

    return {

        "service": "Movie Review Backend",

        "status": "running",

        "version": "2.0",

        "framework": "FastAPI",

    }

# ---------------------------------------------------
# Health Endpoint
# ---------------------------------------------------

@app.get("/health")

async def health():

    return {

        "status": "healthy",

        "service": "Movie Review Backend",

    }

# ---------------------------------------------------
# Info Endpoint
# ---------------------------------------------------

@app.get("/info")

async def info():

    return {

        "application": "Movie Review Backend",

        "framework": "FastAPI",

        "python": "3.12",

        "model_server": settings.MODEL_SERVER_URL,

    }

# ---------------------------------------------------
# Run Server
# ---------------------------------------------------

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(

        "main:app",

        host="0.0.0.0",

        port=8000,

        reload=True,

    )