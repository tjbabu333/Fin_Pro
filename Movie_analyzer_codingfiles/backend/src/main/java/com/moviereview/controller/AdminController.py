from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
import socket
import platform
import time
import logging
import psutil

from admin_service import AdminService, get_admin_service

logger = logging.getLogger("admin")

router = APIRouter(
    prefix="/api/admin",
    tags=["Admin"]
)

APP_START_TIME = time.time()


# ---------------------------------------------------
# Health Check
# ---------------------------------------------------

@router.get("/health")
async def get_health(
    admin_service: AdminService = Depends(get_admin_service)
):
    """
    Backend health endpoint.
    """

    health = admin_service.get_health_status()

    logger.info("Health check requested")

    if health["status"] == "unhealthy":
        return JSONResponse(
            status_code=503,
            content=health
        )

    return health


# ---------------------------------------------------
# Toggle Backend Health
# ---------------------------------------------------

@router.post("/toggle-health")
async def toggle_health(
    admin_service: AdminService = Depends(get_admin_service)
):
    """
    Toggle backend health.
    """

    try:
        return admin_service.toggle_backend_health()

    except Exception as ex:
        logger.exception(ex)

        raise HTTPException(
            status_code=500,
            detail="Failed to toggle backend health"
        )


# ---------------------------------------------------
# Toggle Overload
# ---------------------------------------------------

@router.post("/toggle-overload")
async def toggle_overload(
    admin_service: AdminService = Depends(get_admin_service)
):
    try:
        return admin_service.toggle_backend_overload()

    except Exception as ex:
        logger.exception(ex)

        raise HTTPException(
            status_code=500,
            detail="Failed to toggle backend overload"
        )


# ---------------------------------------------------
# Toggle Database
# ---------------------------------------------------

@router.post("/toggle-database")
async def toggle_database(
    admin_service: AdminService = Depends(get_admin_service)
):
    try:
        return admin_service.toggle_database_connection()

    except Exception as ex:
        logger.exception(ex)

        raise HTTPException(
            status_code=500,
            detail="Failed to toggle database connection"
        )


# ---------------------------------------------------
# Toggle Model Server
# ---------------------------------------------------

@router.post("/toggle-model")
async def toggle_model(
    admin_service: AdminService = Depends(get_admin_service)
):
    try:
        return admin_service.toggle_model_server_connection()

    except Exception as ex:
        logger.exception(ex)

        raise HTTPException(
            status_code=500,
            detail="Failed to toggle model server connection"
        )


# ---------------------------------------------------
# Admin Status
# ---------------------------------------------------

@router.get("/status")
async def admin_status(
    admin_service: AdminService = Depends(get_admin_service)
):
    """
    Returns complete backend status.
    """

    try:
        return admin_service.get_admin_status()

    except Exception as ex:
        logger.exception(ex)

        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve admin status"
        )


# ---------------------------------------------------
# System Information
# ---------------------------------------------------

@router.get("/info")
async def system_info(
    admin_service: AdminService = Depends(get_admin_service)
):
    """
    Returns system metrics.
    """

    try:

        memory = psutil.virtual_memory()

        disk = psutil.disk_usage("/")

        cpu = psutil.cpu_percent(interval=0.5)

        uptime = round(time.time() - APP_START_TIME, 2)

        return {

            "service": "backend",

            "version": "2.0.0",

            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),

            "hostname": socket.gethostname(),

            "platform": platform.platform(),

            "python_version": platform.python_version(),

            "uptime_seconds": uptime,

            "cpu": {

                "usage_percent": cpu,

                "cores": psutil.cpu_count(logical=True)

            },

            "memory": {

                "total": memory.total,

                "used": memory.used,

                "available": memory.available,

                "usage_percent": memory.percent

            },

            "disk": {

                "total": disk.total,

                "used": disk.used,

                "free": disk.free,

                "usage_percent": disk.percent

            },

            "backend": {

                "healthy": admin_service.is_backend_healthy(),

                "overloaded": admin_service.is_backend_overloaded(),

                "database_connected":
                    admin_service.is_database_connected(),

                "model_connected":
                    admin_service.is_model_server_connected()

            }

        }

    except Exception as ex:

        logger.exception(ex)

        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve system information"
        )