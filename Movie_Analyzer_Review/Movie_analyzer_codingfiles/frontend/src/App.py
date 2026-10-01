"""
main.py
========

Movie Review Platform
Main Application Entry Point

Enhancements
------------
✓ Object-Oriented Architecture
✓ Async API Communication
✓ Background Tasks
✓ Automatic Health Monitoring
✓ Centralized Logging
✓ Clean Separation of Concerns
✓ Ready for NiceGUI
"""

from __future__ import annotations

import asyncio
import logging
from typing import Optional

from nicegui import ui

# -------------------------------------------------------
# Internal Modules
# -------------------------------------------------------

from app_state import AppState
from api_client import APIClient

from data.movies import MOVIES

from components.header import HeaderBanner
from components.movie_grid import MovieGrid
from components.latest_reviews import LatestReviews
from components.notifications import NotificationManager
from components.bottom_status import BottomStatusBar
from components.floating_admin import FloatingAdminPanel

# Movie detail page (Part 5)
# from components.movie_detail import MovieDetail


# -------------------------------------------------------
# Logging
# -------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("MovieReview")


# -------------------------------------------------------
# Application
# -------------------------------------------------------

class MovieReviewApplication:

    def __init__(self):

        logger.info("Starting Movie Review Platform")

        # -----------------------------
        # Global Objects
        # -----------------------------

        self.state = AppState()

        self.api = APIClient()

        self.notifications = NotificationManager()

        self.refresh_task: Optional[asyncio.Task] = None

        # -----------------------------
        # Build Interface
        # -----------------------------

        self.build_ui()

        # -----------------------------
        # Startup
        # -----------------------------

        ui.timer(
            0.1,
            self.initialize,
            once=True
        )

    # ---------------------------------------------------

    async def initialize(self):

        """
        Initial application loading.
        """

        logger.info("Initializing application...")

        self.state.loading = True

        try:

            await self.refresh_service_status()

        except Exception as exc:

            logger.exception(exc)

            self.notifications.error(
                "Unable to contact backend."
            )

        self.state.loading = False

        # Load reviews in background

        asyncio.create_task(
            self.load_all_reviews()
        )

        asyncio.create_task(
            self.load_latest_reviews()
        )

        # Refresh health every 10 seconds

        self.refresh_task = asyncio.create_task(
            self.health_monitor()
        )

    # ---------------------------------------------------

    async def health_monitor(self):

        """
        Periodic health monitoring.
        """

        while True:

            try:

                await asyncio.sleep(10)

                await self.refresh_service_status()

            except asyncio.CancelledError:

                logger.info("Health monitor stopped")

                return

            except Exception as exc:

                logger.error(exc)

    # ---------------------------------------------------

    async def refresh_service_status(self):

        """
        Refresh backend health.
        """

        status = await self.api.check_health()

        self.state.service_status.backend = status.backend

        self.state.service_status.database = status.database

        self.state.service_status.model = status.model

        self.state.service_status.backend_overloaded = (
            status.backend_overloaded
        )

        logger.info(
            "Backend=%s DB=%s Model=%s",
            status.backend,
            status.database,
            status.model,
        )

    # ---------------------------------------------------

    async def load_all_reviews(self):

        """
        Load reviews for every movie.
        """

        logger.info("Loading reviews...")

        for movie in MOVIES:

            try:

                reviews = await self.api.get_reviews(movie.id)

                self.state.reviews[movie.id] = reviews

            except Exception:

                self.state.reviews[movie.id] = []

        logger.info("Reviews loaded.")

    # ---------------------------------------------------

    async def load_latest_reviews(self):

        """
        Load latest reviews.
        """

        try:

            latest = await self.api.get_latest_reviews()

            self.state.latest_reviews = latest

            logger.info(
                "%d latest reviews loaded.",
                len(latest),
            )

        except Exception as exc:

            logger.error(exc)

            self.state.latest_reviews = []

    # ---------------------------------------------------

    def build_ui(self):

        """
        Build application interface.
        """

        with ui.column().classes("w-full items-center"):

            HeaderBanner()

            self.content_container = ui.column().classes(
                "w-full max-w-7xl"
            )

            BottomStatusBar(
                self.state,
                self.notifications,
            )

            FloatingAdminPanel(
                self.state,
                self.api,
                self.notifications,
            )

        self.render_home()

    # ---------------------------------------------------

    def render_home(self):

        """
        Initial home page.
        """

        self.content_container.clear()

        with self.content_container:

            ui.label(
                "Choose a Movie to Review"
            ).classes(
                "text-3xl font-bold"
            )

            ui.label(
                "Click any movie to open its review page."
            ).classes(
                "text-gray-500"
            )

            MovieGrid(

                movies=MOVIES,

                on_select=self.open_movie

            )

            LatestReviews(

                latest_reviews=self.state.latest_reviews

            )

    # ---------------------------------------------------

    def open_movie(self, movie):

        """
        Movie selected.
        """

        logger.info(
            "Movie selected: %s",
            movie.title
        )

        self.state.selected_movie = movie

        self.notifications.info(

            f"Viewing {movie.title}"

        )

        # Part 5 replaces this.

        ui.notify(
            "Movie Detail Screen "
            "will be implemented in Part 5."
        )


# -------------------------------------------------------
# Start Application
# -------------------------------------------------------

app = MovieReviewApplication()

ui.run(

    title="Movie Review Platform",

    reload=False,

    favicon="🎬",

    dark=False,

)

"""
Movie Review Platform
Part 1B - Configuration
Enhanced Python Version

Features
--------
✔ Environment variables
✔ .env support
✔ PostgreSQL configuration
✔ Connection pooling
✔ Model server configuration
✔ Logging
✔ Security
✔ Rate limiting
✔ Validation
"""

from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):

    # ====================================================
    # Application
    # ====================================================

    APP_NAME: str = "Movie Review Backend"

    APP_VERSION: str = "2.0.0"

    DEBUG: bool = False

    HOST: str = "0.0.0.0"

    PORT: int = 8000

    # ====================================================
    # Database
    # ====================================================

    DB_HOST: str = "localhost"

    DB_PORT: int = 5432

    DB_NAME: str = "moviereviews"

    DB_USER: str = "movieuser"

    DB_PASSWORD: str = "moviepass"

    DATABASE_POOL_SIZE: int = 10

    DATABASE_MAX_OVERFLOW: int = 20

    DATABASE_POOL_TIMEOUT: int = 30

    DATABASE_POOL_RECYCLE: int = 3600

    # ====================================================
    # AI Model Server
    # ====================================================

    MODEL_SERVER_URL: str = "http://localhost:5000"

    MODEL_SERVER_TIMEOUT: int = 5

    # ====================================================
    # Security
    # ====================================================

    SECRET_KEY: str = (
        "CHANGE_THIS_TO_A_RANDOM_SECRET_KEY"
    )

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    ALGORITHM: str = "HS256"

    # ====================================================
    # Rate Limiting
    # ====================================================

    RATE_LIMIT: str = "100/minute"

    # ====================================================
    # Logging
    # ====================================================

    LOG_LEVEL: str = "INFO"

    LOG_FORMAT: str = (
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings():

    return Settings()

"""
Database Engine

Uses SQLAlchemy 2.0
"""

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import declarative_base

from core.config import get_settings

settings = get_settings()

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{settings.DB_USER}:"
    f"{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:"
    f"{settings.DB_PORT}/"
    f"{settings.DB_NAME}"
)

engine = create_engine(

    DATABASE_URL,

    pool_size=settings.DATABASE_POOL_SIZE,

    max_overflow=settings.DATABASE_MAX_OVERFLOW,

    pool_timeout=settings.DATABASE_POOL_TIMEOUT,

    pool_recycle=settings.DATABASE_POOL_RECYCLE,

    future=True,

    echo=False
)

SessionLocal = sessionmaker(

    autoflush=False,

    autocommit=False,

    bind=engine
)

Base = declarative_base()


def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()

"""
Security Headers Middleware
"""

from starlette.middleware.base import BaseHTTPMiddleware


class SecurityHeadersMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        response = await call_next(request)

        response.headers["X-Frame-Options"] = "DENY"

        response.headers["X-Content-Type-Options"] = "nosniff"

        response.headers["Referrer-Policy"] = "strict-origin"

        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=()"
        )

        response.headers["X-XSS-Protection"] = "1; mode=block"

        return response

