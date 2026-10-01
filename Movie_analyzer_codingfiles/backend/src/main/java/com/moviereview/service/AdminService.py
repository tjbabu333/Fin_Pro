from __future__ import annotations

import gc
import logging
import math
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import Any, Dict, List

from services.review_service import ReviewService
from services.model_server_service import ModelServerService

logger = logging.getLogger(__name__)


class AdminService:
    """
    Admin service responsible for:

    - Backend health
    - Backend overload simulation
    - Database simulation
    - Model server simulation
    """

    def __init__(
        self,
        review_service: ReviewService,
        model_service: ModelServerService,
    ):

        self.review_service = review_service
        self.model_service = model_service

        self.backend_healthy = True
        self.backend_overloaded = False

        self.executor: ThreadPoolExecutor | None = None
        self.tasks = []

        self.lock = threading.Lock()

    # --------------------------------------------------------
    # Health Status
    # --------------------------------------------------------

    def get_health_status(self) -> Dict[str, Any]:

        db = self.review_service.is_database_available()

        model = self.model_service.is_model_server_available()

        if not self.backend_healthy:

            status = "unhealthy"

        elif db and model:

            status = "healthy"

        else:

            status = "degraded"

        return {

            "status": status,

            "service": "backend",

            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),

            "database": db,

            "modelServer": model,

            "backendHealthy": self.backend_healthy,

            "backendOverloaded": self.backend_overloaded,
        }

    # --------------------------------------------------------
    # Backend Health
    # --------------------------------------------------------

    def toggle_backend_health(self):

        with self.lock:

            self.backend_healthy = (
                not self.backend_healthy
            )

        logger.info(
            "Backend Health = %s",
            self.backend_healthy,
        )

        return {

            "message": (
                "Backend Enabled"
                if self.backend_healthy
                else "Backend Disabled"
            ),

            "healthy": self.backend_healthy,

            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
        }

    # --------------------------------------------------------
    # Overload Toggle
    # --------------------------------------------------------

    def toggle_backend_overload(self):

        if self.backend_overloaded:

            self.stop_backend_overload()

        else:

            self.start_backend_overload()

        return {

            "overloaded": self.backend_overloaded,

            "message": (
                "Overload Started"
                if self.backend_overloaded
                else "Overload Stopped"
            ),

            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
        }

    # --------------------------------------------------------
    # CPU Worker
    # --------------------------------------------------------

    def cpu_worker(self):

        while self.backend_overloaded:

            value = 0

            for i in range(200000):

                value += (
                    math.sqrt(i)
                    * math.sin(i)
                )

    # --------------------------------------------------------
    # Memory Worker
    # --------------------------------------------------------

    def memory_worker(self):

        memory: List[bytes] = []

        while self.backend_overloaded:

            try:

                memory.append(
                    bytearray(1024 * 1024)
                )

                if len(memory) > 50:

                    memory.pop(0)

                time.sleep(0.1)

            except MemoryError:

                logger.warning(
                    "Memory pressure detected"
                )

                memory.clear()

                gc.collect()

    # --------------------------------------------------------
    # Start Overload
    # --------------------------------------------------------

    def start_backend_overload(self):

        if self.backend_overloaded:

            return

        logger.warning(
            "Starting overload simulation"
        )

        self.backend_overloaded = True

        self.executor = ThreadPoolExecutor(
            max_workers=4
        )

        for _ in range(3):

            self.tasks.append(

                self.executor.submit(
                    self.cpu_worker
                )

            )

        self.tasks.append(

            self.executor.submit(
                self.memory_worker
            )

        )

    # --------------------------------------------------------
    # Stop Overload
    # --------------------------------------------------------

    def stop_backend_overload(self):

        if not self.backend_overloaded:

            return

        logger.info(
            "Stopping overload simulation"
        )

        self.backend_overloaded = False

        for task in self.tasks:

            task.cancel()

        self.tasks.clear()

        if self.executor:

            self.executor.shutdown(
                wait=False,
                cancel_futures=True,
            )

            self.executor = None

        gc.collect()

    # --------------------------------------------------------
    # Database Toggle
    # --------------------------------------------------------

    def toggle_database_connection(self):

        self.review_service.toggle_database_connection()

        return {

            "connected":
            self.review_service.is_database_connection_enabled(),

            "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat(),
        }

    # --------------------------------------------------------
    # Model Toggle
    # --------------------------------------------------------

    def toggle_model_server_connection(self):

        self.model_service.toggle_model_connection()

        return {

            "connected":
            self.model_service.is_model_connection_enabled(),

            "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat(),
        }

    # --------------------------------------------------------
    # Admin Dashboard
    # --------------------------------------------------------

    def get_admin_status(self):

        return {

            "backendHealthy":
            self.backend_healthy,

            "backendOverloaded":
            self.backend_overloaded,

            "databaseConnected":
            self.review_service.is_database_connection_enabled(),

            "modelServerConnected":
            self.model_service.is_model_connection_enabled(),

            "actualDatabaseStatus":
            self.review_service.is_database_available(),

            "actualModelServerStatus":
            self.model_service.is_model_server_available(),

            "reviewStats":
            self.review_service.get_review_stats(),

            "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat(),
        }

    # --------------------------------------------------------
    # Properties
    # --------------------------------------------------------

    def is_backend_healthy(self):

        return self.backend_healthy

    def is_backend_overloaded(self):

        return self.backend_overloaded