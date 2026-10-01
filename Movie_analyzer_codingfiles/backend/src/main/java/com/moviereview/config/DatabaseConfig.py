import logging
import os
from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("database")

# Database URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///movie_review.db"
)

class DatabaseConfig:
    """
    Database configuration with graceful failure handling.

    Features:
    ----------
    ✔ Lazy database initialization
    ✔ Connection pooling
    ✔ Automatic reconnect
    ✔ Health check support
    ✔ Detailed logging
    ✔ Application continues even if DB is unavailable
    """

    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self.connected = False

    def initialize(self):
        """
        Initialize database connection without crashing the application.
        """

        try:
            self.engine = create_engine(
                DATABASE_URL,
                pool_pre_ping=True,
                pool_recycle=300,
                echo=False,
                future=True
            )

            self.SessionLocal = sessionmaker(
                bind=self.engine,
                autoflush=False,
                autocommit=False
            )

            # Test connection
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))

            self.connected = True
            logger.info("✅ Database connected successfully.")

        except SQLAlchemyError as ex:
            self.connected = False
            logger.error(f"❌ Database connection failed: {ex}")
            logger.warning(
                "Application will continue running in degraded mode."
            )

    def is_connected(self) -> bool:
        """Return current database connection status."""
        return self.connected

    @contextmanager
    def get_session(self):
        """
        Safely provide a database session.
        """

        if not self.connected:
            raise ConnectionError("Database is unavailable.")

        session = self.SessionLocal()

        try:
            yield session
            session.commit()

        except Exception:
            session.rollback()
            raise

        finally:
            session.close()


# Singleton instance
database = DatabaseConfig()

# Initialize at startup
database.initialize()