"""
CORS Configuration
"""

from fastapi.middleware.cors import CORSMiddleware


def configure_cors(app):

    app.add_middleware(

        CORSMiddleware,

        allow_origins=["*"],

        allow_methods=["*"],

        allow_headers=["*"],

        allow_credentials=True
    )

"""
Rate Limiter

Uses SlowAPI
"""

from slowapi import Limiter

from slowapi.util import get_remote_address

limiter = Limiter(

    key_func=get_remote_address,

    default_limits=["100/minute"]
)

"""
Application Startup
"""

from sqlalchemy import text

from core.database import engine

from core.logger import logger


def startup():

    logger.info("🚀 Starting Movie Review Backend")

    try:

        with engine.connect() as conn:

            conn.execute(text("SELECT 1"))

        logger.info("✅ Database Connected")

    except Exception as ex:

        logger.warning(f"Database unavailable: {ex}")

    logger.info("Application Ready")


def shutdown():

    logger.info("Stopping application...")

"""
Application Startup
"""

from sqlalchemy import text

from core.database import engine

from core.logger import logger


def startup():

    logger.info("🚀 Starting Movie Review Backend")

    try:

        with engine.connect() as conn:

            conn.execute(text("SELECT 1"))

        logger.info("✅ Database Connected")

    except Exception as ex:

        logger.warning(f"Database unavailable: {ex}")

    logger.info("Application Ready")


def shutdown():

    logger.info("Stopping application...")

###########################################
# Application
###########################################

APP_NAME=Movie Review Backend

APP_VERSION=2.0.0

DEBUG=False

HOST=0.0.0.0

PORT=8000

###########################################
# Database
###########################################

DB_HOST=localhost

DB_PORT=5432

DB_NAME=moviereviews

DB_USER=movieuser

DB_PASSWORD=moviepass

###########################################
# Model Server
###########################################

MODEL_SERVER_URL=http://localhost:5000

MODEL_SERVER_TIMEOUT=5

###########################################
# Security
###########################################

SECRET_KEY=CHANGE_THIS_SECRET_KEY

ACCESS_TOKEN_EXPIRE_MINUTES=60

###########################################
# Logging
###########################################

LOG_LEVEL=INFO

###################################
# Python
###################################

__pycache__/
*.pyc
*.pyo
*.pyd

###################################
# Virtual Environment
###################################

venv/
.env/
.venv/

###################################
# IDE
###################################

.vscode/
.idea/

###################################
# Logs
###################################

*.log

###################################
# Database
###################################

*.sqlite3

###################################
# Cache
###################################

.pytest_cache/
.mypy_cache/

###################################
# Build
###################################

build/
dist/

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]

version: "3.9"

services:

  backend:

    build: .

    container_name: movie-review-backend

    ports:
      - "8000:8000"

    env_file:
      - .env

    depends_on:
      - postgres

    restart: unless-stopped

  postgres:

    image: postgres:16

    container_name: movie-review-db

    environment:

      POSTGRES_DB: moviereviews

      POSTGRES_USER: movieuser

      POSTGRES_PASSWORD: moviepass

    ports:

      - "5432:5432"

    volumes:

      - postgres_data:/var/lib/postgresql/data

volumes:

  postgres_data:

"""
Global Application Constants
"""

from enum import Enum

APP_NAME = "Movie Review Backend"

APP_VERSION = "2.0.0"

MAX_REVIEW_LENGTH = 2000

LATEST_REVIEW_LIMIT = 5

DEFAULT_RATING = 3.0

MODEL_TIMEOUT = 5

DATABASE_TIMEOUT = 30


class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

"""
Custom Exceptions
"""


class DatabaseException(Exception):
    """Database unavailable"""

    pass


class ModelServerException(Exception):
    """AI Model unavailable"""

    pass


class ReviewSubmissionException(Exception):
    """Review submission failed"""

    pass


class ValidationException(Exception):
    """Invalid request"""

    pass

"""
Standard API Response Objects
"""

from datetime import datetime


def success(message, data=None):

    return {
        "success": True,
        "message": message,
        "timestamp": datetime.utcnow().isoformat(),
        "data": data,
    }


def error(message):

    return {
        "success": False,
        "message": message,
        "timestamp": datetime.utcnow().isoformat(),
    }


def warning(message, data=None):

    return {
        "success": False,
        "warning": True,
        "message": message,
        "timestamp": datetime.utcnow().isoformat(),
        "data": data,
    }

"""
Application Health Manager
"""


class HealthManager:

    backend = True

    database = True

    model = True

    backend_overloaded = False

    @classmethod
    def status(cls):

        if cls.backend and cls.database and cls.model:

            return "healthy"

        if cls.backend:

            return "degraded"

        return "unhealthy"

    @classmethod
    def toggle_backend(cls):

        cls.backend = not cls.backend

    @classmethod
    def toggle_database(cls):

        cls.database = not cls.database

    @classmethod
    def toggle_model(cls):

        cls.model = not cls.model

    @classmethod
    def toggle_overload(cls):

        cls.backend_overloaded = not cls.backend_overloaded

"""
Utility Functions
"""

from datetime import datetime


def utc_now():

    return datetime.utcnow()


def truncate(text, length=60):

    if len(text) <= length:

        return text

    return text[:length] + "..."


def is_blank(value):

    return value is None or value.strip() == ""

"""
Run Development Server
"""

import uvicorn

if __name__ == "__main__":

    uvicorn.run(

        "main:app",

        host="0.0.0.0",

        port=8000,

        reload=True
    )

"""
Initialize Database
"""

from core.database import Base
from core.database import engine

from models.review import Review

print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Database initialized.")

"""
Check Backend Health
"""

import requests

try:

    response = requests.get("http://localhost:8000/health")

    print(response.json())

except Exception as ex:

    print("Server unavailable")

    print(ex)

"""
Review Database Model

Enhanced SQLAlchemy Version
"""

from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Index,
    Text,
)

from core.database import Base


class Review(Base):
    """
    Review Entity
    """

    __tablename__ = "reviews"

    __table_args__ = (

        Index("idx_movie", "movie_id"),

        Index("idx_created", "created_at"),

        Index("idx_sentiment", "sentiment"),

    )

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    movie_id = Column(
        String(100),
        nullable=False
    )

    review_text = Column(
        Text,
        nullable=False
    )

    sentiment = Column(
        String(20),
        nullable=False
    )

    sentiment_score = Column(
        Float,
        default=0.0
    )

    rating = Column(
        Float,
        default=3.0
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):

        return (
            f"<Review("
            f"id={self.id}, "
            f"movie={self.movie_id}, "
            f"rating={self.rating})>"
        )

    @property
    def stars(self):

        return "⭐" * round(self.rating)

    @property
    def short_review(self):

        if len(self.review_text) < 100:
            return self.review_text

        return self.review_text[:100] + "..."

    def to_dict(self):

        return {

            "id": self.id,

            "movieId": self.movie_id,

            "reviewText": self.review_text,

            "sentiment": self.sentiment,

            "sentimentScore": self.sentiment_score,

            "rating": self.rating,

            "createdAt": self.created_at.isoformat(),

            "updatedAt": self.updated_at.isoformat()
            if self.updated_at else None,

        }

"""
Pydantic Schemas
"""

from datetime import datetime

from pydantic import BaseModel

from pydantic import Field

from pydantic import ConfigDict


class ReviewCreate(BaseModel):

    movieId: str = Field(..., min_length=1)

    reviewText: str = Field(
        ...,
        min_length=3,
        max_length=2000
    )


class ReviewResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    movieId: str

    reviewText: str

    sentiment: str

    sentimentScore: float

    rating: float

    createdAt: datetime


class ReviewSubmissionResult(BaseModel):

    success: bool

    review: ReviewResponse | None

    message: str

"""
Repository Layer

Enhanced Version
"""

from sqlalchemy.orm import Session

from sqlalchemy import desc

from models.review import Review


