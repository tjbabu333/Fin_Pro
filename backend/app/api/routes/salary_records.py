from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.salary import SalaryResponse, SalaryUpdate
from app.services.salary_service import SalaryService


router = APIRouter(
    prefix="/api/v1/salaries",
    tags=["Salaries"],
)


# ---------------------------------------------------------
# GET SALARY BY ID
# ---------------------------------------------------------

@router.get(
    "/{salary_id}",
    response_model=SalaryResponse,
)
def get_salary(
    salary_id: int,
    db: Session = Depends(get_db),
):
    service = SalaryService(db)

    salary = service.get_salary(salary_id)

    if not salary:
        raise HTTPException(
            status_code=404,
            detail="Salary record not found",
        )

    return salary


# ---------------------------------------------------------
# UPDATE SALARY
# ---------------------------------------------------------

@router.put(
    "/{salary_id}",
    response_model=SalaryResponse,
)
def update_salary(
    salary_id: int,
    salary_data: SalaryUpdate,
    db: Session = Depends(get_db),
):
    service = SalaryService(db)

    updated_salary = service.update_salary(
        salary_id,
        salary_data,
    )

    if not updated_salary:
        raise HTTPException(
            status_code=404,
            detail="Salary record not found",
        )

    db.commit()
    db.refresh(updated_salary)

    return updated_salary

@router.delete( 
        "/{salary_id}",  
        status_code=status.HTTP_204_NO_CONTENT, 
) 
def delete_salary( 
       salary_id: int, 
       db: Session = Depends(get_db), 
): 
       service = SalaryService(db) 

       deleted = service.delete_salary(salary_id) 

       if not deleted: 
             raise HTTPException( 
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail="Salary record not found", 
             ) 

       db.commit() 

       return None

