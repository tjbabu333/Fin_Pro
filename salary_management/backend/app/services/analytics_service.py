from app.repositories.analytics_repository import (
    AnalyticsRepository,
)


class AnalyticsService:
    def __init__(self, repository: AnalyticsRepository):
        self.repository = repository

    def get_analytics(self) -> dict:
        department_rows = (
            self.repository.get_department_analytics()
        )

        departments = [
            {
                "department": department.department or "Unassigned",
                "employee_count": department.employee_count,
                "average_salary": float(
                    department.average_salary or 0
                ),
                "total_salary": float(
                    department.total_salary or 0
                ),
            }
            for department in department_rows
        ]

        return {
            "summary": {
                "total_employees": (
                    self.repository.get_total_employees()
                ),
                "total_salary_records": (
                    self.repository.get_total_salary_records()
                ),
                "total_base_salary": (
                    self.repository.get_total_base_salary()
                ),
                "total_bonus": (
                    self.repository.get_total_bonus()
                ),
                "average_salary": (
                    self.repository.get_average_salary()
                ),
            },
            "departments": departments,
        }