class ReviewRepository:

    def __init__(self, db: Session):

        self.db = db

    def save(self, review: Review):

        self.db.add(review)

        self.db.commit()

        self.db.refresh(review)

        return review

    def find_by_movie(self, movie_id: str):

        return (

            self.db.query(Review)

            .filter(
                Review.movie_id == movie_id
            )

            .order_by(
                desc(Review.created_at)
            )

            .all()

        )

    def latest_reviews(self, limit=5):

        return (

            self.db.query(Review)

            .order_by(
                desc(Review.created_at)
            )

            .limit(limit)

            .all()

        )

    def count_reviews(self):

        return self.db.query(Review).count()

    def count_movie_reviews(self, movie_id):

        return (

            self.db.query(Review)

            .filter(
                Review.movie_id == movie_id
            )

            .count()

        )

    def delete(self, review_id):

        review = self.db.get(
            Review,
            review_id
        )

        if review:

            self.db.delete(review)

            self.db.commit()

            return True

        return False

    def exists(self, review_id):

        return self.db.get(
            Review,
            review_id
        ) is not None

    def health_check(self):

        self.db.execute("SELECT 1")

from pydantic import BaseModel


class HealthResponse(BaseModel):

    status: str

    database: bool

    modelServer: bool

    backendHealthy: bool

    backendOverloaded: bool

    timestamp: str


class ToggleResponse(BaseModel):

    message: str

    timestamp: str

from dataclasses import dataclass


@dataclass
class Movie:

    id: str

    title: str

    year: int

    genre: str

    thumbnail: str

from models.movie import Movie

MOVIES = [

    Movie(
        "shawshank",
        "The Shawshank Redemption",
        1994,
        "Drama",
        "/images/movies/shawshank-redemption.jpg",
    ),

    Movie(
        "inception",
        "Inception",
        2010,
        "Sci-Fi",
        "/images/movies/inception.jpg",
    ),

    Movie(
        "interstellar",
        "Interstellar",
        2014,
        "Sci-Fi",
        "/images/movies/interstellar.jpg",
    ),

    Movie(
        "fight-club",
        "Fight Club",
        1999,
        "Drama",
        "/images/movies/fight-club.jpg",
    ),

    Movie(
        "gladiator",
        "Gladiator",
        2000,
        "Action",
        "/images/movies/gladiator.jpg",
    ),

    Movie(
        "dark-knight",
        "The Dark Knight",
        2008,
        "Action",
        "/images/movies/dark-knight.jpg",
    ),

]

"""
Movie Review Platform
Model Server Service

Enhanced Python Version

Features
--------
✓ Async HTTP client
✓ Connection pooling
✓ Automatic retries
✓ Timeout handling
✓ Health checking
✓ Connection simulation
✓ Better logging
✓ Type hints
✓ Production ready
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import asyncio
import httpx

from core.config import get_settings
from core.logger import logger
from core.exceptions import ModelServerException

settings = get_settings()


@dataclass
class SentimentResult:
    """
    Result returned from the AI Model Server.
    """

    sentiment: str
    score: float
    rating: float

    def to_dict(self):

        return {
            "sentiment": self.sentiment,
            "score": self.score,
            "rating": self.rating,
        }


class ModelServerService:
    """
    AI Model Server Client

    Responsible for

    • sentiment analysis

    • health checking

    • connection simulation

    • retry logic

    """

    def __init__(self):

        self.base_url = settings.MODEL_SERVER_URL

        self.timeout = settings.MODEL_SERVER_TIMEOUT

        self.connected = True

        self.client = httpx.AsyncClient(

            base_url=self.base_url,

            timeout=httpx.Timeout(self.timeout),

            limits=httpx.Limits(

                max_connections=100,

                max_keepalive_connections=20

            )

        )

    # --------------------------------------------------------
    # Connection Simulation
    # --------------------------------------------------------

    def toggle_model_connection(self):

        self.connected = not self.connected

        logger.warning(

            "Model Server Connection %s",

            "ENABLED"

            if self.connected

            else "DISABLED"

        )

    def is_model_connection_enabled(self):

        return self.connected

    # --------------------------------------------------------
    # Health Check
    # --------------------------------------------------------

    async def health_check(self) -> bool:

        if not self.connected:

            return False

        try:

            response = await self.client.get("/health")

            response.raise_for_status()

            data = response.json()

            healthy = (

                data.get("status")

                == "healthy"

            )

            if healthy:

                logger.info(

                    "✓ Model Server Healthy"

                )

            else:

                logger.warning(

                    "Model Server Unhealthy"

                )

            return healthy

        except Exception as ex:

            logger.error(

                "Model Server Health Failed: %s",

                ex

            )

            return False

    # --------------------------------------------------------
    # Sentiment Analysis
    # --------------------------------------------------------

    async def analyze_sentiment(

        self,

        review_text: str

    ) -> SentimentResult:

        if not self.connected:

            raise ModelServerException(

                "Model server disabled "

                "(Admin Simulation)"

            )

        payload = {

            "text": review_text

        }

        retries = 3

        for attempt in range(retries):

            try:

                logger.info(

                    "Calling AI Model "

                    "(Attempt %d)",

                    attempt + 1

                )

                response = await self.client.post(

                    "/analyze",

                    json=payload

                )

                response.raise_for_status()

                data: dict[str, Any] = response.json()

                if "sentiment" not in data:

                    raise ModelServerException(

                        "Invalid AI response."

                    )

                result = SentimentResult(

                    sentiment=data.get(

                        "sentiment",

                        "neutral"

                    ),

                    score=float(

                        data.get(

                            "score",

                            0

                        )

                    ),

                    rating=float(

                        data.get(

                            "rating",

                            3.0

                        )

                    )

                )

                logger.info(

                    "AI Result: %s | %.2f | %.1f⭐",

                    result.sentiment,

                    result.score,

                    result.rating

                )

                return result

            except (

                httpx.ConnectError,

                httpx.ReadTimeout,

                httpx.NetworkError

            ):

                logger.warning(

                    "Retrying AI Server..."

                )

                await asyncio.sleep(1)

            except Exception as ex:

                logger.error(

                    "AI Error: %s",

                    ex

                )

                raise ModelServerException(

                    "Model server unavailable"

                )

        raise ModelServerException(

            "AI server unreachable."

        )

    # --------------------------------------------------------
    # Ping
    # --------------------------------------------------------

    async def ping(self):

        try:

            response = await self.client.get("/")

            return response.status_code == 200

        except Exception:

            return False

    # --------------------------------------------------------
    # Close Client
    # --------------------------------------------------------

    async def close(self):

        await self.client.aclose()

        logger.info(

            "Model Server Client Closed"

        )


# --------------------------------------------------------
# Singleton Instance
# --------------------------------------------------------

model_server_service = ModelServerService()

"""
Movie Review Platform
Review Service

Enhanced Python Version

