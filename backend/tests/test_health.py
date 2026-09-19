from unittest.mock import Mock

from fastapi.testclient import TestClient


def test_health_returns_request_id(client: TestClient):
    response = client.get("/health")

    assert response.status_code == 200

    request_id = response.headers.get("X-Request-ID")

    assert request_id is not None
    assert len(request_id) > 0


def test_health_preserves_request_id(client: TestClient):
    request_id = "test-request-123"

    response = client.get(
        "/health",
        headers={"X-Request-ID": request_id},
    )

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == request_id

def test_error_response_contains_request_id(client: TestClient):
    request_id = "test-error-request-123"

    response = client.get(
        "/api/v1/employees/999999999",
        headers={"X-Request-ID": request_id},
    )

    assert response.status_code == 404
    assert response.headers["X-Request-ID"] == request_id

    data = response.json()

    assert data["error"]["code"] == "EMPLOYEE_NOT_FOUND"

def test_readiness_returns_503_when_database_is_unavailable(
    client: TestClient,
):
    fake_db = Mock()
    fake_db.execute.side_effect = Exception("Database connection failed")

    from app.db.session import get_db
    from app.main import app

    def override_get_db():
        yield fake_db

    app.dependency_overrides[get_db] = override_get_db

    try:
        response = client.get("/ready")

        assert response.status_code == 503
        assert response.json() == {
            "detail": "Database is unavailable"
        }
    finally:
        app.dependency_overrides.clear()