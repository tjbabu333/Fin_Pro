"""Database engine/session setup."""

from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from finban_mapper.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_session() -> Generator[Session, None, None]:
    """FastAPI dependency: yields a session, closes it after the request."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
