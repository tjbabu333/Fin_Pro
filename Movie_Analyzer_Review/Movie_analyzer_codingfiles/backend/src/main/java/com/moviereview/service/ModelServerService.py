from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional

import httpx
from pydantic import BaseModel

logger = logging.getLogger(__name__)


# ===========================================================
# Exceptions
# ===========================================================

class ModelServerException(Exception):
    """Raised when the model server cannot be reached."""
    pass


# ===========================================================
# Pydantic Response Model
# ===========================================================

class SentimentResult(BaseModel):

    sentiment: str

    score: float

    rating: float


# ===========================================================
# Model Server Service
# ===========================================================

class ModelServerService:

    def __init__(
        self,
        base_url: str = "http://localhost:8001",
        timeout: int = 3,
    ):

        self.base_url = base_url

        self.timeout = timeout

        self.model_server_connected = True

        self.client = httpx.AsyncClient(

            base_url=base_url,

            timeout=timeout,
        )

    # -------------------------------------------------------
    # Analyze Sentiment
    # -------------------------------------------------------

    async def analyze_sentiment(
        self,
        review_text: str,
    ) -> SentimentResult:

        if not self.model_server_connected:

            raise ModelServerException(
                "Model server disabled by administrator."
            )

        try:

            logger.info(
                "Sending review to model server..."
            )

            response = await self.client.post(

                "/analyze",

                json={
                    "text": review_text,
                },
            )

            response.raise_for_status()

            data = response.json()

            return SentimentResult(

                sentiment=data.get(
                    "sentiment",
                    "Neutral",
                ),

                score=float(
                    data.get(
                        "score",
                        0.0,
                    )
                ),

                rating=float(
                    data.get(
                        "rating",
                        3.0,
                    )
                ),
            )

        except httpx.TimeoutException:

            logger.exception("Model server timeout.")

            raise ModelServerException(

                "Model server timeout."

            )

        except httpx.HTTPError as exc:

            logger.exception(exc)

            raise ModelServerException(

                "Model server unavailable."

            )

    # -------------------------------------------------------
    # Health Check
    # -------------------------------------------------------

    async def is_model_server_available(
        self,
    ) -> bool:

        if not self.model_server_connected:

            return False

        try:

            response = await self.client.get(

                "/health"

            )

            response.raise_for_status()

            data = response.json()

            return (

                data.get("status")

                == "healthy"

            )

        except Exception:

            logger.exception(

                "Health check failed."

            )

            return False

    # -------------------------------------------------------
    # Toggle Connection
    # -------------------------------------------------------

    def toggle_model_connection(self):

        self.model_server_connected = (

            not self.model_server_connected

        )

        logger.info(

            "Model connection = %s",

            self.model_server_connected,

        )

    # -------------------------------------------------------
    # Getter
    # -------------------------------------------------------

    def is_model_connection_enabled(

        self,

    ) -> bool:

        return self.model_server_connected

    # -------------------------------------------------------
    # Close HTTP Client
    # -------------------------------------------------------

    async def close(self):

        await self.client.aclose()