from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.employee import (EmployeeCreate, EmployeeUpdate, EmployeeResponse)
from app.services.employee_service import EmployeeService

from app.core.exceptions import EmployeeNotFoundError



router = APIRouter(
    prefix="/api/v1/employees",
    tags=["Employees"]
)


@router.post("", response_model=EmployeeResponse)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    service = EmployeeService(db)
    return service.create_employee(employee)


@router.get("", response_model=list[EmployeeResponse])
def get_employee(
    db: Session = Depends(get_db)
):
    service = EmployeeService(db)
    return service.get_employees()


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    service = EmployeeService(db)

    employee = service.get_employee(employee_id)

    if not employee:
        raise EmployeeNotFoundError()

    return employee


@router.patch("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db)
):
    service = EmployeeService(db)

    updated_employee = service.update_employee(
        employee_id,
        employee
    )

    if not updated_employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return updated_employee

