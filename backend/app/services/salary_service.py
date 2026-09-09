from sqlalchemy.orm import Session

from app.db.models import Employee, SalaryRecord
from app.repositories.salary_repository import SalaryRepository
from app.schemas.salary import SalaryCreate, SalaryUpdate


class SalaryService:

    def __init__(self, db: Session):
        self.repository = SalaryRepository(db)
        self.db = db

    def create_salary(
        self,
        employee_id: int,
        data: SalaryCreate,
    ) -> SalaryRecord | None:

        employee = self.db.get(Employee, employee_id)

        if not employee:
            return None

        if data.base_salary < 0:
            raise ValueError("Base salary cannot be negative")

        if data.bonus < 0:
            raise ValueError("Bonus cannot be negative")

        if (
            data.effective_to is not None
            and data.effective_to < data.effective_from
        ):
            raise ValueError(
                "effective_to cannot be before effective_from"
            )

        salary = SalaryRecord(
            employee_id=employee_id,
            base_salary=data.base_salary,
            bonus=data.bonus,
            currency=data.currency.upper(),
            effective_from=data.effective_from,
            effective_to=data.effective_to,
        )

        return self.repository.create(salary)

    def get_salary(
        self,
        salary_id: int,
    ) -> SalaryRecord | None:

        return self.repository.get_by_id(salary_id)

    def get_employee_salaries(
        self,
        employee_id: int,
    ) -> list[SalaryRecord]:

        return self.repository.get_by_employee_id(employee_id)

    def get_latest_salary(
           self, 
           employee_id: int,
    ) -> SalaryRecord | None:
 
           return self.repository.get_latest_by_employee_id(employee_id)

    def update_salary(
           self,
           salary_id: int,
           data: SalaryUpdate,
    ) -> SalaryRecord | None:

           salary = self.repository.get_by_id(salary_id)

           if not salary:
                return None

           if data.base_salary < 0:
                raise ValueError("Base salary cannot be negative")

           if data.bonus < 0:
                raise ValueError("Bonus cannot be negative")

           if (
                data.effective_to is not None
                and data.effective_to < data.effective_from
           ):
                raise ValueError(
                       "effective_to cannot be before effective_from"
                )
           
           salary.base_salary = data.base_salary
           salary.bonus = data.bonus
           salary.currency = data.currency.upper()
           salary.effective_from = data.effective_from
           salary.effective_to = data.effective_to

           return self.repository.update(salary)

    def delete_salary( 
           self, 
           salary_id: int, 
    ) -> bool: 

           salary = self.repository.get_by_id(salary_id) 

           if not salary: 
                  return False 

           self.repository.delete(salary) 

           return True
