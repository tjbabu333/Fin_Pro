from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import (
    String,
    Float,
    DateTime,
    Integer,
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)

from pydantic import BaseModel, Field


# --------------------------------------------------
# SQLAlchemy Base
# --------------------------------------------------

class Base(DeclarativeBase):
    pass


# --------------------------------------------------
# Review Database Model
# --------------------------------------------------

class Review(Base):
    """
    Database model for movie reviews.
    """

    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    movie_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    review_text: Mapped[str] = mapped_column(
        String(2000),
        nullable=False,
    )

    sentiment: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    sentiment_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )

    rating: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self):

        return (
            f"<Review("
            f"id={self.id}, "
            f"movie='{self.movie_id}', "
            f"sentiment='{self.sentiment}', "
            f"rating={self.rating}"
            f")>"
        )

    def to_dict(self):

        return {

            "id": self.id,

            "movieId": self.movie_id,

            "reviewText": self.review_text,

            "sentiment": self.sentiment,

            "sentimentScore": self.sentiment_score,

            "rating": self.rating,

            "createdAt": self.created_at.isoformat(),
        }

class ReviewRequest(BaseModel):

    movieId: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

    reviewText: str = Field(
        ...,
        min_length=5,
        max_length=2000,
    )

class ReviewResponse(BaseModel):

    id: int

    movieId: str

    reviewText: str

    sentiment: Optional[str]

    sentimentScore: Optional[float]

    rating: Optional[float]

    createdAt: datetime

    class Config:
        from_attributes = True

def create_review(
    movie_id: str,
    review_text: str,
    sentiment: str,
    sentiment_score: float,
    rating: float,
) -> Review:

    return Review(
        movie_id=movie_id,
        review_text=review_text,
        sentiment=sentiment,
        sentiment_score=sentiment_score,
        rating=rating,
    )

