from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import SalaryRecord


class SalaryRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, salary: SalaryRecord) -> SalaryRecord:
        self.db.add(salary)
        self.db.flush()
        self.db.refresh(salary)

        return salary

    def get_by_id(
        self,
        salary_id: int,
    ) -> SalaryRecord | None:

        return self.db.get(SalaryRecord, salary_id)

    def get_by_employee_id(
        self,
        employee_id: int,
    ) -> list[SalaryRecord]:

        statement = (
            select(SalaryRecord)
            .where(SalaryRecord.employee_id == employee_id)
            .order_by(SalaryRecord.effective_from.desc())
        )

        return list(self.db.scalars(statement).all())

    def get_latest_by_employee_id(
        self,
        employee_id: int,
    ) -> SalaryRecord | None:

        statement = (
            select(SalaryRecord)
            .where(SalaryRecord.employee_id == employee_id)
            .order_by(SalaryRecord.effective_from.desc())
            .limit(1)
        )

        return self.db.scalar(statement)

    def update(
           self,
           salary: SalaryRecord,
    ) -> SalaryRecord:

           self.db.flush()
           self.db.refresh(salary)

           return salary

    def delete( 
           self, 
           salary: SalaryRecord, 
    ) -> None: 

           self.db.delete(salary) 

