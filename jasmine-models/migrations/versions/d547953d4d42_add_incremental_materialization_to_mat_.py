"""Add incremental materialization to mat_type_name enum.

Revision ID: d547953d4d42
Revises: d5c799b43657
Create Date: 2022-01-15 11:30:41.226731

"""
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "d547953d4d42"
down_revision = "d5c799b43657"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "materializations",
        "materialization_type",
        existing_type=mysql.ENUM("view", "history_table", "upsert", "reload"),
        nullable=False,
        type_=mysql.ENUM("view", "history_table", "upsert", "reload", "incremental"),
    )


def downgrade():
    op.alter_column(
        "materializations",
        "materialization_type",
        existing_type=mysql.ENUM(
            "view", "history_table", "upsert", "reload", "incremental"
        ),
        nullable=False,
        type_=mysql.ENUM("view", "history_table", "upsert", "reload"),
    )
