import random
import sys
from pathlib import Path

from sqlalchemy import insert

# Allow imports from the backend directory
BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

TOTAL_EMPLOYEES = 10_000
BATCH_SIZE = 1_000


FIRST_NAMES = [
    "John",
    "Robert",
    "Michael",
    "David",
    "James",
    "William",
    "Daniel",
    "Matthew",
    "Chris",
    "Andrew",
]

LAST_NAMES = [
    "Smith",
    "Johnson",
    "Brown",
    "Wilson",
    "Taylor",
    "Anderson",
    "Thomas",
    "Jackson",
    "White",
    "Harris",
]

COUNTRIES = [
    "USA",
    "India",
    "UK",
    "Canada",
    "Germany",
    "Australia",
]

DEPARTMENTS = [
    "Engineering",
    "Finance",
    "Human Resources",
    "Sales",
    "Marketing",
    "Operations",
    "IT",
]

JOB_TITLES = [
    "Python Developer",
    "Senior Python Developer",
    "Backend Developer",
    "Software Engineer",
    "Senior Software Engineer",
    "Data Engineer",
    "DevOps Engineer",
    "Technical Lead",
]


def generate_employees(start_number: int, count: int):
    employees = []

    for number in range(
        start_number,
        start_number + count,
    ):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)

        employee_code = f"SEED{number:05d}"
        email = (
            f"{first_name.lower()}."
            f"{last_name.lower()}."
            f"{number}@example.com"
        )

        employee = {
            "employee_code": employee_code,
            "full_name": f"{first_name} {last_name}",
            "email": email,
            "country": random.choice(COUNTRIES),
            "department": random.choice(DEPARTMENTS),
            "job_title": random.choice(JOB_TITLES),
            "status": random.choice(
                ["ACTIVE", "INACTIVE"]
            ),
        }

        employees.append(employee)

    return employees


def seed_employees():
    from app.db.database import engine
    from app.db.models.employee import Employee

    print(
        f"Seeding {TOTAL_EMPLOYEES} employees..."
    )

    with engine.begin() as connection:
        for start in range(
            1,
            TOTAL_EMPLOYEES + 1,
            BATCH_SIZE,
        ):
            employees = generate_employees(
                start,
                min(
                    BATCH_SIZE,
                    TOTAL_EMPLOYEES - start + 1,
                ),
            )

            connection.execute(
                insert(Employee),
                employees,
            )

            print(
                f"Inserted through "
                f"{start + len(employees) - 1}"
            )

    print(
        f"Successfully inserted "
        f"{TOTAL_EMPLOYEES} employees."
    )


if __name__ == "__main__":
    seed_employees()
