from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.exceptions import EmployeeNotFoundError
from app.db.session import get_db
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeListResponse,
    EmployeeResponse,
    EmployeeUpdate,
)
from app.services.employee_service import EmployeeService

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


@router.get("", response_model=EmployeeListResponse)
def get_employees(
     page: int = Query(1, ge=1),
     page_size: int = Query(20, ge=1, le=100),
     search: str | None = Query(None),
    db: Session = Depends(get_db)
):
    service = EmployeeService(db)

    employees, total = service.get_employees(
          page=page,
          page_size=page_size,
          search=search,
    )
    return {
          "items": employees,
          "page" : page,
          "page_size": page_size,
          "total": total,
    }

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

