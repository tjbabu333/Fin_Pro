from sqlalchemy import func, or_, select
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
    
    def get_all(self) -> list[Employee]:
           statement = select(Employee).order_by(Employee.id)
           return list(self.db.scalars(statement).all())

    def create(self, employee: Employee) -> Employee:
        self.db.add(employee)
        self.db.flush()
        self.db.refresh(employee)
        
        return employee

    def update(self, employee: Employee) -> Employee:
           self.db.flush()
           self.db.refresh(employee)

           return employee

        