from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Generator

import httpx
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import DateTime, Float, String, create_engine, desc, text
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://movieuser:moviepass@localhost:5432/moviereviews",
)
MODEL_SERVER_URL = os.getenv("MODEL_SERVER_URL", "http://localhost:5000")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    movie_id: Mapped[str] = mapped_column(String(255), index=True)
    review_text: Mapped[str] = mapped_column(String(2000))
    sentiment: Mapped[str | None] = mapped_column(String(50), nullable=True)
    sentiment_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "movieId": self.movie_id,
            "reviewText": self.review_text,
            "sentiment": self.sentiment,
            "sentimentScore": self.sentiment_score,
            "rating": self.rating,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
        }


class ReviewRequest(BaseModel):
    movieId: str = Field(min_length=1, max_length=255)
    reviewText: str = Field(min_length=3, max_length=2000)


app = FastAPI(title="Movie Analyzer Backend", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"service": "Movie Analyzer Backend", "status": "running"}


@app.get("/health")
async def health(db: Session = Depends(get_db)) -> dict:
    db_ok = False
    model_ok = False

    try:
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        pass

    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(f"{MODEL_SERVER_URL}/health")
            model_ok = response.is_success
    except Exception:
        pass

    return {
        "status": "healthy" if db_ok and model_ok else "degraded",
        "backend": True,
        "database": db_ok,
        "model": model_ok,
    }


@app.get("/api/reviews/latest")
def latest_reviews(limit: int = 5, db: Session = Depends(get_db)) -> list[dict]:
    rows = db.query(Review).order_by(desc(Review.created_at)).limit(min(limit, 20)).all()
    return [row.to_dict() for row in rows]


@app.get("/api/reviews/{movie_id}")
def get_reviews(movie_id: str, db: Session = Depends(get_db)) -> list[dict]:
    rows = (
        db.query(Review)
        .filter(Review.movie_id == movie_id)
        .order_by(desc(Review.created_at))
        .all()
    )
    return [row.to_dict() for row in rows]


@app.post("/api/reviews", status_code=201)
async def submit_review(payload: ReviewRequest, db: Session = Depends(get_db)) -> dict:
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                f"{MODEL_SERVER_URL}/analyze",
                json={"text": payload.reviewText},
            )
            response.raise_for_status()
            analysis = response.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=503, detail="Sentiment model is unavailable") from exc

    review = Review(
        movie_id=payload.movieId,
        review_text=payload.reviewText,
        sentiment=analysis.get("sentiment"),
        sentiment_score=float(analysis.get("score", 0.0)),
        rating=float(analysis.get("rating", 3.0)),
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review.to_dict()
