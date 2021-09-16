from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKeyConstraint,
    Index,
    PrimaryKeyConstraint,
    String,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from jasmine.webserver.models.model_registry import orm_registry

@orm_registry.mapped
class Organization:
    __tablename__ = "organizations"

    organization_id = Column(BigInteger, nullable=False)
    name = Column(String(length=64), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("organization_id"),
        UniqueConstraint("name"),
    )


@orm_registry.mapped
class User:
    __tablename__ = "users"

    user_id = Column(BigInteger, nullable=False)
    email = Column(String(length=96), nullable=False)
    name = Column(String(length=96), nullable=False)
    default_project_id = Column(BigInteger, nullable=True)
    organization_id = Column(BigInteger, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("user_id"),
        Index("org_email", "organization_id", "email"),
        Index("org_name", "organization_id", "name"),
        UniqueConstraint("email"),
        ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.organization_id"],
            name="user_organization",
        ),
        ForeignKeyConstraint(
            ["default_project_id"],
            ["projects.project_id"],
            name="user_default_project",
        ),
    )

    organization = relationship("Organization", backref="users")
    default_project = relationship("User", backref="users_using_as_default")


team_membership = Table(
    "team_memberships",
    orm_registry.metadata,
    Column("team_id", BigInteger, nullable=False),
    Column("user_id", BigInteger, nullable=False),
    PrimaryKeyConstraint("team_id", "user_id"),
    Index("user_teams", "user_id"),
    ForeignKeyConstraint(
        ["team_id"],
        ["teams.team_id"],
        name="membership_team",
    ),
    ForeignKeyConstraint(
        ["user_id"],
        ["users.user_id"],
        name="membership_user",
    ),
)


@orm_registry.mapped
class Team:
    __tablename__ = "teams"

    team_id = Column(BigInteger, nullable=False)
    name = Column(String(length=64), nullable=False)
    organization_id = Column(BigInteger, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("team_id"),
        Index("org_team_name", "organization_id", "name"),
        Index("team_name", "name"),
        ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.organization_id"],
            name="team_organization",
        ),
    )

    organization = relationship("Organization", backref="teams")
    members = relationship("User", secondary=team_membership, backref="teams")
