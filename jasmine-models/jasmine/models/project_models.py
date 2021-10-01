from sqlalchemy import (
    JSON,
    BigInteger,
    Column,
    DateTime,
    Enum,
    ForeignKeyConstraint,
    Index,
    PrimaryKeyConstraint,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from jasmine.models.model_registry import orm_registry


@orm_registry.mapped
class Backend:
    __tablename__ = "backends"

    backend_id = Column(BigInteger, nullable=False)
    name = Column(String(length=64), nullable=False)

    backend_type = Column(Enum("mysql"), nullable=False)
    spec = Column(JSON, nullable=False)

    organization_id = Column(BigInteger, nullable=False)

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
class View:
    __tablename__ = "views"

    view_id = Column(BigInteger, nullable=False)

    view_type = Column(Enum("query"), nullable=False)

    spec = Column(JSON, nullable=False)

    # Everything starts as '[proj]/scratch/baby_avocado'
    path = Column(String(256), nullable=False)
    project_id = Column(BigInteger, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("view_id"),
        UniqueConstraint("project_id", "path"),
        ForeignKeyConstraint(["project_id"], ["projects.project_id"], "view_project"),
    )

    project = relationship("Project", backref="views")


"""
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


@orm_registry.mapped
class BackendEvent:
    __tablename__ = "backend_events"

    backend_event_id = Column(BigInteger, nullable=False)
    title = Column(String(length=256), nullable=False)
    description = Column(Text, nullable=True)

    created_time = Column(DateTime, nullable=False)

    materialization_id = Column(BigInteger, nullable=True)
    view_id = Column(BigInteger, nullable=True)
    project_id = Column(BigInteger, nullable=True)
    backend_id = Column(BigInteger, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("backend_event_id"),
        Index("created_time", "created_time"),
        ForeignKeyConstraint(
            ["backend_id"],
            ["backends.backend_id"],
            "backend_event_backend",
        ),
        ForeignKeyConstraint(
            ["project_id"],
            ["projects.project_id"],
            "project_event_view",
        ),
        ForeignKeyConstraint(
            ["view_id"],
            ["views.view_id"],
            "backend_event_view",
        ),
    )

    backend = relationship("Backend", backref="backend_events")
    project = relationship("Project", backref="backend_events")
    view = relationship("View", backref="backend_events")