Features
--------
✓ Async database support
✓ Repository pattern
✓ AI integration
✓ Validation
✓ Health monitoring
✓ Logging
✓ Graceful failure handling
"""

from __future__ import annotations

from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from core.logger import logger
from core.constants import LATEST_REVIEW_LIMIT
from core.exceptions import (
    DatabaseException,
    ReviewSubmissionException,
)

from repositories.review_repository import ReviewRepository
from models.review import Review
from schemas.review_schema import (
    ReviewCreate,
    ReviewSubmissionResult,
)

from services.model_server_service import (
    ModelServerService,
    SentimentResult,
)


class ReviewService:
    """
    Handles all review-related business logic.
    """

    def __init__(
        self,
        db: Session,
        model_service: ModelServerService,
    ):

        self.db = db

        self.repository = ReviewRepository(db)

        self.model_service = model_service

        # Admin simulation flag
        self.database_connected = True

    # ======================================================
    # Database Health
    # ======================================================

    async def is_database_available(self) -> bool:
        """
        Check whether the database is reachable.
        """

        if not self.database_connected:
            return False

        try:

            self.repository.health_check()

            return True

        except Exception as ex:

            logger.error(
                "Database Health Failed: %s",
                ex,
            )

            return False

    def toggle_database_connection(self):
        """
        Admin simulation.
        """

        self.database_connected = (
            not self.database_connected
        )

        logger.warning(
            "Database Connection %s",
            "ENABLED"
            if self.database_connected
            else "DISABLED",
        )

    def is_database_connection_enabled(self):

        return self.database_connected

    # ======================================================
    # Validation
    # ======================================================

    @staticmethod
    def validate_request(review: ReviewCreate):

        if not review.movieId.strip():

            raise ValueError(
                "Movie ID is required."
            )

        if not review.reviewText.strip():

            raise ValueError(
                "Review text is required."
            )

        if len(review.reviewText) > 2000:

            raise ValueError(
                "Review exceeds maximum length."
            )

    # ======================================================
    # Get Reviews
    # ======================================================

    async def get_reviews_by_movie(
        self,
        movie_id: str,
    ) -> List[Review]:

        if not self.database_connected:

            raise DatabaseException(
                "Database connection disabled."
            )

        try:

            logger.info(
                "Loading reviews for %s",
                movie_id,
            )

            reviews = (
                self.repository.find_by_movie(
                    movie_id
                )
            )

            logger.info(
                "Loaded %d reviews",
                len(reviews),
            )

            return reviews

        except SQLAlchemyError as ex:

            logger.error(
                "Database Error: %s",
                ex,
            )

            raise DatabaseException(
                "Unable to load reviews."
            )

    # ======================================================
    # Latest Reviews
    # ======================================================

    async def get_latest_reviews(
        self,
        limit: int = LATEST_REVIEW_LIMIT,
    ) -> List[Review]:

        if not self.database_connected:

            raise DatabaseException(
                "Database unavailable."
            )

        try:

            return (
                self.repository.latest_reviews(
                    limit
                )
            )

        except SQLAlchemyError as ex:

            logger.error(ex)

            raise DatabaseException(
                "Unable to fetch latest reviews."
            )

    # ======================================================
    # Statistics
    # ======================================================

    async def get_review_statistics(self):

        try:

            total = (
                self.repository.count_reviews()
            )

            return {

                "totalReviews": total,

                "databaseConnected":
                    await self.is_database_available(),

                "databaseSimulation":
                    self.database_connected,

            }

        except Exception:

            return {

                "totalReviews": 0,

                "databaseConnected": False,

                "databaseSimulation":
                    self.database_connected,

            }

"""
Movie Review Platform
Part 3B-2
Remaining UI Components

Includes:
✓ Movie Grid
✓ Notifications
✓ Bottom Status Bar
"""

from nicegui import ui
from typing import List, Dict, Callable
from datetime import datetime


# ============================================================
# MOVIE GRID
# ============================================================

class MovieGrid:

    def __init__(self, movies: List[dict], on_movie_select: Callable):
        self.movies = movies
        self.on_movie_select = on_movie_select

    def render(self):

        with ui.grid(columns=3).classes("w-full gap-6"):

            for movie in self.movies:

                with ui.card().classes(
                    "cursor-pointer hover:shadow-xl transition-all"
                ).on(
                    "click",
                    lambda e, m=movie: self.on_movie_select(m)
                ):

                    ui.image(movie["thumbnail"]).classes(
                        "w-full h-64 object-cover rounded"
                    )

                    with ui.card_section():

                        ui.label(movie["title"]).classes(
                            "text-lg font-bold"
                        )

                        ui.label(
                            f"{movie['year']} • {movie['genre']}"
                        ).classes("text-gray-500")


# ============================================================
# NOTIFICATIONS
# ============================================================

class NotificationCenter:

    COLORS = {
        "success": "positive",
        "error": "negative",
        "warning": "warning",
        "info": "info"
    }

    @staticmethod
    def notify(message: str, level="info"):

        ui.notify(
            message,
            type=NotificationCenter.COLORS.get(level, "info"),
            timeout=3000,
            position="top-right"
        )


# ============================================================
# BOTTOM STATUS BAR
# ============================================================

class BottomStatusBar:

    def __init__(self, state):
        self.state = state

    def render(self):

        with ui.footer().classes(
            "bg-slate-900 text-white justify-between px-6"
        ):

            # -------------------------
            # Individual Services
            # -------------------------

            with ui.row().classes("items-center gap-5"):

                self._service(
                    "Frontend",
                    True,
                    self.state.frontend_overloaded
                )

                self._service(
                    "Backend",
                    self.state.backend,
                    self.state.backend_overloaded
                )

                self._service(
                    "Database",
                    self.state.database,
                    False
                )

                self._service(
                    "Model",
                    self.state.model,
                    False
                )

            # -------------------------
            # Overall Health
            # -------------------------

            ui.label(
                self.get_health_message()
            ).classes("font-bold")

    # --------------------------------------------------------

    def _service(
            self,
            name,
            online,
            overloaded=False
    ):

        color = "green" if online else "red"

        text = name

        if overloaded:
            text += " (Overloaded)"

        with ui.row().classes("items-center gap-2"):

            ui.icon(
                "circle",
                color=color
            ).classes("text-xs")

            ui.label(text)

    # --------------------------------------------------------

    def get_health_message(self):

        services = [
            self.state.backend,
            self.state.database,
            self.state.model
        ]

        online = sum(1 for s in services if s)

        overloaded = (
            self.state.frontend_overloaded
            or
            self.state.backend_overloaded
        )

        if online == 3 and not overloaded:
            return "✅ All Systems Operational"

        elif online == 3:
            return "⚡ Systems Online but Overloaded"

        elif online >= 2:
            return "⚠ Partial Service Degradation"

        elif online == 1:
            return "🔴 Major Service Outage"

        else:
            return "💥 Critical System Failure"


# ============================================================
# REVIEW CARD
# ============================================================

class ReviewCard:

    @staticmethod
    def render(review: Dict):

        sentiment = review.get("sentiment", "neutral")

        colors = {
            "positive": "green",
            "negative": "red",
            "neutral": "gray"
        }

        emojis = {
            "positive": "😊",
            "negative": "😞",
            "neutral": "😐"
        }

        with ui.card().classes("w-full mb-4"):

            with ui.row().classes("justify-between w-full"):

                ui.label(
                    review["movie_title"]
                ).classes("font-bold text-lg")

                ui.badge(
                    f"{emojis[sentiment]} {sentiment}",
                    color=colors[sentiment]
                )

            ui.label(
                review["review_text"]
            )

            ui.separator()

            with ui.row().classes("justify-between w-full"):

                ui.label(
                    f"⭐ {review.get('rating',0):.1f}"
                )

                created = review.get("created_at")

                if isinstance(created, str):

                    try:
                        created = datetime.fromisoformat(created)
                        created = created.strftime("%b %d, %Y")
                    except:
                        pass

                ui.label(str(created))

"""
Movie Review Platform
Part 3B-3

Extra reusable UI components

