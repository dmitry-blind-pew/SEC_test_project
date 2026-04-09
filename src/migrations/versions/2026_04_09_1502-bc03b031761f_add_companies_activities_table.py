"""add companies_activities table

Revision ID: bc03b031761f
Revises: 1255c4a4ed9b
Create Date: 2026-04-09 15:02:02.217515

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "bc03b031761f"
down_revision: Union[str, Sequence[str], None] = "1255c4a4ed9b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "companies_activities",
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("activity_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["companies.id"],
            name=op.f("fk_companies_activities_company_id_companies"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["activity_id"],
            ["activities.id"],
            name=op.f("fk_companies_activities_activity_id_activities"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "company_id",
            "activity_id",
            name=op.f("pk_companies_activities"),
        ),
    )
def downgrade() -> None:
    op.drop_table("companies_activities")
