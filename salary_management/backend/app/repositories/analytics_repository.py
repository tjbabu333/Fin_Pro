from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models.employee import Employee
from app.db.models.salary_record import SalaryRecord


class AnalyticsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_total_employees(self) -> int:
        return (
            self.db.query(func.count(Employee.id))
            .scalar()
            or 0
        )

    def get_total_salary_records(self) -> int:
        return (
            self.db.query(func.count(SalaryRecord.id))
            .scalar()
            or 0
        )

    def get_total_base_salary(self) -> float:
        result = (
            self.db.query(
                func.coalesce(
                    func.sum(SalaryRecord.base_salary),
                    0,
                )
            )
            .scalar()
        )

        return float(result or 0)

    def get_total_bonus(self) -> float:
        result = (
            self.db.query(
                func.coalesce(
                    func.sum(SalaryRecord.bonus),
                    0,
                )
            )
            .scalar()
        )

        return float(result or 0)

    def get_average_salary(self) -> float:
        result = (
            self.db.query(
                func.coalesce(
                    func.avg(SalaryRecord.base_salary),
                    0,
                )
            )
            .scalar()
        )

        return float(result or 0)

    def get_department_analytics(self):
        return (
            self.db.query(
                Employee.department,
                func.count(
                    func.distinct(Employee.id)
                ).label("employee_count"),
                func.coalesce(
                    func.avg(SalaryRecord.base_salary),
                    0,
                ).label("average_salary"),
                func.coalesce(
                    func.sum(SalaryRecord.base_salary),
                    0,
                ).label("total_salary"),
            )
            .outerjoin(
                SalaryRecord,
                SalaryRecord.employee_id == Employee.id,
            )
            .group_by(Employee.department)
            .order_by(Employee.department)
            .all()
        )