Includes
---------
✓ Loading Overlay
✓ Confirmation Dialog
✓ Movie Details Dialog
✓ Review Statistics Card
✓ Empty State Widget
✓ Error Widget
"""

from nicegui import ui
from datetime import datetime


# =====================================================
# Loading Overlay
# =====================================================

class LoadingOverlay:

    def __init__(self):

        self.dialog = ui.dialog()

        with self.dialog:

            with ui.card().classes(
                "items-center justify-center p-8"
            ):

                ui.spinner(size="lg")

                ui.label(
                    "Loading..."
                ).classes(
                    "text-lg font-bold mt-4"
                )

    def show(self):
        self.dialog.open()

    def hide(self):
        self.dialog.close()


# =====================================================
# Confirmation Dialog
# =====================================================

class ConfirmDialog:

    @staticmethod
    async def show(title, message):

        dialog = ui.dialog()

        result = {"value": False}

        with dialog, ui.card():

            ui.label(title).classes(
                "text-xl font-bold"
            )

            ui.label(message)

            with ui.row():

                ui.button(
                    "Cancel",
                    on_click=lambda: (
                        result.update(value=False),
                        dialog.close()
                    )
                )

                ui.button(
                    "Confirm",
                    color="red",
                    on_click=lambda: (
                        result.update(value=True),
                        dialog.close()
                    )
                )

        dialog.open()

        await dialog

        return result["value"]


# =====================================================
# Movie Details Dialog
# =====================================================

class MovieDialog:

    @staticmethod
    def show(movie):

        dialog = ui.dialog()

        with dialog:

            with ui.card().classes("w-[650px]"):

                ui.image(
                    movie["thumbnail"]
                ).classes("w-full rounded")

                ui.label(
                    movie["title"]
                ).classes(
                    "text-2xl font-bold mt-4"
                )

                ui.label(
                    f"{movie['year']} • {movie['genre']}"
                ).classes(
                    "text-gray-500"
                )

                if movie.get("description"):

                    ui.separator()

                    ui.label(
                        movie["description"]
                    )

                ui.button(
                    "Close",
                    on_click=dialog.close
                )

        dialog.open()


# =====================================================
# Review Statistics Card
# =====================================================

class ReviewStatistics:

    @staticmethod
    def render(stats):

        with ui.card().classes("w-full p-5"):

            ui.label(
                "Review Statistics"
            ).classes(
                "text-xl font-bold"
            )

            ui.separator()

            with ui.grid(columns=2):

                ReviewStatistics.metric(
                    "Total Reviews",
                    stats.get("totalReviews", 0)
                )

                ReviewStatistics.metric(
                    "Positive",
                    stats.get("positive", 0)
                )

                ReviewStatistics.metric(
                    "Negative",
                    stats.get("negative", 0)
                )

                ReviewStatistics.metric(
                    "Average Rating",
                    f"{stats.get('averageRating',0):.1f}"
                )

    @staticmethod
    def metric(name, value):

        with ui.card().classes("text-center"):

            ui.label(str(value)).classes(
                "text-3xl font-bold text-blue-700"
            )

            ui.label(name)


# =====================================================
# Empty State Widget
# =====================================================

class EmptyState:

    @staticmethod
    def render(
        title="Nothing here",
        subtitle="No data available.",
        icon="📭"
    ):

        with ui.column().classes(
            "items-center justify-center w-full p-10"
        ):

            ui.label(icon).classes("text-6xl")

            ui.label(title).classes(
                "text-2xl font-bold"
            )

            ui.label(subtitle).classes(
                "text-gray-500"
            )


# =====================================================
# Error Widget
# =====================================================

class ErrorWidget:

    @staticmethod
    def render(error):

        with ui.card().classes(
            "w-full bg-red-50 border-red-300"
        ):

            ui.label("❌ Error").classes(
                "text-xl text-red-700 font-bold"
            )

            ui.label(str(error)).classes(
                "text-red-600"
            )


# =====================================================
# Date Formatting Utility
# =====================================================

def pretty_date(date):

    if date is None:
        return "Unknown"

    if isinstance(date, str):

        try:
            date = datetime.fromisoformat(date)
        except Exception:
            return date

    return date.strftime("%b %d, %Y %I:%M %p")

"""
Movie Review Platform
Home Page

Features
--------
✓ Header Banner
✓ Movie Grid
✓ Latest Reviews
✓ Bottom Status Bar
✓ Floating Admin Panel
✓ Auto Refresh
"""

from nicegui import ui

from data.movies import MOVIES
from components import (
    HeaderBanner,
    MovieGrid,
    LatestReviews,
    FloatingAdminPanel,
    BottomStatusBar,
    NotificationCenter
)

from api_client import APIClient
from state import AppState


class HomePage:

    def __init__(self):

        self.api = APIClient()

        self.state = AppState()

        self.latest_reviews = []

    # ----------------------------------------------------

    async def load_data(self):

        try:

            self.latest_reviews = await self.api.get_latest_reviews()

            status = await self.api.get_service_status()

            self.state.backend = status["backend"]
            self.state.database = status["database"]
            self.state.model = status["model"]
            self.state.backend_overloaded = status["backendOverloaded"]

        except Exception:

            NotificationCenter.notify(
                "Backend unavailable",
                "warning"
            )

    # ----------------------------------------------------

    async def refresh(self):

        await self.load_data()

        ui.navigate.reload()

    # ----------------------------------------------------

    def open_movie(self, movie):

        ui.navigate.to(f"/movie/{movie['id']}")

    # ----------------------------------------------------

    async def render(self):

        await self.load_data()

        HeaderBanner().render()

        ui.separator()

        ui.label(
            "Choose a Movie"
        ).classes(
            "text-3xl font-bold mt-6"
        )

        MovieGrid(
            MOVIES,
            self.open_movie
        ).render()

        ui.separator()

        LatestReviews(
            self.latest_reviews
        ).render()

        FloatingAdminPanel(
            self.state,
            self.refresh
        ).render()

        BottomStatusBar(
            self.state
        ).render()

"""
Movie Review Platform
Movie Review Page

Features
--------
✓ Display selected movie
✓ Submit review
✓ AI Sentiment Analysis
✓ Rating Display
✓ Review History
✓ Loading Spinner
✓ Error Handling
"""

from nicegui import ui

from api_client import APIClient
from state import AppState
from components import (
    ReviewCard,
    NotificationCenter,
    LoadingOverlay,
    EmptyState
)
from data.movies import MOVIES


class MovieReviewPage:

    def __init__(self, movie_id: str):

        self.movie_id = movie_id

        self.api = APIClient()

        self.state = AppState()

        self.loading = LoadingOverlay()

        self.review_box = None

        self.review_history = []

        self.movie = self.find_movie()

    # -------------------------------------------------

    def find_movie(self):

        for movie in MOVIES:
            if movie["id"] == self.movie_id:
                return movie

        return None

    # -------------------------------------------------

    async def load_reviews(self):

        try:

            self.review_history = await self.api.get_reviews(
                self.movie_id
            )

        except Exception:

            self.review_history = []

            NotificationCenter.notify(
                "Unable to load review history.",
                "warning"
            )

    # -------------------------------------------------

    async def submit_review(self):

        review = self.review_box.value.strip()

        if len(review) < 5:

            NotificationCenter.notify(
                "Review is too short.",
                "warning"
            )

            return

        self.loading.show()

        try:

            result = await self.api.submit_review(
                self.movie_id,
                review
            )

            self.loading.hide()

            if result["success"]:

                NotificationCenter.notify(
                    "Review submitted successfully!",
                    "success"
                )

                self.review_box.value = ""

                await self.load_reviews()

                ui.navigate.reload()

            else:

                NotificationCenter.notify(
                    result["message"],
                    "warning"
                )

        except Exception as e:

            self.loading.hide()

            NotificationCenter.notify(
                str(e),
                "error"
            )

    # -------------------------------------------------

    async def render(self):

        if self.movie is None:

            ui.label(
                "Movie not found."
            ).classes("text-red text-xl")

            return

        await self.load_reviews()

        with ui.row().classes("w-full gap-8"):

            # -----------------------------
            # Left Side
            # -----------------------------

            with ui.column().classes("w-1/3"):

                ui.image(
                    self.movie["thumbnail"]
                ).classes(
                    "rounded shadow-lg"
                )

                ui.label(
                    self.movie["title"]
                ).classes(
                    "text-3xl font-bold"
                )

                ui.label(
                    f"{self.movie['year']} • {self.movie['genre']}"
                ).classes(
                    "text-gray-500"
                )

            # -----------------------------
            # Right Side
            # -----------------------------

            with ui.column().classes("w-2/3"):

                ui.label(
                    "Write a Review"
                ).classes(
                    "text-2xl font-bold"
                )

                self.review_box = ui.textarea(
                    placeholder="Share your thoughts..."
                ).classes("w-full")

                ui.button(
                    "Analyze & Submit",
                    color="green",
                    on_click=self.submit_review
                )

                ui.separator()

                ui.label(
                    "Community Reviews"
                ).classes(
                    "text-2xl font-bold"
                )

                if not self.review_history:

                    EmptyState.render(
                        "No Reviews",
                        "Be the first to review this movie.",
                        "🎬"
                    )

                else:

                    for review in self.review_history:

                        ReviewCard.render(
                            {
                                "movie_title": self.movie["title"],
                                "review_text": review["reviewText"],
                                "sentiment": review["sentiment"],
                                "rating": review["rating"],
                                "created_at": review["createdAt"]
                            }
                        )

        ui.button(
            "← Back to Home",
            on_click=lambda: ui.navigate.to("/")
        ).classes("mt-8")

"""
Movie Review Platform
Part 4C

Admin Dashboard

