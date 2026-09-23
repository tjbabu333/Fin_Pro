from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class SalaryCreate(BaseModel):
    base_salary: Decimal = Field(ge=0)
    bonus: Decimal = Field(default=Decimal("0.00"), ge=0)
    currency: str = Field(min_length=3, max_length=3)
    effective_from: date
    effective_to: date | None = None


class SalaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_id: int
    base_salary: Decimal
    bonus: Decimal
    currency: str
    effective_from: date
    effective_to: date | None

class SalaryUpdate(BaseModel):
    base_salary: Decimal = Field(ge=0)
    bonus: Decimal = Field(default=Decimal("0.00"), ge=0)
    currency: str = Field(min_length=3, max_length=3)
    effective_from: date
    effective_to: date | None = None