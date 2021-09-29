"""Reorder/rename columns for consistency.

Revision ID: d3b9889927f0
Revises: 564a9e076693
Create Date: 2021-09-10 10:42:40.798737

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
import sqlalchemy.dialects.mysql as mysql

# revision identifiers, used by Alembic.
revision = "d3b9889927f0"
down_revision = "564a9e076693"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "teams",
        "team_name",
        new_column_name="name",
        existing_type=mysql.VARCHAR(length=64),
        existing_nullability=False,
    )


def downgrade():
    op.alter_column(
        "teams",
        "name",
        new_column_name="team_name",
        existing_type=mysql.VARCHAR(length=64),
        existing_nullability=False,
    )
