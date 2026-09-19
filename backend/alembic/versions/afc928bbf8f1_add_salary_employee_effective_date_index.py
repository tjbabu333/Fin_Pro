"""add salary employee effective date index

Revision ID: afc928bbf8f1
Revises: 82e6c8c36049
Create Date: 2026-09-18
"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "afc928bbf8f1"
down_revision: str | Sequence[str] | None = "82e6c8c36049"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_index(
        "ix_salary_records_employee_effective_from",
        "salary_records",
        ["employee_id", "effective_from"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        "ix_salary_records_employee_effective_from",
        table_name="salary_records",
    )
