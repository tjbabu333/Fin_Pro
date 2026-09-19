from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models import Employee


class EmployeeRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, employee_id: int) -> Employee | None:
        return self.db.get(Employee, employee_id)

    def get_by_employee_code(
        self,
        employee_code: str,
    ) -> Employee | None:
        statement = select(Employee).where(
            Employee.employee_code == employee_code
        )

        return self.db.scalar(statement)

    def get_by_email(
        self,
        email: str,
    ) -> Employee | None:
        statement = select(Employee).where(
            Employee.email == email
        )

        return self.db.scalar(statement)

    def get_all(
        self,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
    ) -> tuple[list[Employee], int]:
        statement = select(Employee)

        if search:
            search_value = f"%{search.strip()}%"

            statement = statement.where(
                (Employee.employee_code.ilike(search_value))
                | (Employee.full_name.ilike(search_value))
                | (Employee.email.ilike(search_value))
                | (Employee.country.ilike(search_value))
                | (Employee.department.ilike(search_value))
                | (Employee.job_title.ilike(search_value))
            )

        count_statement = select(
            func.count()
        ).select_from(
            statement.subquery()
        )

        total = self.db.scalar(count_statement) or 0

        statement = (
            statement
            .order_by(Employee.id)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        employees = list(
            self.db.scalars(statement).all()
        )

        return employees, total

    def create(self, employee: Employee) -> Employee:
        self.db.add(employee)
        self.db.flush()
        self.db.refresh(employee)

        return employee

    def update(self, employee: Employee) -> Employee:
        self.db.flush()
        self.db.refresh(employee)

        return employee

