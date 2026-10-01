from typing import List, Optional

from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from models.review import Review


class ReviewRepository:
    """
    Repository layer for Review database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    # -------------------------------------------------
    # Save Review
    # -------------------------------------------------

    def save(self, review: Review) -> Review:
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        return review

    # -------------------------------------------------
    # Find By ID
    # -------------------------------------------------

    def find_by_id(self, review_id: int) -> Optional[Review]:
        return (
            self.db.query(Review)
            .filter(Review.id == review_id)
            .first()
        )

    # -------------------------------------------------
    # Find Reviews By Movie
    # -------------------------------------------------

    def find_by_movie_id(
        self,
        movie_id: str
    ) -> List[Review]:

        return (
            self.db.query(Review)
            .filter(Review.movie_id == movie_id)
            .order_by(desc(Review.created_at))
            .all()
        )

    # -------------------------------------------------
    # Count Reviews
    # -------------------------------------------------

    def count_by_movie_id(
        self,
        movie_id: str
    ) -> int:

        return (
            self.db.query(func.count(Review.id))
            .filter(Review.movie_id == movie_id)
            .scalar()
        )

    # -------------------------------------------------
    # Recent Reviews
    # -------------------------------------------------

    def find_recent_reviews(
        self,
        limit: int = 10
    ) -> List[Review]:

        return (
            self.db.query(Review)
            .order_by(desc(Review.created_at))
            .limit(limit)
            .all()
        )

    # -------------------------------------------------
    # Latest Five Reviews
    # -------------------------------------------------

    def find_top_five_reviews(self):

        return self.find_recent_reviews(limit=5)

    # -------------------------------------------------
    # Delete Review
    # -------------------------------------------------

    def delete(self, review: Review):

        self.db.delete(review)
        self.db.commit()

    # -------------------------------------------------
    # Find All Reviews
    # -------------------------------------------------

    def find_all(self):

        return (
            self.db.query(Review)
            .order_by(desc(Review.created_at))
            .all()
        )

    # -------------------------------------------------
    # Search Reviews
    # -------------------------------------------------

    def search_reviews(
        self,
        keyword: str
    ) -> List[Review]:

        return (
            self.db.query(Review)
            .filter(
                Review.review_text.ilike(
                    f"%{keyword}%"
                )
            )
            .all()
        )

    # -------------------------------------------------
    # Pagination
    # -------------------------------------------------

    def paginate(
        self,
        page: int = 1,
        page_size: int = 20,
    ):

        offset = (page - 1) * page_size

        return (
            self.db.query(Review)
            .order_by(desc(Review.created_at))
            .offset(offset)
            .limit(page_size)
            .all()
        )

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///movie_reviews.db"

engine = create_engine(
    DATABASE_URL,
    echo=False,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

from fastapi import Depends
from sqlalchemy.orm import Session

from repositories.review_repository import ReviewRepository
from database import get_db


def get_review_repository(
    db: Session = Depends(get_db)
):

    return ReviewRepository(db)

