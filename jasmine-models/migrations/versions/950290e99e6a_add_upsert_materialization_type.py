"""Add upsert materialization type.

Revision ID: 950290e99e6a
Revises: 4b6f23a3b894
Create Date: 2022-01-05 11:50:52.894137

"""
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "950290e99e6a"
down_revision = "4b6f23a3b894"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "materializations",
        "materialization_type",
        existing_type=mysql.ENUM("view", "history_table"),
        nullable=False,
        type_=mysql.ENUM("view", "history_table", "upsert"),
    )


def downgrade():
    op.alter_column(
        "materializations",
        "materialization_type",
        existing_type=mysql.ENUM("view", "history_table", "upsert"),
        nullable=False,
        type_=mysql.ENUM("view", "history_table"),
    )
