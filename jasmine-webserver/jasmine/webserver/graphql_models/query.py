from functools import wraps
from typing import Optional

from ariadne import ObjectType
from jasmine.sql.pretty_print import pretty_printed_sql_str

from jasmine.webserver.app_base import app_db_engine_session
from jasmine.webserver.models import (
    Backend,
    Organization,
    Project,
    Query,
    Team,
    User,
    orm_registry,
)

query_type_defs = """
scalar JSON

type Query {
    "Defaults to current user's organization."
    organization(id: ID): Organization!

    "Defaults to current user."
    user(id: ID): User!

    team(id: ID!): Team!
    backend(id: ID!): Backend!
    project(id: ID!): Project!

    sql_query(id: ID!): SqlQuery!

    "Defaults to the current organization."
    sql_query_from_path(
        project_name: String!,
        query_path: String!,
        organization_id: ID
    ): SqlQuery!

"Get an autoformatted version of the given SQL query."
formatted_query_text(query_text: String!): String!
}
"""
query_obj = ObjectType("Query")


def with_sqla_session(func):
    @wraps(func)
    def wrapped(obj, info, *args, **kwargs):
        engine, session = app_db_engine_session(orm_registry)

        try:
            result = func(session, obj, info, *args, **kwargs)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise e

    return wrapped


@query_obj.field("organization")
@with_sqla_session
def resolve_organization(session, obj, info, id: Optional[int] = None) -> Organization:
    assert id is not None
    return session.query(Organization).where(Organization.organization_id == id).first()


@query_obj.field("user")
@with_sqla_session
def resolve_user(session, obj, info, id: Optional[int] = None) -> User:
    assert id is not None
    return session.query(User).where(User.user_id == id).first()


@query_obj.field("team")
@with_sqla_session
def resolve_team(session, obj, info, id: int) -> Team:
    return session.query(Team).where(Team.team_id == id).first()


@query_obj.field("backend")
@with_sqla_session
def resolve_backend(session, obj, info, id: int) -> Backend:
    return session.query(Backend).where(Backend.backend_id == id).first()


@query_obj.field("project")
@with_sqla_session
def resolve_project(session, obj, info, id: int) -> Project:
    return session.query(Project).where(Project.project_id == id).first()


@query_obj.field("sql_query")
@with_sqla_session
def resolve_sql_query(session, obj, info, id: int) -> Query:
    return session.query(Query).where(Query.query_id == id).first()


@query_obj.field("sql_query_from_path")
@with_sqla_session
def resolve_sql_query_from_path(
    session,
    obj,
    info,
    project_name: str,
    query_path: str,
    organization_id: Optional[int],
) -> Query:
    assert organization_id is not None
    return (
        session.query(Query)
        .join(Query.project)
        .where(Project.name == project_name)
        .where(Project.organization_id == int(organization_id))
        .where(Query.path == query_path)
    ).first()


@query_obj.field("formatted_query_text")
@with_sqla_session
def formatted_query_text(session, obj, info, query_text: str):
    try:
        query_text = pretty_printed_sql_str(query_text)
    except Exception as e:
        query_text = f"/* Could not format query: {e}. */\n" + query_text

    return query_text
