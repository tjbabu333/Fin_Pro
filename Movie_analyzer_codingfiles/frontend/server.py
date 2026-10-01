"""
=========================================================
Movie Review Platform
Frontend Server (FastAPI)
Part 1 - Initialization & Configuration

Equivalent to:
- Express Server
- Middleware
- Security
- Configuration
=========================================================
"""

import os
import sys
import time
import signal
import logging
import asyncio
import threading
import traceback
from pathlib import Path
from datetime import datetime
from typing import Optional

import psutil
import uvicorn
import httpx

from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    BackgroundTasks
)

from fastapi.responses import (
    JSONResponse,
    FileResponse,
    HTMLResponse
)

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware

# =========================================================
# Environment Variables
# =========================================================

PORT = int(os.getenv("PORT", 3000))

BACKEND_URL = os.getenv(
    "BACKEND_API_URL",
    "http://localhost:8080"
)

STATIC_DIR = Path("build")

REQUEST_TIMEOUT = 30

MAX_BODY_SIZE = 10 * 1024  # 10 KB


# =========================================================
# Logging
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("FrontendServer")


logger.info("🚀 Starting Movie Review Frontend")
logger.info(f"Backend URL : {BACKEND_URL}")
logger.info(f"Frontend Port : {PORT}")


# =========================================================
# FastAPI Application
# =========================================================

app = FastAPI(

    title="Movie Review Frontend",

    version="2.0.0",

    description="""
Production Ready Frontend Server

Features
---------
✔ Reverse Proxy
✔ Health Monitoring
✔ Admin APIs
✔ Static File Hosting
✔ Security
✔ Logging
✔ Graceful Shutdown
"""
)


# =========================================================
# Server State
# =========================================================

server_healthy = True

server_overloaded = False

overload_thread: Optional[threading.Thread] = None

shutdown_event = threading.Event()


# =========================================================
# Security Middleware
# =========================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)

app.add_middleware(

    GZipMiddleware,

    minimum_size=1024
)


# =========================================================
# Security Headers Middleware
# =========================================================

class SecurityHeadersMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        response = await call_next(request)

        response.headers["X-Frame-Options"] = "DENY"

        response.headers["X-Content-Type-Options"] = "nosniff"

        response.headers["X-XSS-Protection"] = "1; mode=block"

        response.headers["Referrer-Policy"] = "strict-origin"

        response.headers["Permissions-Policy"] = "geolocation=()"

        return response


app.add_middleware(SecurityHeadersMiddleware)


# =========================================================
# Request Size Limiter
# =========================================================

@app.middleware("http")
async def request_size_limit(request: Request, call_next):

    content_length = request.headers.get("content-length")

    if content_length:

        if int(content_length) > MAX_BODY_SIZE:

            return JSONResponse(

                status_code=413,

                content={

                    "error": "Payload Too Large"

                }

            )

    return await call_next(request)


# =========================================================
# Request Logger
# =========================================================

@app.middleware("http")
async def log_requests(request: Request, call_next):

    start = time.time()

    response = await call_next(request)

    duration = time.time() - start

    logger.info(

        "%s %s -> %s (%.2f ms)",

        request.method,

        request.url.path,

        response.status_code,

        duration * 1000

    )

    return response


# =========================================================
# Global Exception Handler
# =========================================================

@app.exception_handler(Exception)

async def global_exception_handler(request, exc):

    logger.error(traceback.format_exc())

    return JSONResponse(

        status_code=500,

        content={

            "error": "Internal Server Error",

            "message": str(exc),

            "timestamp": datetime.utcnow().isoformat()

        }

    )


# =========================================================
# Utility Functions
# =========================================================

def current_timestamp():

    return datetime.utcnow().isoformat()


def system_memory():

    memory = psutil.virtual_memory()

    return {

        "total": memory.total,

        "used": memory.used,

        "percent": memory.percent

    }


def cpu_usage():

    return psutil.cpu_percent(interval=0.2)

# =========================================================
# Health Check Endpoint
# =========================================================

@app.get("/health")
async def health_check():
    """
    Kubernetes health endpoint.
    """

    if not server_healthy:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "timestamp": current_timestamp(),
                "service": "frontend"
            }
        )

    return {
        "status": (
            "degraded"
            if server_overloaded
            else "healthy"
        ),
        "timestamp": current_timestamp(),
        "service": "frontend",
        "overloaded": server_overloaded
    }


# =========================================================
# Admin Status Endpoint
# =========================================================

@app.get("/admin/status")
async def admin_status():
    """
    Return complete frontend status.
    """

    process = psutil.Process()

    return {
        "healthy": server_healthy,
        "overloaded": server_overloaded,
        "timestamp": current_timestamp(),
        "uptime": time.time() - process.create_time(),
        "memory": system_memory(),
        "cpu_percent": cpu_usage(),
        "threads": process.num_threads(),
        "pid": process.pid
    }


# =========================================================
# Toggle Health
# =========================================================

