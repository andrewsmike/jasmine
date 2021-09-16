from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKeyConstraint,
    Index,
    PrimaryKeyConstraint,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from jasmine.webserver.models.model_registry import orm_registry


@orm_registry.mapped
class Backend:
    __tablename__ = "backends"

    backend_id = Column(BigInteger, nullable=False)
    name = Column(String(length=64), nullable=False)
    organization_id = Column(BigInteger, nullable=False)
    # TODO: What specifies a backend?

    __table_args__ = (
        PrimaryKeyConstraint("backend_id"),
        UniqueConstraint("organization_id", "name"),
        ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.organization_id"],
            "backend_organization",
        ),
    )

    organization = relationship("Organization", backref="backends")


@orm_registry.mapped
class Project:
    __tablename__ = "projects"

    project_id = Column(BigInteger, nullable=False)
    name = Column(String(length=64), nullable=False)
    backend_id = Column(BigInteger, nullable=False)
    organization_id = Column(BigInteger, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("project_id"),
        UniqueConstraint("organization_id", "name"),
        Index("backend", "backend_id"),
        ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.organization_id"],
            "project_organization",
        ),
        ForeignKeyConstraint(
            ["backend_id"], ["backends.backend_id"], "project_backend"
        ),
    )

    organization = relationship("Organization", backref="projects")
    backend = relationship("Backend", backref="projects")


@orm_registry.mapped
class Query:
    __tablename__ = "queries"

    query_id = Column(BigInteger, nullable=False)

    query_text = Column(Text, nullable=False)

    # Everything starts as 'scratch/2021-09-01 baby avocado'
    # or maybe 'scratch/2021-09-01 43252352'.
    # All renames must move query out of scratch.
    path = Column(String(256), nullable=False)
    project_id = Column(BigInteger, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("query_id"),
        UniqueConstraint("project_id", "path"),
        ForeignKeyConstraint(["project_id"], ["projects.project_id"]),
    )

    project = relationship("Project", backref="queries")


"""
# TBD
MaterializationType = Enum("view")

@orm_registry.mapped
class Materialization:
    __tablename__ = "materializations"

    query_id = Column(BigInteger, nullable=False)
    materialization_type = Column(MaterializationType, nullable=False)
    status =  Column(String, nullable=False)

    config = Column(Text, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("query_id", "materialization_type"),
        ForeignKeyConstraint(["project_id"], ["projects.project_id"]),
    )

    project = relationship("Project", backref="queries")

"""
