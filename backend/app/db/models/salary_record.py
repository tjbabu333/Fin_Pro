from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class SalaryRecord(Base):
    __tablename__ = "salary_records"

    id: Mapped[int] = mapped_column(primary_key=True)

    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id"),
        nullable=False,
        index=True,
    )

    base_salary: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    bonus: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
        default=Decimal("0.00"),
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        index=True,
    )

    effective_from: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    effective_to: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    employee = relationship(
        "Employee",
        back_populates="salary_records",
    )