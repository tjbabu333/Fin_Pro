from sqlalchemy.orm import Session

from app.db.models import Employee
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.employee import EmployeeCreate, EmployeeUpdate

from app.core.exceptions import EmployeeNotFoundError

from app.core.exceptions import EmployeeAlreadyExistsError

import logging

logger = logging.getLogger("app.employee")

class EmployeeService:

    def __init__(self, db: Session):
        self.repository = EmployeeRepository(db)
        self.db = db

    def create_employee(
        self,
        data: EmployeeCreate,
    ) -> Employee:

        logger.info(
            "Creating employee |  employee_code=%s",
            data.employee_code
        )
    
        existing_code = self.repository.get_by_employee_code(
            data.employee_code
        )

        if existing_code:
            logger.warning(
              "Employee creation failed | duplicate employee_code=%s",
              data.employee_code,
            )
            raise EmployeeAlreadyExistsError("Employee code already exists")

        existing_email = self.repository.get_by_email(
            data.email
        )

        if existing_email:
            raise EmployeeAlreadyExistsError("Employee email already exists")

        employee = Employee(
            employee_code=data.employee_code,
            full_name=data.full_name,
            email=data.email,
            country=data.country,
            department=data.department,
            job_title=data.job_title,
            status=data.status,
        )

        return self.repository.create(employee)

    def get_employees(self):
        return self.repository.get_all()

    def get_employee(self, employee_id: int):
        return self.repository.get_by_id(employee_id)

    def update_employee(
        self,
        employee_id: int,
        data: EmployeeUpdate,
    ):
        employee = self.repository.get_by_id(employee_id)

        if not employee:
            raise EmployeeNotFoundError()
        
        return employee

        if data.full_name is not None:
            employee.full_name = data.full_name

        if data.email is not None:
            employee.email = data.email

        if data.country is not None:
            employee.country = data.country

        if data.department is not None:
            employee.department = data.department

        if data.job_title is not None:
            employee.job_title = data.job_title

        if data.status is not None:
            employee.status = data.status

        return self.repository.update(employee)