Features
--------
✓ Frontend Controls
✓ Backend Controls
✓ Database Controls
✓ Model Server Controls
✓ Backend Overload
✓ Service Status
✓ Review Statistics
✓ Auto Refresh
"""

from nicegui import ui

from api_client import APIClient
from state import AppState
from components import NotificationCenter


class AdminDashboard:

    def __init__(self):

        self.api = APIClient()

        self.state = AppState()

        self.status = {}

        self.review_stats = {}

    # --------------------------------------------------------
    # Load backend information
    # --------------------------------------------------------

    async def load_status(self):

        try:

            self.status = await self.api.get_admin_status()

            self.review_stats = self.status.get(
                "reviewStats",
                {}
            )

        except Exception as e:

            NotificationCenter.notify(
                str(e),
                "error"
            )

    # --------------------------------------------------------

    async def refresh(self):

        await self.load_status()

        ui.notify(
            "Status refreshed",
            type="info"
        )

        ui.navigate.reload()

    # --------------------------------------------------------

    async def toggle_backend(self):

        await self.api.toggle_backend_health()

        NotificationCenter.notify(
            "Backend health toggled",
            "success"
        )

        await self.refresh()

    # --------------------------------------------------------

    async def toggle_database(self):

        await self.api.toggle_database()

        NotificationCenter.notify(
            "Database connection changed",
            "success"
        )

        await self.refresh()

    # --------------------------------------------------------

    async def toggle_model(self):

        await self.api.toggle_model()

        NotificationCenter.notify(
            "Model server changed",
            "success"
        )

        await self.refresh()

    # --------------------------------------------------------

    async def toggle_overload(self):

        await self.api.toggle_backend_overload()

        NotificationCenter.notify(
            "Backend overload toggled",
            "warning"
        )

        await self.refresh()

    # --------------------------------------------------------

    def service_card(self, title, online):

        color = (
            "green"
            if online
            else "red"
        )

        with ui.card().classes(
            "w-52 text-center"
        ):

            ui.icon(
                "dns",
                color=color
            ).classes(
                "text-5xl"
            )

            ui.label(title).classes(
                "text-xl font-bold"
            )

            ui.label(
                "ONLINE"
                if online
                else "OFFLINE"
            ).classes(
                f"text-{color}-600"
            )

    # --------------------------------------------------------

    async def render(self):

        await self.load_status()

        ui.label(
            "⚙ Admin Dashboard"
        ).classes(
            "text-4xl font-bold mb-6"
        )

        # =====================================================
        # SERVICE STATUS
        # =====================================================

        ui.label(
            "Service Status"
        ).classes(
            "text-2xl font-bold"
        )

        with ui.row().classes(
            "gap-4"
        ):

            self.service_card(
                "Backend",
                self.status.get(
                    "backendHealthy",
                    False
                )
            )

            self.service_card(
                "Database",
                self.status.get(
                    "databaseConnected",
                    False
                )
            )

            self.service_card(
                "Model Server",
                self.status.get(
                    "modelServerConnected",
                    False
                )
            )

        ui.separator()

        # =====================================================
        # BACKEND CONTROLS
        # =====================================================

        ui.label(
            "Backend Controls"
        ).classes(
            "text-2xl font-bold"
        )

        with ui.row():

            ui.button(
                "Toggle Backend Health",
                color="green",
                on_click=self.toggle_backend
            )

            ui.button(
                "Toggle Backend Overload",
                color="orange",
                on_click=self.toggle_overload
            )

            ui.button(
                "Toggle Database",
                color="blue",
                on_click=self.toggle_database
            )

            ui.button(
                "Toggle Model Server",
                color="purple",
                on_click=self.toggle_model
            )

            ui.button(
                "Refresh",
                icon="refresh",
                on_click=self.refresh
            )

        ui.separator()

        # =====================================================
        # REVIEW STATISTICS
        # =====================================================

        ui.label(
            "Review Statistics"
        ).classes(
            "text-2xl font-bold"
        )

        with ui.grid(columns=2):

            with ui.card():

                ui.label(
                    "Total Reviews"
                ).classes(
                    "text-lg"
                )

                ui.label(
                    str(
                        self.review_stats.get(
                            "totalReviews",
                            0
                        )
                    )
                ).classes(
                    "text-4xl font-bold"
                )

            with ui.card():

                ui.label(
                    "Database Status"
                ).classes(
                    "text-lg"
                )

                ui.label(

                    "Available"

                    if self.review_stats.get(
                        "databaseConnected",
                        False
                    )

                    else

                    "Unavailable"

                ).classes(
                    "text-3xl"
                )

        ui.separator()

        # =====================================================
        # SYSTEM INFORMATION
        # =====================================================

        ui.label(
            "System Information"
        ).classes(
            "text-2xl font-bold"
        )

        with ui.card().classes("w-full"):

            ui.label(
                f"Backend Healthy : {self.status.get('backendHealthy')}"
            )

            ui.label(
                f"Backend Overloaded : {self.status.get('backendOverloaded')}"
            )

            ui.label(
                f"Database Connected : {self.status.get('databaseConnected')}"
            )

            ui.label(
                f"Model Connected : {self.status.get('modelServerConnected')}"
            )

            ui.label(
                f"Actual Database Status : {self.status.get('actualDatabaseStatus')}"
            )

            ui.label(
                f"Actual Model Status : {self.status.get('actualModelServerStatus')}"
            )

            ui.label(
                f"Timestamp : {self.status.get('timestamp')}"
            )

        ui.separator()

        ui.button(
            "← Back to Home",
            icon="home",
            on_click=lambda: ui.navigate.to("/")
        )

        # =====================================================
        # AUTO REFRESH
        # =====================================================

        ui.timer(
            interval=5,
            callback=self.refresh
        )

"""
Movie Review Platform
Part 4D

router.py

Application Router

Registers all application pages.
"""

from nicegui import ui

from pages.home import HomePage
from pages.movie_review import MovieReviewPage
from pages.admin_dashboard import AdminDashboard


# ==========================================================
# Global Theme
# ==========================================================

def setup_theme():

    ui.colors(
        primary="#2563eb",
        secondary="#0f172a",
        accent="#14b8a6",
        positive="#22c55e",
        negative="#ef4444",
        warning="#f59e0b",
        info="#3b82f6"
    )

    ui.add_head_html("""

    <style>

    body{
        background:#f8fafc;
        font-family:Inter,sans-serif;
    }

    .page-container{
        max-width:1400px;
        margin:auto;
        padding:30px;
    }

    </style>

    """)


# ==========================================================
# Home Route
# ==========================================================

@ui.page("/")
async def home():

    setup_theme()

    with ui.column().classes(
        "page-container w-full"
    ):

        page = HomePage()

        await page.render()


# ==========================================================
# Movie Route
# ==========================================================

@ui.page("/movie/{movie_id}")
async def movie(movie_id: str):

    setup_theme()

    with ui.column().classes(
        "page-container w-full"
    ):

        page = MovieReviewPage(movie_id)

        await page.render()


# ==========================================================
# Admin Route
# ==========================================================

@ui.page("/admin")
async def admin():

    setup_theme()

    with ui.column().classes(
        "page-container w-full"
    ):

        page = AdminDashboard()

        await page.render()


# ==========================================================
# 404 Page
# ==========================================================

@ui.page("/404")
def page_not_found():

    setup_theme()

    with ui.column().classes(
        "items-center justify-center w-full h-screen"
    ):

        ui.icon(
            "error_outline",
            size="100px",
            color="red"
        )

        ui.label(
            "404"
        ).classes(
            "text-6xl font-bold"
        )

        ui.label(
            "Page Not Found"
        ).classes(
            "text-2xl"
        )

        ui.button(
            "Go Home",
            icon="home",
            on_click=lambda: ui.navigate.to("/")
        )


# ==========================================================
# Navigation Helper
# ==========================================================

class Router:

    @staticmethod
    def home():

        ui.navigate.to("/")

    @staticmethod
    def admin():

        ui.navigate.to("/admin")

    @staticmethod
    def movie(movie_id: str):

        ui.navigate.to(
            f"/movie/{movie_id}"
        )

    @staticmethod
    def back():

        ui.navigate.back()


# ==========================================================
# Global Navigation Menu
# ==========================================================

def navigation_bar():

    with ui.header().classes(
        "bg-blue-700 text-white items-center justify-between px-8"
    ):

        ui.label(
            "🎬 Movie Review Platform"
        ).classes(
            "text-2xl font-bold"
        )

        with ui.row():

            ui.button(
                "Home",
                icon="home",
                on_click=Router.home
            ).props("flat color=white")

            ui.button(
                "Admin",
                icon="settings",
                on_click=Router.admin
            ).props("flat color=white")

"""
===========================================================
Movie Review Platform
Part 4E - Reusable UI Widgets
===========================================================