@app.post("/admin/toggle-health")
async def toggle_health():

    global server_healthy

    server_healthy = not server_healthy

    logger.warning(
        "Frontend health changed -> %s",
        server_healthy
    )

    return {
        "message":
            f"Frontend health "
            f"{'enabled' if server_healthy else 'disabled'}",

        "healthy": server_healthy,

        "timestamp": current_timestamp()
    }


# =========================================================
# Crash Endpoint
# =========================================================

@app.post("/admin/crash")
async def crash_server(background_tasks: BackgroundTasks):
    """
    Simulate container crash.
    """

    logger.error(
        "Frontend crash requested."
    )

    background_tasks.add_task(delayed_crash)

    return {
        "message":
            "Frontend crash initiated",

        "countdown": 3,

        "timestamp": current_timestamp()
    }


def delayed_crash():

    logger.error("Crash in 3 seconds...")

    for i in range(3, 0, -1):

        logger.error(
            "Crash in %s second(s)...",
            i
        )

        time.sleep(1)

    logger.error(
        "Forcefully exiting process."
    )

    os._exit(1)


# =========================================================
# Overload Worker
# =========================================================

def overload_worker():
    """
    CPU + Memory overload simulation.
    """

    global server_overloaded

    logger.warning(
        "Overload worker started."
    )

    memory_chunks = []

    while (
        server_overloaded
        and
        not shutdown_event.is_set()
    ):

        # -----------------------------
        # CPU Intensive Calculation
        # -----------------------------

        start = time.time()

        while time.time() - start < 0.5:

            x = 0

            for i in range(50000):
                x += (
                    i ** 0.5
                ) * (
                    i % 11
                )

        # -----------------------------
        # Memory Pressure
        # -----------------------------

        memory_chunks.append(
            bytearray(1024 * 1024)
        )

        if len(memory_chunks) > 40:
            memory_chunks.pop(0)

        time.sleep(0.1)

    logger.info(
        "Overload worker stopped."
    )


# =========================================================
# Start Overload
# =========================================================

@app.post("/admin/start-overload")
async def start_overload():

    global server_overloaded
    global overload_thread

    if server_overloaded:

        return {
            "message":
                "Overload already running",

            "overloaded": True
        }

    server_overloaded = True

    overload_thread = threading.Thread(

        target=overload_worker,

        daemon=True

    )

    overload_thread.start()

    logger.warning(
        "Frontend overload started."
    )

    return {

        "message":
            "Frontend overload simulation started",

        "overloaded": True,

        "timestamp": current_timestamp()

    }


# =========================================================
# Stop Overload
# =========================================================

@app.post("/admin/stop-overload")
async def stop_overload():

    global server_overloaded

    if not server_overloaded:

        return {

            "message":
                "No overload is running",

            "overloaded": False

        }

    server_overloaded = False

    logger.info(
        "Frontend overload stopped."
    )

    return {

        "message":
            "Frontend overload stopped",

        "overloaded": False,

        "timestamp": current_timestamp()

    }


# =========================================================
# Ping Endpoint
# =========================================================

@app.get("/ping")
async def ping():
    """
    Simple ping endpoint.
    """

    return {
        "message": "pong",
        "timestamp": current_timestamp()
    }


# =========================================================
# Metrics Endpoint
# =========================================================

@app.get("/metrics")
async def metrics():
    """
    Lightweight runtime metrics.
    """

    process = psutil.Process()

    return {

        "cpu": cpu_usage(),

        "memory": system_memory(),

        "threads": process.num_threads(),

        "handles": getattr(
            process,
            "num_handles",
            lambda: None
        )(),

        "timestamp": current_timestamp()

    }

"""
routes/frontend.py

Frontend routes and application startup.
Enhanced FastAPI version of the Express frontend server.
"""

from pathlib import Path
import signal
import sys
import time
import psutil

from fastapi import APIRouter
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from core.config import settings
from core.state import server_state
from core.logger import logger

router = APIRouter(tags=["Frontend"])

# --------------------------------------------------
# Static Files
# --------------------------------------------------

BUILD_DIR = Path(settings.BUILD_DIR)

if BUILD_DIR.exists():
    router.mount(
        "/static",
        StaticFiles(directory=BUILD_DIR),
        name="static"
    )

# --------------------------------------------------
# React Single Page Application
# --------------------------------------------------

@router.get("/{full_path:path}")
async def react_app(full_path: str):
    """
    Serve React application.

    Every unknown route returns index.html
    allowing React Router to work.
    """

    requested = BUILD_DIR / full_path

    if requested.exists() and requested.is_file():
        return FileResponse(requested)

    index = BUILD_DIR / "index.html"

    if index.exists():
        return FileResponse(index)

    return {
        "message": "React build folder not found.",
        "expected": str(index)
    }


# --------------------------------------------------
# Startup Logging
# --------------------------------------------------

def startup_logs():

    logger.info("=" * 60)
    logger.info("🎬 Movie Review Frontend Started")
    logger.info("=" * 60)

    logger.info(f"Host      : {settings.HOST}")
    logger.info(f"Port      : {settings.PORT}")
    logger.info(f"Backend   : {settings.BACKEND_URL}")
    logger.info(f"Build Dir : {BUILD_DIR}")

    logger.info("=" * 60)


