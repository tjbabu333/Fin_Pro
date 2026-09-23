from fastapi.testclient import TestClient


def employee_payload(
    employee_code: str = "SALARY_TEST_EMP_001",
    email: str = "salary.employee@example.com",
) -> dict:
    return {
        "employee_code": employee_code,
        "full_name": "Salary Test Employee",
        "email": email,
        "country": "India",
        "department": "Engineering",
        "job_title": "Python Developer",
        "status": "ACTIVE",
    }


def salary_payload(
    base_salary: str = "75000.00",
    bonus: str = "5000.00",
    currency: str = "USD",
    effective_from: str = "2026-01-01",
    effective_to: str | None = None,
) -> dict:
    return {
        "base_salary": base_salary,
        "bonus": bonus,
        "currency": currency,
        "effective_from": effective_from,
        "effective_to": effective_to,
    }


def create_employee(
    client: TestClient,
    employee_code: str = "SALARY_TEST_EMP_001",
    email: str = "salary.employee@example.com",
) -> int:
    response = client.post(
        "/api/v1/employees",
        json=employee_payload(
            employee_code=employee_code,
            email=email,
        ),
    )

    assert response.status_code == 200

    return response.json()["id"]


def create_salary(
    client: TestClient,
    employee_id: int,
    payload: dict | None = None,
) -> dict:
    response = client.post(
        f"/api/v1/employees/{employee_id}/salaries",
        json=payload or salary_payload(),
    )

    assert response.status_code == 201

    return response.json()


def test_create_salary(
    client: TestClient,
):
    employee_id = create_employee(client)

    salary = create_salary(
        client,
        employee_id,
    )

    assert salary["employee_id"] == employee_id
    assert salary["base_salary"] == "75000.00"
    assert salary["bonus"] == "5000.00"
    assert salary["currency"] == "USD"
    assert salary["effective_from"] == "2026-01-01"
    assert salary["effective_to"] is None


def test_create_salary_currency_is_uppercase(
    client: TestClient,
):
    employee_id = create_employee(
        client,
        employee_code="SALARY_UPPER_001",
        email="salary.upper@example.com",
    )

    salary = create_salary(
        client,
        employee_id,
        salary_payload(
            currency="inr",
        ),
    )

    assert salary["currency"] == "INR"


