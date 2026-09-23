from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from finban_mapper.main import app
from finban_mapper.persistence.db import get_session
from finban_mapper.persistence.models import Base


def _make_test_client() -> TestClient:
    """TestClient wired to an in-memory SQLite DB instead of real Postgres.

    StaticPool keeps the same connection alive across requests — plain
    ``sqlite:///:memory:`` otherwise hands out a fresh, empty database
    per connection.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine)

    def override_get_session():
        session = TestSession()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_session] = override_get_session
    return TestClient(app)


def test_health_check():
    client = _make_test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_entity_state_404_when_not_found():
    client = _make_test_client()
    resp = client.get("/entities/offer/does-not-exist/state")
    assert resp.status_code == 404