# --------------------------------------------------
# Runtime Statistics
# --------------------------------------------------

def runtime_stats():

    process = psutil.Process()

    return {
        "pid": process.pid,
        "cpu_percent": process.cpu_percent(),
        "memory_mb": round(
            process.memory_info().rss / 1024 / 1024,
            2
        ),
        "threads": process.num_threads(),
        "uptime_seconds": round(
            time.time() - server_state.started_at,
            2
        )
    }


# --------------------------------------------------
# Graceful Shutdown
# --------------------------------------------------

def shutdown_handler(signum, frame):

    logger.warning("=" * 60)
    logger.warning("Stopping Frontend Server...")
    logger.warning("=" * 60)

    server_state.stop_overload()

    logger.info("Server shutdown completed.")

    sys.exit(0)


signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

"""
core/logger.py

Enhanced logging system for the Movie Review Frontend.

Features
--------
✔ Colored console logs
✔ Rotating log files
✔ Separate error log
✔ Timestamped messages
✔ Debug / Info / Warning / Error helpers
✔ Production-ready formatting
"""

from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
import sys

# -------------------------------------------------
# Configuration
# -------------------------------------------------

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "frontend.log"
ERROR_FILE = LOG_DIR / "frontend_errors.log"

# -------------------------------------------------
# ANSI Colors
# -------------------------------------------------

class Colors:
    RESET = "\033[0m"

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"

# -------------------------------------------------
# Colored Formatter
# -------------------------------------------------

class ColoredFormatter(logging.Formatter):

    COLORS = {
        logging.DEBUG: Colors.CYAN,
        logging.INFO: Colors.GREEN,
        logging.WARNING: Colors.YELLOW,
        logging.ERROR: Colors.RED,
        logging.CRITICAL: Colors.RED,
    }

    def format(self, record):

        color = self.COLORS.get(record.levelno, Colors.RESET)

        message = super().format(record)

        return f"{color}{message}{Colors.RESET}"

# -------------------------------------------------
# Logger
# -------------------------------------------------

logger = logging.getLogger("MovieReviewFrontend")

logger.setLevel(logging.INFO)

# -------------------------------------------------
# Console Handler
# -------------------------------------------------

console = logging.StreamHandler(sys.stdout)

console.setFormatter(
    ColoredFormatter(
        "[%(asctime)s] %(levelname)s | %(message)s",
        "%H:%M:%S",
    )
)

# -------------------------------------------------
# File Handler
# -------------------------------------------------

file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
)

file_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s"
    )
)

# -------------------------------------------------
# Error File
# -------------------------------------------------

error_handler = RotatingFileHandler(
    ERROR_FILE,
    maxBytes=2 * 1024 * 1024,
    backupCount=3,
)

error_handler.setLevel(logging.ERROR)

error_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s"
    )
)

# -------------------------------------------------
# Register Handlers
# -------------------------------------------------

logger.addHandler(console)
logger.addHandler(file_handler)
logger.addHandler(error_handler)

# -------------------------------------------------
# Helper Functions
# -------------------------------------------------

def startup():
    logger.info("=" * 60)
    logger.info("🎬 Movie Review Frontend Started")
    logger.info("=" * 60)


def shutdown():
    logger.info("=" * 60)
    logger.info("🛑 Frontend Shutdown")
    logger.info("=" * 60)


def proxy(method: str, path: str):
    logger.info(f"🔄 Proxy {method} {path}")


def success(message: str):
    logger.info(f"✅ {message}")


def warning(message: str):
    logger.warning(f"⚠️ {message}")


def error(message: str):
    logger.error(f"❌ {message}")


def crash(message: str):
    logger.critical(f"💥 {message}")


def overload(message: str):
    logger.warning(f"🔥 {message}")

# ============================================================
# Movie Review Frontend
# Production Requirements
# ============================================================

# -----------------------------
# FastAPI Framework
# -----------------------------
fastapi>=0.116.0
uvicorn[standard]>=0.35.0

# -----------------------------
# HTTP Client
# -----------------------------
httpx>=0.28.0
aiohttp>=3.12.0

# -----------------------------
# Data Validation
# -----------------------------
pydantic>=2.11.0
pydantic-settings>=2.10.0

# -----------------------------
# Environment Variables
# -----------------------------
python-dotenv>=1.1.0

# -----------------------------
# Security
# -----------------------------
python-multipart>=0.0.20
itsdangerous>=2.2.0

# -----------------------------
# Performance
# -----------------------------
orjson>=3.11.0
uvloop>=0.21.0
httptools>=0.6.4

# -----------------------------
# Logging
# -----------------------------
colorlog>=6.9.0

# -----------------------------
# Monitoring
# -----------------------------
psutil>=7.0.0

# -----------------------------
# Async Utilities
# -----------------------------
anyio>=4.9.0

# -----------------------------
# Testing
# -----------------------------
pytest>=8.4.0
pytest-asyncio>=1.1.0

# -----------------------------
# Development
# -----------------------------
watchfiles>=1.1.0
rich>=14.1.0

# -----------------------------
# Optional Production Server
# -----------------------------
gunicorn>=23.0.0