def test_create_salary_employee_not_found(
    client: TestClient,
):
    response = client.post(
        "/api/v1/employees/999999999/salaries",
        json=salary_payload(),
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Employee not found"


def test_create_salary_negative_base_salary(
    client: TestClient,
):
    employee_id = create_employee(
        client,
        employee_code="SALARY_NEG_BASE_001",
        email="salary.neg.base@example.com",
    )

    response = client.post(
        f"/api/v1/employees/{employee_id}/salaries",
        json=salary_payload(
            base_salary="-1.00",
        ),
    )

    assert response.status_code == 422

    data = response.json()

    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_create_salary_negative_bonus(
    client: TestClient,
):
    employee_id = create_employee(
        client,
        employee_code="SALARY_NEG_BONUS_001",
        email="salary.neg.bonus@example.com",
    )

    response = client.post(
        f"/api/v1/employees/{employee_id}/salaries",
        json=salary_payload(
            bonus="-1.00",
        ),
    )

    assert response.status_code == 422

    data = response.json()

    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_create_salary_invalid_currency(
    client: TestClient,
):
    employee_id = create_employee(
        client,
        employee_code="SALARY_CURRENCY_001",
        email="salary.currency@example.com",
    )

    response = client.post(
        f"/api/v1/employees/{employee_id}/salaries",
        json=salary_payload(
            currency="US",
        ),
    )

    assert response.status_code == 422

    data = response.json()

    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_create_salary_invalid_period(
    client: TestClient,
):
    employee_id = create_employee(
        client,
        employee_code="SALARY_PERIOD_001",
        email="salary.period@example.com",
    )

    response = client.post(
        f"/api/v1/employees/{employee_id}/salaries",
        json=salary_payload(
            effective_from="2026-06-01",
            effective_to="2026-05-01",
        ),
    )

    assert response.status_code == 422

    data = response.json()

    assert data["error"]["code"] == "INVALID_SALARY_PERIOD"
    assert data["error"]["message"] == (
         "effective_to cannot be before effective_from"
    )


def test_get_employee_salaries(
    client: TestClient,
):
    employee_id = create_employee(
        client,
        employee_code="SALARY_LIST_001",
        email="salary.list@example.com",
    )

    create_salary(
        client,
        employee_id,
    )

    response = client.get(
        f"/api/v1/employees/{employee_id}/salaries",
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["employee_id"] == employee_id
    assert data[0]["currency"] == "USD"


def test_get_latest_salary(
    client: TestClient,
):
    employee_id = create_employee(
        client,
        employee_code="SALARY_LATEST_001",
        email="salary.latest@example.com",
    )

    create_salary(
        client,
        employee_id,
        salary_payload(
            base_salary="70000.00",
            effective_from="2025-01-01",
        ),
    )

    latest_salary = create_salary(
        client,
        employee_id,
        salary_payload(
            base_salary="80000.00",
            effective_from="2026-01-01",
        ),
    )

    response = client.get(
        f"/api/v1/employees/{employee_id}/salaries/latest",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == latest_salary["id"]
    assert data["base_salary"] == "80000.00"
    assert data["effective_from"] == "2026-01-01"


def test_get_latest_salary_not_found(
    client: TestClient,
):
    employee_id = create_employee(
        client,
        employee_code="SALARY_NO_LATEST_001",
        email="salary.no.latest@example.com",
    )

    response = client.get(
        f"/api/v1/employees/{employee_id}/salaries/latest",
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Salary record not found"


def test_get_salary_by_id(
    client: TestClient,
):
    employee_id = create_employee(
        client,
        employee_code="SALARY_GET_ID_001",
        email="salary.get.id@example.com",
    )

    salary = create_salary(
        client,
        employee_id,
    )

    response = client.get(
        f"/api/v1/salaries/{salary['id']}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == salary["id"]
    assert data["employee_id"] == employee_id


def test_get_salary_not_found(
    client: TestClient,
):
    response = client.get(
        "/api/v1/salaries/999999999",
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Salary record not found"


def test_update_salary(
    client: TestClient,
):
    employee_id = create_employee(
        client,
        employee_code="SALARY_UPDATE_001",
        email="salary.update@example.com",
    )

    salary = create_salary(
        client,
        employee_id,
    )

    response = client.put(
        f"/api/v1/salaries/{salary['id']}",
        json=salary_payload(
            base_salary="90000.00",
            bonus="10000.00",
            currency="EUR",
            effective_from="2026-02-01",
            effective_to="2026-12-31",
        ),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == salary["id"]
    assert data["base_salary"] == "90000.00"
    assert data["bonus"] == "10000.00"
    assert data["currency"] == "EUR"
    assert data["effective_from"] == "2026-02-01"
    assert data["effective_to"] == "2026-12-31"


def test_update_salary_not_found(
      client: TestClient,
):

      response = client.put(
              "/api/v1/salaries/999999999",
              json=salary_payload(
                     base_salary="90000.00",
              ),
      )

      assert response.status_code == 404

      data = response.json()

      assert data["detail"] == "Salary record not found"

def test_delete_salary(
       client: TestClient,
):
       employee_id = create_employee(
              client,
              employee_code="SALARY_DELETE_001",
              email="salary.delete@example.com",
       )

       salary = create_salary(
               client,
               employee_id,
       )

       response = client.delete(
            f"/api/v1/salaries/{salary['id']}",
       )

       assert response.status_code == 204

       get_response = client.get(
               f"/api/v1/salaries/{salary['id']}",
       )

       assert get_response.status_code == 404

def test_delete_salary_not_found(
       client: TestClient,
):

       response = client.delete(
             "/api/v1/salaries/999999999",
       )

       assert response.status_code == 404

       data = response.json()

       assert data["detail"] == "Salary record not found"
