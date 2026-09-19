import os
from collections.abc import Generator
from pathlib import Path

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.base import Base
from app.db.session import get_db
from app.main import app

# ---------------------------------------------------------
# Load test environment variables
# ---------------------------------------------------------

BACKEND_DIR = Path(__file__).resolve().parents[1]

load_dotenv(
    BACKEND_DIR / ".env.test",
    override=False,
)


# ---------------------------------------------------------
# Test database
# ---------------------------------------------------------

TEST_DATABASE_URL = os.getenv(
    "DATABASE_URL"
)

if not TEST_DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not configured for tests. "
        "Create backend/.env.test with DATABASE_URL."
    )

if "salary_test_db" not in TEST_DATABASE_URL:
    raise RuntimeError(
        "Tests must use the salary_test_db database. "
        "Check backend/.env.test."
    )


test_engine = create_engine(
    TEST_DATABASE_URL,
    pool_pre_ping=True,
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)


# ---------------------------------------------------------
# Create database tables
# ---------------------------------------------------------

@pytest.fixture(scope="session", autouse=True)
def create_test_tables():
    """
    Create all application tables in the test database
    before the test suite starts.

    Drop them after the entire test suite finishes.
    """

    Base.metadata.create_all(bind=test_engine)

    yield

    Base.metadata.drop_all(bind=test_engine)


# ---------------------------------------------------------
# Database session fixture
# ---------------------------------------------------------

@pytest.fixture
def db_session() -> Generator[Session]:
    """
    Provide an isolated database session for each test.

    All changes are rolled back after the test so one test
    cannot affect another test.
    """

    connection = test_engine.connect()
    transaction = connection.begin()

    session = Session(
        bind=connection,
        join_transaction_mode="create_savepoint",
    )

    try:
        yield session

    finally:
        session.close()
        transaction.rollback()
        connection.close()


# ---------------------------------------------------------
# FastAPI dependency override
# ---------------------------------------------------------

@pytest.fixture
def client(
    db_session: Session,
) -> Generator[TestClient]:
    """
    Provide a FastAPI TestClient that uses the isolated
    test database session instead of the development database.
    """

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app, raise_server_exceptions=False) as test_client:
            yield test_client

    finally:
        app.dependency_overrides.clear()
