"""Add history_table to view_type enum.

Revision ID: d5c799b43657
Revises: 1a665a343d3e
Create Date: 2022-01-12 12:19:25.825690

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "d5c799b43657"
down_revision = "1a665a343d3e"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "views",
        "view_type",
        existing_type=mysql.ENUM("query"),
        nullable=False,
        type_=mysql.ENUM("query", "history_table"),
    )


def downgrade():
    op.alter_column(
        "views",
        "view_type",
        existing_type=mysql.ENUM("query", "history_table"),
        nullable=False,
        type_=mysql.ENUM("query"),
    )