Contains:
✔ Header Banner
✔ Notification System
✔ Bottom Status Bar
✔ Loading Spinner
✔ Movie Card Widget
✔ Rating Stars
✔ Sentiment Badge
✔ Gradient Panels
✔ Animated Buttons

Author: ChatGPT Enhanced Version
"""

from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QMessageBox,
    QGraphicsDropShadowEffect,
)

from PyQt6.QtGui import (
    QColor,
    QFont,
)

from PyQt6.QtCore import (
    Qt,
    QTimer,
)


# ==========================================================
# Notification Widget
# ==========================================================

class Notification(QWidget):
    """
    Small popup notification.
    Automatically disappears.
    """

    COLORS = {
        "success": "#16a34a",
        "warning": "#f59e0b",
        "error": "#dc2626",
        "info": "#2563eb"
    }

    def __init__(self, message, kind="info"):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowType.Tool |
            Qt.WindowType.FramelessWindowHint
        )

        self.setStyleSheet(f"""
            QWidget {{
                background:{self.COLORS.get(kind,"#2563eb")};
                color:white;
                border-radius:12px;
                padding:12px;
            }}
        """)

        layout = QHBoxLayout(self)

        label = QLabel(message)
        label.setWordWrap(True)

        layout.addWidget(label)

        QTimer.singleShot(3000, self.close)


# ==========================================================
# Header Banner
# ==========================================================

class HeaderBanner(QFrame):

    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
        QFrame{
            background:qlineargradient(
                x1:0,y1:0,
                x2:1,y2:1,
                stop:0 #1e3a8a,
                stop:1 #2563eb);
            border-radius:18px;
            padding:25px;
        }
        QLabel{
            color:white;
        }
        """)

        layout = QVBoxLayout(self)

        title = QLabel("🎬 Movie Review Platform")
        title.setFont(QFont("Segoe UI",22,QFont.Weight.Bold))

        subtitle = QLabel(
            "AI Powered Movie Reviews\n"
            "FastAPI • PostgreSQL • Docker • Kubernetes"
        )

        subtitle.setFont(QFont("Segoe UI",11))

        tags = QLabel(
            "🚀 Docker     ☸ Kubernetes     🤖 AI"
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(tags)


# ==========================================================
# Sentiment Badge
# ==========================================================

class SentimentBadge(QLabel):

    COLORS = {
        "positive": "#16a34a",
        "negative": "#dc2626",
        "neutral": "#64748b"
    }

    ICONS = {
        "positive":"😊",
        "negative":"😞",
        "neutral":"😐"
    }

    def __init__(self, sentiment):

        super().__init__()

        color = self.COLORS.get(sentiment,"gray")
        icon = self.ICONS.get(sentiment,"😐")

        self.setText(f"{icon} {sentiment.title()}")

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet(f"""
        QLabel{{
            background:{color};
            color:white;
            padding:5px 10px;
            border-radius:12px;
            font-weight:bold;
        }}
        """)


# ==========================================================
# Rating Stars
# ==========================================================

class RatingStars(QLabel):

    def __init__(self, rating):

        super().__init__()

        stars = "⭐" * round(rating)

        self.setText(f"{stars} ({rating:.1f}/5)")
        self.setFont(QFont("Segoe UI",10))


# ==========================================================
# Status Bar
# ==========================================================

class BottomStatusBar(QFrame):

    def __init__(self):

        super().__init__()

        self.setFixedHeight(50)

        self.setStyleSheet("""
        QFrame{
            background:#111827;
            color:white;
        }
        """)

        self.layout = QHBoxLayout(self)

        self.frontend = QLabel()
        self.backend = QLabel()
        self.database = QLabel()
        self.model = QLabel()
        self.summary = QLabel()

        self.layout.addWidget(self.frontend)
        self.layout.addWidget(self.backend)
        self.layout.addWidget(self.database)
        self.layout.addWidget(self.model)
        self.layout.addStretch()
        self.layout.addWidget(self.summary)

    def update_status(
            self,
            frontend,
            backend,
            database,
            model,
            frontend_overload=False,
            backend_overload=False
    ):

        self.frontend.setText(
            f"Frontend {'🟢' if frontend else '🔴'}"
        )

        self.backend.setText(
            f"Backend {'🟢' if backend else '🔴'}"
        )

        self.database.setText(
            f"Database {'🟢' if database else '🔴'}"
        )

        self.model.setText(
            f"Model {'🟢' if model else '🔴'}"
        )

        online = sum([
            frontend,
            backend,
            database,
            model
        ])

        if online == 4:
            msg = "✅ All Systems Operational"

        elif online >= 2:
            msg = "⚠ Partial Service Degradation"

        else:
            msg = "💥 Critical Failure"

        if frontend_overload or backend_overload:
            msg += " | ⚡ Overloaded"

        self.summary.setText(msg)


# ==========================================================
# Animated Button
# ==========================================================

class AnimatedButton(QPushButton):

    def __init__(self, text, color="#2563eb"):

        super().__init__(text)

        self.default = color

        self.setStyleSheet(f"""
        QPushButton{{
            background:{color};
            color:white;
            padding:12px;
            border:none;
            border-radius:10px;
            font-size:14px;
            font-weight:bold;
        }}

        QPushButton:hover{{
            background:#1d4ed8;
        }}

        QPushButton:pressed{{
            background:#1e40af;
        }}
        """)

        shadow = QGraphicsDropShadowEffect()

        shadow.setBlurRadius(15)
        shadow.setOffset(0,4)
        shadow.setColor(QColor(0,0,0,80))

        self.setGraphicsEffect(shadow)


# ==========================================================
# Movie Card
# ==========================================================

class MovieCard(QFrame):

    def __init__(self, movie, callback):

        super().__init__()

        self.movie = movie
        self.callback = callback

        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setStyleSheet("""
        QFrame{
            background:white;
            border-radius:15px;
            border:1px solid #d1d5db;
        }

        QFrame:hover{
            border:2px solid #2563eb;
        }
        """)

        layout = QVBoxLayout(self)

        poster = QLabel("🎬")
        poster.setAlignment(Qt.AlignmentFlag.AlignCenter)
        poster.setFont(QFont("Arial",40))

        title = QLabel(movie.title)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        genre = QLabel(
            f"{movie.genre} • {movie.year}"
        )

        genre.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(poster)
        layout.addWidget(title)
        layout.addWidget(genre)

    def mousePressEvent(self, event):
        self.callback(self.movie)


# ==========================================================
# Loading Spinner
# ==========================================================

class LoadingSpinner(QLabel):

    def __init__(self):

        super().__init__("⏳ Loading...")

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet("""
        QLabel{
            color:#2563eb;
            font-size:18px;
            font-weight:bold;
        }
        """)


# ==========================================================
# Message Boxes
# ==========================================================

def show_success(text):
    QMessageBox.information(None, "Success", text)


def show_error(text):
    QMessageBox.critical(None, "Error", text)


def show_warning(text):
    QMessageBox.warning(None, "Warning", text)

"""
===========================================================
Movie Review Platform
Part 4E - Reusable UI Widgets
===========================================================

Contains:
✔ Header Banner
✔ Notification System
✔ Bottom Status Bar
✔ Loading Spinner
✔ Movie Card Widget
✔ Rating Stars
✔ Sentiment Badge
✔ Gradient Panels
✔ Animated Buttons

Author: ChatGPT Enhanced Version
"""

from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QMessageBox,
    QGraphicsDropShadowEffect,
)

from PyQt6.QtGui import (
    QColor,
    QFont,
)

from PyQt6.QtCore import (
    Qt,
    QTimer,
)


# ==========================================================
# Notification Widget
# ==========================================================

