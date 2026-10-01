from __future__ import annotations

import logging
from typing import List, Dict, Any
from dataclasses import dataclass

from models.review import Review
from repositories.review_repository import ReviewRepository
from services.model_server_service import (
    ModelServerService,
    ModelServerException,
)

logger = logging.getLogger(__name__)


# ==========================================================
# Custom Exceptions
# ==========================================================

class DatabaseException(Exception):
    """Raised when database operations fail."""
    pass


class ReviewSubmissionException(Exception):
    """Raised when a review cannot be submitted."""
    pass


# ==========================================================
# Review Submission Result
# ==========================================================

@dataclass
class ReviewSubmissionResult:

    success: bool

    review: Review

    message: str


# ==========================================================
# Review Service
# ==========================================================

class ReviewService:

    def __init__(
        self,
        repository: ReviewRepository,
        model_service: ModelServerService,
    ):

        self.repository = repository

        self.model_service = model_service

        # Used for admin simulation
        self.database_connected = True

    # ======================================================
    # Validation
    # ======================================================

    def validate_review(
        self,
        movie_id: str,
        review_text: str,
    ):

        if not movie_id or not movie_id.strip():

            raise ValueError(
                "Movie ID is required."
            )

        if not review_text or not review_text.strip():

            raise ValueError(
                "Review text is required."
            )

        if len(review_text) > 2000:

            raise ValueError(
                "Review exceeds maximum length."
            )

    # ======================================================
    # Fetch Reviews
    # ======================================================

    async def get_reviews_by_movie_id(
        self,
        movie_id: str,
    ) -> List[Review]:

        if not self.database_connected:

            raise DatabaseException(

                "Database connection disabled."

            )

        try:

            logger.info(

                "Fetching reviews for movie %s",

                movie_id,

            )

            reviews = self.repository.find_by_movie_id(
                movie_id
            )

            logger.info(

                "Found %d reviews",

                len(reviews),

            )

            return reviews

        except Exception as exc:

            logger.exception(exc)

            raise DatabaseException(

                "Unable to fetch reviews."

            )

    # ======================================================
    # Submit Review
    # ======================================================

    async def submit_review(
        self,
        movie_id: str,
        review_text: str,
    ) -> ReviewSubmissionResult:
        """
        Submit a review.

        Flow:

        1. Validate input
        2. Call AI model server
        3. If AI fails -> reject request
        4. If DB unavailable -> return analyzed review only
        5. Save review
        """

        logger.info(
            "Submitting review for movie %s",
            movie_id,
        )

        # -------------------------------
        # Validate Input
        # -------------------------------

        self.validate_review(
            movie_id,
            review_text,
        )

        # -------------------------------
        # Analyze Review
        # -------------------------------

        try:

            sentiment = await self.model_service.analyze_sentiment(
                review_text
            )

        except ModelServerException as exc:

            logger.error(
                "Model server unavailable: %s",
                exc,
            )

            raise ReviewSubmissionException(
                str(exc)
            )

        # -------------------------------
        # Create Review Object
        # -------------------------------

        review = Review(

            movie_id=movie_id,

            review_text=review_text,

            sentiment=sentiment.sentiment,

            sentiment_score=sentiment.score,

            rating=sentiment.rating,
        )

        # -------------------------------
        # Database Disabled
        # -------------------------------

        if not self.database_connected:

            logger.warning(
                "Database disabled. Returning review without saving."
            )

            return ReviewSubmissionResult(

                success=False,

                review=review,

                message=(
                    "Review analyzed successfully "
                    "but database is unavailable."
                ),
            )

        # -------------------------------
        # Save Review
        # -------------------------------

        try:

            saved_review = self.repository.save(
                review
            )

            logger.info(
                "Review saved successfully."
            )

            return ReviewSubmissionResult(

                success=True,

                review=saved_review,

                message="Review submitted successfully.",
            )

        except Exception as exc:

            logger.exception(exc)

            logger.warning(
                "Database save failed."
            )

            return ReviewSubmissionResult(

                success=False,

                review=review,

                message=(
                    "Review analyzed successfully "
                    "but could not be stored."
                ),
            )

    # ======================================================
    # Database Health Check
    # ======================================================

    def is_database_available(self) -> bool:
        """
        Check whether the database is available.
        """

        if not self.database_connected:
            return False

        try:

            # Simple health check
            self.repository.count()

            return True

        except Exception as exc:

            logger.exception(exc)

            return False

    # ======================================================
    # Toggle Database Connection
    # ======================================================

    def toggle_database_connection(self) -> None:
        """
        Admin simulation for database failure.
        """

        self.database_connected = (
            not self.database_connected
        )

        logger.warning(

            "Database connection %s",

            "ENABLED"
            if self.database_connected
            else "DISABLED",

        )

    # ======================================================
    # Database Connection Status
    # ======================================================

    def is_database_connection_enabled(
        self,
    ) -> bool:

        return self.database_connected

    # ======================================================
    # Review Statistics
    # ======================================================

    def get_review_stats(
        self,
    ) -> Dict[str, Any]:

        try:

            total = self.repository.count()

            return {

                "totalReviews": total,

                "databaseConnected":
                    self.is_database_available(),

            }

        except Exception:

            return {

                "totalReviews": 0,

                "databaseConnected": False,

                "error":
                    "Database unavailable",

            }

    # ======================================================
    # Latest Reviews
    # ======================================================

    async def get_latest_reviews(
        self,
        limit: int = 5,
    ) -> List[Review]:

        if not self.database_connected:

            raise DatabaseException(

                "Database unavailable."

            )

        try:

            logger.info(

                "Fetching latest %d reviews",

                limit,

            )

            reviews = self.repository.find_recent_reviews(
                limit
            )

            return reviews

        except Exception as exc:

            logger.exception(exc)

            raise DatabaseException(

                "Unable to fetch latest reviews."

            )