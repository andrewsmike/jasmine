"""Create initial schema.

Revision ID: 564a9e076693
Revises: 
Create Date: 2021-09-10 00:03:46.417048

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "564a9e076693"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "organizations",
        sa.Column("organization_id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint("organization_id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "backends",
        sa.Column("backend_id", sa.BigInteger(), nullable=False),
        sa.Column("organization_id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.organization_id"],
            name="backend_organization",
        ),
        sa.PrimaryKeyConstraint("backend_id"),
        sa.UniqueConstraint("organization_id", "name"),
    )
    op.create_table(
        "teams",
        sa.Column("team_id", sa.BigInteger(), nullable=False),
        sa.Column("team_name", sa.String(length=64), nullable=False),
        sa.Column("organization_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.organization_id"],
            name="team_organization",
        ),
        sa.PrimaryKeyConstraint("team_id"),
    )
    op.create_index(
        "org_team_name", "teams", ["organization_id", "team_name"], unique=False
    )
    op.create_index("team_name", "teams", ["team_name"], unique=False)
    op.create_table(
        "users",
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("organization_id", sa.BigInteger(), nullable=False),
        sa.Column("email", sa.String(length=96), nullable=False),
        sa.Column("name", sa.String(length=96), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.organization_id"],
            name="user_organization",
        ),
        sa.PrimaryKeyConstraint("user_id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index("org_email", "users", ["organization_id", "email"], unique=False)
    op.create_index("org_name", "users", ["organization_id", "name"], unique=False)
    op.create_table(
        "projects",
        sa.Column("project_id", sa.BigInteger(), nullable=False),
        sa.Column("organization_id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("backend_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["backend_id"], ["backends.backend_id"], name="project_backend"
        ),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.organization_id"],
            name="project_organization",
        ),
        sa.PrimaryKeyConstraint("project_id"),
        sa.UniqueConstraint("organization_id", "name"),
    )
    op.create_index("backend", "projects", ["backend_id"], unique=False)
    op.create_table(
        "team_memberships",
        sa.Column("team_id", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(["team_id"], ["teams.team_id"], name="membership_team"),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"], name="membership_user"),
        sa.PrimaryKeyConstraint("team_id", "user_id"),
    )
    op.create_index("user_teams", "team_memberships", ["user_id"], unique=False)
    op.create_table(
        "queries",
        sa.Column("query_id", sa.BigInteger(), nullable=False),
        sa.Column("project_id", sa.BigInteger(), nullable=False),
        sa.Column("path", sa.String(length=256), nullable=False),
        sa.Column("query_text", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.project_id"],
        ),
        sa.PrimaryKeyConstraint("query_id"),
        sa.UniqueConstraint("project_id", "path"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("queries")
    op.drop_index("user_teams", table_name="team_memberships")
    op.drop_table("team_memberships")
    op.drop_index("backend", table_name="projects")
    op.drop_table("projects")
    op.drop_index("org_name", table_name="users")
    op.drop_index("org_email", table_name="users")
    op.drop_table("users")
    op.drop_index("team_name", table_name="teams")
    op.drop_index("org_team_name", table_name="teams")
    op.drop_table("teams")
    op.drop_table("backends")
    op.drop_table("organizations")
    # ### end Alembic commands ###