class Notification(QWidget):
    """
    Small popup notification.
    Automatically disappears.
    """

    COLORS = {
        "success": "#16a34a",
        "warning": "#f59e0b",
        "error": "#dc2626",
        "info": "#2563eb"
    }

    def __init__(self, message, kind="info"):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowType.Tool |
            Qt.WindowType.FramelessWindowHint
        )

        self.setStyleSheet(f"""
            QWidget {{
                background:{self.COLORS.get(kind,"#2563eb")};
                color:white;
                border-radius:12px;
                padding:12px;
            }}
        """)

        layout = QHBoxLayout(self)

        label = QLabel(message)
        label.setWordWrap(True)

        layout.addWidget(label)

        QTimer.singleShot(3000, self.close)


# ==========================================================
# Header Banner
# ==========================================================

class HeaderBanner(QFrame):

    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
        QFrame{
            background:qlineargradient(
                x1:0,y1:0,
                x2:1,y2:1,
                stop:0 #1e3a8a,
                stop:1 #2563eb);
            border-radius:18px;
            padding:25px;
        }
        QLabel{
            color:white;
        }
        """)

        layout = QVBoxLayout(self)

        title = QLabel("🎬 Movie Review Platform")
        title.setFont(QFont("Segoe UI",22,QFont.Weight.Bold))

        subtitle = QLabel(
            "AI Powered Movie Reviews\n"
            "FastAPI • PostgreSQL • Docker • Kubernetes"
        )

        subtitle.setFont(QFont("Segoe UI",11))

        tags = QLabel(
            "🚀 Docker     ☸ Kubernetes     🤖 AI"
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(tags)


# ==========================================================
# Sentiment Badge
# ==========================================================

class SentimentBadge(QLabel):

    COLORS = {
        "positive": "#16a34a",
        "negative": "#dc2626",
        "neutral": "#64748b"
    }

    ICONS = {
        "positive":"😊",
        "negative":"😞",
        "neutral":"😐"
    }

    def __init__(self, sentiment):

        super().__init__()

        color = self.COLORS.get(sentiment,"gray")
        icon = self.ICONS.get(sentiment,"😐")

        self.setText(f"{icon} {sentiment.title()}")

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet(f"""
        QLabel{{
            background:{color};
            color:white;
            padding:5px 10px;
            border-radius:12px;
            font-weight:bold;
        }}
        """)


# ==========================================================
# Rating Stars
# ==========================================================

class RatingStars(QLabel):

    def __init__(self, rating):

        super().__init__()

        stars = "⭐" * round(rating)

        self.setText(f"{stars} ({rating:.1f}/5)")
        self.setFont(QFont("Segoe UI",10))


# ==========================================================
# Status Bar
# ==========================================================

class BottomStatusBar(QFrame):

    def __init__(self):

        super().__init__()

        self.setFixedHeight(50)

        self.setStyleSheet("""
        QFrame{
            background:#111827;
            color:white;
        }
        """)

        self.layout = QHBoxLayout(self)

        self.frontend = QLabel()
        self.backend = QLabel()
        self.database = QLabel()
        self.model = QLabel()
        self.summary = QLabel()

        self.layout.addWidget(self.frontend)
        self.layout.addWidget(self.backend)
        self.layout.addWidget(self.database)
        self.layout.addWidget(self.model)
        self.layout.addStretch()
        self.layout.addWidget(self.summary)

    def update_status(
            self,
            frontend,
            backend,
            database,
            model,
            frontend_overload=False,
            backend_overload=False
    ):

        self.frontend.setText(
            f"Frontend {'🟢' if frontend else '🔴'}"
        )

        self.backend.setText(
            f"Backend {'🟢' if backend else '🔴'}"
        )

        self.database.setText(
            f"Database {'🟢' if database else '🔴'}"
        )

        self.model.setText(
            f"Model {'🟢' if model else '🔴'}"
        )

        online = sum([
            frontend,
            backend,
            database,
            model
        ])

        if online == 4:
            msg = "✅ All Systems Operational"

        elif online >= 2:
            msg = "⚠ Partial Service Degradation"

        else:
            msg = "💥 Critical Failure"

        if frontend_overload or backend_overload:
            msg += " | ⚡ Overloaded"

        self.summary.setText(msg)


# ==========================================================
# Animated Button
# ==========================================================

class AnimatedButton(QPushButton):

    def __init__(self, text, color="#2563eb"):

        super().__init__(text)

        self.default = color

        self.setStyleSheet(f"""
        QPushButton{{
            background:{color};
            color:white;
            padding:12px;
            border:none;
            border-radius:10px;
            font-size:14px;
            font-weight:bold;
        }}

        QPushButton:hover{{
            background:#1d4ed8;
        }}

        QPushButton:pressed{{
            background:#1e40af;
        }}
        """)

        shadow = QGraphicsDropShadowEffect()

        shadow.setBlurRadius(15)
        shadow.setOffset(0,4)
        shadow.setColor(QColor(0,0,0,80))

        self.setGraphicsEffect(shadow)


# ==========================================================
# Movie Card
# ==========================================================

class MovieCard(QFrame):

    def __init__(self, movie, callback):

        super().__init__()

        self.movie = movie
        self.callback = callback

        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setStyleSheet("""
        QFrame{
            background:white;
            border-radius:15px;
            border:1px solid #d1d5db;
        }

        QFrame:hover{
            border:2px solid #2563eb;
        }
        """)

        layout = QVBoxLayout(self)

        poster = QLabel("🎬")
        poster.setAlignment(Qt.AlignmentFlag.AlignCenter)
        poster.setFont(QFont("Arial",40))

        title = QLabel(movie.title)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        genre = QLabel(
            f"{movie.genre} • {movie.year}"
        )

        genre.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(poster)
        layout.addWidget(title)
        layout.addWidget(genre)

    def mousePressEvent(self, event):
        self.callback(self.movie)


# ==========================================================
# Loading Spinner
# ==========================================================

class LoadingSpinner(QLabel):

    def __init__(self):

        super().__init__("⏳ Loading...")

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet("""
        QLabel{
            color:#2563eb;
            font-size:18px;
            font-weight:bold;
        }
        """)


# ==========================================================
# Message Boxes
# ==========================================================

def show_success(text):
    QMessageBox.information(None, "Success", text)


def show_error(text):
    QMessageBox.critical(None, "Error", text)


def show_warning(text):
    QMessageBox.warning(None, "Warning", text)

"""
=========================================================
Main Application Controller
=========================================================
"""

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
)

from ui.home_window import HomeWindow
from ui.review_window import ReviewWindow
from ui.admin_window import AdminWindow
from ui.latest_reviews_window import LatestReviewsWindow

from services.review_service import ReviewService
from services.admin_service import AdminService
from services.model_service import ModelServerService

from database.repository import ReviewRepository

from api.api_client import APIClient


class MovieReviewApplication(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("🎬 Movie Review Platform")
        self.resize(1400, 900)

        # -------------------------
        # Backend
        # -------------------------

        self.api = APIClient()

        self.repository = ReviewRepository()

        self.model_service = ModelServerService(self.api)

        self.review_service = ReviewService(
            self.repository,
            self.model_service
        )

        self.admin_service = AdminService(
            self.review_service,
            self.model_service
        )

        # -------------------------
        # Windows
        # -------------------------

        self.home = HomeWindow(self.review_service)

        self.review = ReviewWindow(self.review_service)

        self.admin = AdminWindow(self.admin_service)

        self.latest = LatestReviewsWindow(
            self.review_service
        )

        # -------------------------

        container = QWidget()

        layout = QVBoxLayout(container)

        layout.addWidget(self.home)
        layout.addWidget(self.latest)
        layout.addWidget(self.admin)

        self.setCentralWidget(container)

        self.connect_events()

    def connect_events(self):

        self.home.movie_selected.connect(
            self.open_movie
        )

    def open_movie(self, movie):

        self.review.load_movie(movie)

        self.review.show()

PyQt6>=6.7.0

requests>=2.32.0

httpx>=0.28.0

sqlalchemy>=2.0.30

psycopg2-binary>=2.9.10

pydantic>=2.8.0

python-dotenv>=1.0.1

loguru>=0.7.2

pillow>=10.4.0

fastapi>=0.112.0

uvicorn>=0.30.0

aiohttp>=3.10.0

"""
Simple launcher
"""

from main import main

if __name__ == "__main__":
    main()


