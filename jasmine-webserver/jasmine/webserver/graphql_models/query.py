from datetime import datetime
from functools import wraps
import json
from typing import Optional

from ariadne import ObjectType

from jasmine.models import (
    Backend,
    Organization,
    Project,
    Team,
    User,
    View,
    orm_registry,
)
from jasmine.sql.pretty_print import sql_pretty_printed
from jasmine.webserver.app_base import app_db_session

query_type_defs = """
scalar JSON
scalar Date
scalar DateTime

type Query {
    "Defaults to current user's organization."
    organization(id: ID): Organization!

    "Defaults to current user."
    user(id: ID): User!

    team(id: ID!): Team!
    backend(id: ID!): Backend!
    project(id: ID!): Project!

    view(id: ID!): View!
    materialization(id: ID!): Materialization!

    "Defaults to the current organization."
    view_from_path(
        project_name: String!,
        view_path: String!,
        organization_id: ID
    ): View

    "Get an autoformatted version of the given SQL query."
    formatted_query_text(query_text: String!): String!
}
"""
query_obj = ObjectType("Query")


# Datetimes aren't json serializable by default.
# This patch handles datetime when encoding json objects.
def json_datetime_encoder(encoder, obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    else:
        return default_json_encoder(obj)


default_json_encoder = json.JSONEncoder.default
json.JSONEncoder.default = json_datetime_encoder  # type: ignore


def with_sqla_session(func):
    @wraps(func)
    def wrapped(obj, info, *args, **kwargs):
        with app_db_session(orm_registry) as session:
            try:
                return func(session, obj, info, *args, **kwargs)
            except Exception as e:
                session.rollback()
                raise
            finally:
                session.commit()

    return wrapped


@query_obj.field("organization")
@with_sqla_session
def resolve_organization(session, obj, info, id: Optional[int] = None) -> Organization:
    assert id is not None
    return session.query(Organization).where(Organization.organization_id == id).one()


@query_obj.field("user")
@with_sqla_session
def resolve_user(session, obj, info, id: Optional[int] = None) -> User:
    assert id is not None
    return session.query(User).where(User.user_id == id).one()


@query_obj.field("team")
@with_sqla_session
def resolve_team(session, obj, info, id: int) -> Team:
    return session.query(Team).where(Team.team_id == id).one()


@query_obj.field("backend")
@with_sqla_session
def resolve_backend(session, obj, info, id: int) -> Backend:
    return session.query(Backend).where(Backend.backend_id == id).one()


@query_obj.field("project")
@with_sqla_session
def resolve_project(session, obj, info, id: int) -> Project:
    return session.query(Project).where(Project.project_id == id).one()


@query_obj.field("view")
@with_sqla_session
def resolve_view(session, obj, info, id: int) -> View:
    return session.query(View).where(View.view_id == id).one()


@query_obj.field("view_from_path")
@with_sqla_session
def resolve_sql_query_from_path(
    session,
    obj,
    info,
    project_name: str,
    view_path: str,
    organization_id: Optional[int],
) -> Optional[View]:
    assert organization_id is not None
    return (
        session.query(View)
        .join(View.project)
        .where(Project.name == project_name)
        .where(Project.organization_id == int(organization_id))
        .where(View.path == view_path)
    ).one()


@query_obj.field("formatted_query_text")
@with_sqla_session
def formatted_query_text(session, obj, info, query_text: str):
    try:
        query_text = sql_pretty_printed(query_text)
    except Exception as e:
        query_text = f"/* Could not format query: {e}. */\n" + query_text

    return query_text
