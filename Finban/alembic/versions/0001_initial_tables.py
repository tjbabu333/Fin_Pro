"""initial tables

Revision ID: 0001
Revises:
Create Date: 2026-09-07
"""

import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "entity_state",
        sa.Column("entity_type", sa.String(64), primary_key=True),
        sa.Column("entity_id", sa.String(128), primary_key=True),
        sa.Column("current_state", sa.String(64), nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
    )

    op.create_table(
        "state_change",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("entity_type", sa.String(64), nullable=False),
        sa.Column("entity_id", sa.String(128), nullable=False),
        sa.Column("old_state", sa.String(64), nullable=True),
        sa.Column("new_state", sa.String(64), nullable=False),
        sa.Column("source_system", sa.String(64), nullable=False),
        sa.Column("source_event_id", sa.String(128), nullable=False),
        sa.Column("rule_id", sa.String(64), nullable=False),
        sa.Column("occurred_at", sa.DateTime, nullable=False),
    )

    op.create_table(
        "processed_event",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("system", sa.String(64), nullable=False),
        sa.Column("external_id", sa.String(128), nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
        sa.Column("processed_at", sa.DateTime, nullable=False),
        sa.UniqueConstraint("system", "external_id", "updated_at", name="uq_processed_event"),
    )


def downgrade() -> None:
    op.drop_table("processed_event")
    op.drop_table("state_change")
    op.drop_table("entity_state")
