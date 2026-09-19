from fastapi.testclient import TestClient


def employee_payload(
    employee_code: str = "TEST_EMP_001",
    email: str = "test.employee@example.com",
) -> dict:
    return {
        "employee_code": employee_code,
        "full_name": "Test Employee",
        "email": email,
        "country": "India",
        "department": "Engineering",
        "job_title": "Python Developer",
        "status": "ACTIVE",
    }


def test_create_employee(client: TestClient):
    response = client.post(
        "/api/v1/employees",
        json=employee_payload(),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["employee_code"] == "TEST_EMP_001"
    assert data["full_name"] == "Test Employee"
    assert data["email"] == "test.employee@example.com"
    assert data["country"] == "India"
    assert data["department"] == "Engineering"
    assert data["job_title"] == "Python Developer"
    assert data["status"] == "ACTIVE"
    assert "id" in data


def test_create_duplicate_employee_code(
    client: TestClient,
):
    payload = employee_payload(
        employee_code="DUPLICATE_001",
        email="duplicate1@example.com",
    )

    first_response = client.post(
        "/api/v1/employees",
        json=payload,
    )

    assert first_response.status_code == 200

    second_response = client.post(
        "/api/v1/employees",
        json=employee_payload(
            employee_code="DUPLICATE_001",
            email="duplicate2@example.com",
        ),
    )

    assert second_response.status_code == 409

    data = second_response.json()

    assert data["error"]["code"] == (
        "EMPLOYEE_ALREADY_EXISTS"
    )


def test_create_duplicate_employee_email(
    client: TestClient,
):
    client.post(
        "/api/v1/employees",
        json=employee_payload(
            employee_code="EMAIL_DUP_001",
            email="same@example.com",
        ),
    )

    response = client.post(
        "/api/v1/employees",
        json=employee_payload(
            employee_code="EMAIL_DUP_002",
            email="same@example.com",
        ),
    )

    assert response.status_code == 409

    data = response.json()

    assert data["error"]["code"] == (
        "EMPLOYEE_ALREADY_EXISTS"
    )


def test_create_employee_validation_error(
    client: TestClient,
):
    payload = employee_payload()

    payload["email"] = "invalid-email"

    response = client.post(
        "/api/v1/employees",
        json=payload,
    )

    assert response.status_code == 422

    data = response.json()

    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_get_employees(
    client: TestClient,
):
    client.post(
        "/api/v1/employees",
        json=employee_payload(
            employee_code="GET_EMP_001",
            email="get.employee@example.com",
        ),
    )

    response = client.get(
        "/api/v1/employees",
    )

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "page" in data
    assert "page_size" in data
    assert "total" in data

    assert data["page"] == 1
    assert data["page_size"] == 20
    assert data["total"] >= 1
    assert isinstance(data["items"], list)


def test_get_employee_by_id(
    client: TestClient,
):
    create_response = client.post(
        "/api/v1/employees",
        json=employee_payload(
            employee_code="GET_BY_ID_001",
            email="getbyid@example.com",
        ),
    )

    assert create_response.status_code == 200

    employee_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/employees/{employee_id}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == employee_id
    assert data["employee_code"] == "GET_BY_ID_001"


def test_get_employee_not_found(
    client: TestClient,
):
    response = client.get(
        "/api/v1/employees/999999999",
    )

    assert response.status_code == 404

    data = response.json()

    assert data["error"]["code"] == (
        "EMPLOYEE_NOT_FOUND"
    )


def test_update_employee(
    client: TestClient,
):
    create_response = client.post(
        "/api/v1/employees",
        json=employee_payload(
            employee_code="UPDATE_EMP_001",
            email="update@example.com",
        ),
    )

    assert create_response.status_code == 200

    employee_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/employees/{employee_id}",
        json={
            "department": "Finance",
            "job_title": "Senior Python Developer",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == employee_id
    assert data["department"] == "Finance"
    assert data["job_title"] == (
        "Senior Python Developer"
    )


def test_update_employee_not_found(
    client: TestClient,
):
    response = client.patch(
        "/api/v1/employees/999999999",
        json={
            "department": "Finance",
        },
    )

    assert response.status_code == 404

    data = response.json()

    assert data["error"]["code"] == (
        "EMPLOYEE_NOT_FOUND"
    )


def test_employee_search(
    client: TestClient,
):
    client.post(
        "/api/v1/employees",
        json=employee_payload(
            employee_code="SEARCH_PYTHON_001",
            email="search.python@example.com",
        ),
    )

    response = client.get(
        "/api/v1/employees",
        params={
            "search": "SEARCH_PYTHON_001",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert (
        data["items"][0]["employee_code"]
        == "SEARCH_PYTHON_001"
    )


def test_employee_pagination(
    client: TestClient,
):
    for number in range(1, 6):
        client.post(
            "/api/v1/employees",
            json=employee_payload(
                employee_code=f"PAGE_EMP_{number:03d}",
                email=f"page{number}@example.com",
            ),
        )

    response = client.get(
        "/api/v1/employees",
        params={
            "page": 1,
            "page_size": 2,
            "search": "PAGE_EMP_",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["page_size"] == 2
    assert data["total"] == 5
    assert len(data["items"]) == 2
