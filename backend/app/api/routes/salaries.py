from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.salary import (
    SalaryCreate,
    SalaryResponse,
    SalaryUpdate,
)
from app.services.salary_service import SalaryService


router = APIRouter(
    prefix="/api/v1/employees/{employee_id}/salaries",
    tags=["Salaries"],
)


# ---------------------------------------------------------
# CREATE SALARY
# ---------------------------------------------------------

@router.post(
    "",
    response_model=SalaryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_salary(
    employee_id: int,
    salary: SalaryCreate,
    db: Session = Depends(get_db),
):
    service = SalaryService(db)

    created_salary = service.create_salary(
        employee_id,
        salary,
    )

    if not created_salary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    db.commit()
    db.refresh(created_salary)

    return created_salary


# ---------------------------------------------------------
# GET ALL SALARIES FOR EMPLOYEE
# ---------------------------------------------------------

@router.get(
    "",
    response_model=list[SalaryResponse],
)
def get_employee_salaries(
    employee_id: int,
    db: Session = Depends(get_db),
):
    service = SalaryService(db)

    return service.get_employee_salaries(employee_id)


# ---------------------------------------------------------
# GET LATEST SALARY
# ---------------------------------------------------------

@router.get(
    "/latest",
    response_model=SalaryResponse,
)
def get_latest_salary(
    employee_id: int,
    db: Session = Depends(get_db),
):
    service = SalaryService(db)

    salary = service.get_latest_salary(employee_id)

    if not salary:
        raise HTTPException(
            status_code=404,
            detail="Salary record not found",
        )

    return salary

