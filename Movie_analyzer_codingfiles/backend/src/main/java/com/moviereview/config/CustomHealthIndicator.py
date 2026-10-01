from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
import socket
import threading
import time

app = FastAPI(
    title="Movie Review API",
    version="1.0.0"
)

# Record application startup time
APP_START_TIME = time.time()


class AdminService:
    """
    Service responsible for controlling backend health status.
    Thread-safe implementation.
    """

    def __init__(self):
        self._backend_healthy = True
        self._lock = threading.Lock()

    def is_backend_healthy(self) -> bool:
        with self._lock:
            return self._backend_healthy

    def set_backend_health(self, healthy: bool):
        with self._lock:
            self._backend_healthy = healthy


# Singleton instance
admin_service = AdminService()


def get_admin_service():
    return admin_service


class CustomHealthIndicator:
    """
    Custom health indicator similar to Spring Boot HealthIndicator.
    """

    def __init__(self, admin_service: AdminService):
        self.admin_service = admin_service

    def check_health(self):
        uptime = round(time.time() - APP_START_TIME, 2)

        health_data = {
            "service": "backend",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "hostname": socket.gethostname(),
            "version": "1.0.0",
            "uptime_seconds": uptime
        }

        if not self.admin_service.is_backend_healthy():
            health_data.update({
                "status": "DOWN",
                "admin_status": "unhealthy",
                "reason": "Backend marked as unhealthy via admin toggle"
            })

            return JSONResponse(
                status_code=503,
                content=health_data
            )

        health_data.update({
            "status": "UP",
            "admin_status": "healthy",
            "message": "Backend is healthy"
        })

        return JSONResponse(
            status_code=200,
            content=health_data
        )


@app.get("/health")
def health(admin_service: AdminService = Depends(get_admin_service)):
    """
    Health endpoint similar to Spring Boot Actuator.
    """
    indicator = CustomHealthIndicator(admin_service)
    return indicator.check_health()


@app.post("/admin/health/{status}")
def update_health(
    status: str,
    admin_service: AdminService = Depends(get_admin_service)
):
    """
    Admin endpoint to toggle backend health.

    Example:
        POST /admin/health/up
        POST /admin/health/down
    """

    status = status.lower()

    if status == "up":
        admin_service.set_backend_health(True)
    elif status == "down":
        admin_service.set_backend_health(False)
    else:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Status must be 'up' or 'down'"
            }
        )

    return {
        "message": f"Backend health changed to {status.upper()}",
        "current_health": admin_service.is_backend_healthy()
    }