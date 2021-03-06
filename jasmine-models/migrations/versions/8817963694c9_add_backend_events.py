"""Add backend events.

Revision ID: 8817963694c9
Revises: 5fecf4bf9ca5
Create Date: 2021-09-29 00:54:28.675928

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8817963694c9"
down_revision = "5fecf4bf9ca5"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "backend_events",
        sa.Column("backend_event_id", sa.BigInteger(), nullable=False),
        sa.Column("title", sa.String(length=256), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_time", sa.DateTime(), nullable=False),
        sa.Column("materialization_id", sa.BigInteger(), nullable=True),
        sa.Column("view_id", sa.BigInteger(), nullable=True),
        sa.Column("project_id", sa.BigInteger(), nullable=True),
        sa.Column("backend_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["backend_id"], ["backends.backend_id"], name="backend_event_backend"
        ),
        sa.ForeignKeyConstraint(
            ["project_id"], ["projects.project_id"], name="project_event_view"
        ),
        sa.ForeignKeyConstraint(
            ["view_id"], ["views.view_id"], name="backend_event_view"
        ),
        sa.PrimaryKeyConstraint("backend_event_id"),
    )
    op.create_index("created_time", "backend_events", ["created_time"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("created_time", table_name="backend_events")
    op.drop_table("backend_events")
    # ### end Alembic commands ###
