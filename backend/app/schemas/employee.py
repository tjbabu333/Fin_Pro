from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


EmployeeStatus = Literal["ACTIVE", "INACTIVE"]


class EmployeeCreate(BaseModel):
    employee_code: str = Field(min_length=1, max_length=50)
    full_name: str = Field(min_length=1, max_length=150)
    email: EmailStr
    country: str = Field(min_length=1, max_length=100)
    department: str = Field(min_length=1, max_length=100)
    job_title: str = Field(min_length=1, max_length=150)
    status: EmployeeStatus = "ACTIVE"


class EmployeeUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=150)
    email: EmailStr | None = None
    country: str | None = Field(default=None, min_length=1, max_length=100)
    department: str | None = Field(default=None, min_length=1, max_length=100)
    job_title: str | None = Field(default=None, min_length=1, max_length=150)
    status: EmployeeStatus | None = None


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_code: str
    full_name: str
    email: str
    country: str
    department: str
    job_title: str
    status: EmployeeStatus