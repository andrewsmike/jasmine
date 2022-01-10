"""Add reload materialization.

Revision ID: 1a665a343d3e
Revises: 950290e99e6a
Create Date: 2022-01-09 19:18:06.620399

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "1a665a343d3e"
down_revision = "950290e99e6a"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "materializations",
        "materialization_type",
        existing_type=mysql.ENUM("view", "history_table", "upsert"),
        nullable=False,
        type_=mysql.ENUM("view", "history_table", "upsert", "reload"),
    )


def downgrade():
    op.alter_column(
        "materializations",
        "materialization_type",
        existing_type=mysql.ENUM("view", "history_table", "upsert", "reload"),
        nullable=False,
        type_=mysql.ENUM("view", "history_table", "upsert"),
    )
