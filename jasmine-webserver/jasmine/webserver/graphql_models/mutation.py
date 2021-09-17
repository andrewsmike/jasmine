from functools import wraps
from typing import Optional

from ariadne import ObjectType

from jasmine.webserver.graphql_models.query import with_sqla_session
from jasmine.webserver.models import Project, Query, User
from jasmine.webserver.random_phrase import random_hex, random_phrase

mutation_type_defs = """
interface OperationResult {
    success: Boolean!
    error: String
}

type OrganizationResult implements OperationResult {
    success: Boolean!
    error: String
    result: Organization
}
type UserResult implements OperationResult {
    success: Boolean!
    error: String
    result: User
}
type TeamResult implements OperationResult {
    success: Boolean!
    error: String
    result: Team
}
type BackendResult implements OperationResult {
    success: Boolean!
    error: String
    result: Backend
}
type ProjectResult implements OperationResult {
    success: Boolean!
    error: String
    result: Project
}
type SqlQueryResult implements OperationResult {
    success: Boolean!
    error: String
    result: SqlQuery
}

type Mutation {
    delete_organization(id: ID!): OrganizationResult!
    update_organization_name(id: ID!, newName: String!): OrganizationResult!

    delete_user(id: ID!): UserResult!
    change_user_email(id: ID!, new_email: String!): UserResult!
    update_user_name(id: ID!, new_name: String!): UserResult!
    update_user_default_project(id: ID!, project_id: ID!): UserResult!

    create_team(organization_id: ID!, name: String!): TeamResult!
    delete_team(id: ID!): TeamResult!
    update_team_name(id: ID!, new_name: String!): TeamResult!

    add_team_member(team_id: ID!, user_id: ID!): TeamResult!
    remove_team_member(team_id: ID!, user_id: ID!): TeamResult!

    create_backend(organization_id: ID!, name: String!): BackendResult!
    delete_backend(id: ID!): BackendResult!
    update_backend_name(id: ID!, new_name: String!): BackendResult!

    create_project(organization_id: ID!, name: String!, backend_id: ID!): ProjectResult!
    delete_project(id: ID!): ProjectResult!
    update_project_name(id: ID!, new_name: String!): ProjectResult!

    create_query(project_id: ID, path: String, query_text: String): SqlQueryResult!
    delete_query(id: ID!): SqlQueryResult!
    update_query_path(id: ID!, path: String!): SqlQueryResult!
    update_query_text(id: ID!, query_text: String!): SqlQueryResult!
    copy_query(id: ID!, new_path: String): SqlQueryResult!
}
"""
mutation_obj = ObjectType("Mutation")

MAX_ATTEMPTS = 64


def random_query_path(project: Project):
    paths = {query.path for query in project.queries}

    for i in range(MAX_ATTEMPTS):
        random_path = f"scratch/{random_phrase(short=True)}_{random_hex(4)}"
        if random_path not in paths:
            return random_path
    else:
        raise RuntimeError(
            "Too many scratch queries; retry or clear scratch/ directory."
        )


def as_wrapped_graphql_payload(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return {
                "success": True,
                "error": None,
                "result": func(*args, **kwargs),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "result": None,
            }

    return wrapper


@mutation_obj.field("create_query")
@as_wrapped_graphql_payload
@with_sqla_session
def create_query(
    session,
    obj,
    info,
    project_id: Optional[int] = None,
    path: Optional[str] = None,
    query_text: Optional[str] = None,
):
    # Temporary.
    user = session.query(User).where(User.user_id == 1).first()

    assert (
        user.default_project_id is not None
    ), "User must have default project configured."

    if path is None:
        path = random_query_path(user.default_project)

    if query_text is None:
        query_text = ""

    assert path is not None  # For MyPy.
    assert query_text is not None  # For MyPy.

    query = Query(
        project_id=user.default_project_id,
        query_text=query_text,
        path=path,
    )

    session.add(query)

    return query


@mutation_obj.field("update_query_text")
@as_wrapped_graphql_payload
@with_sqla_session
def update_query_text(
    session, obj, info, id: Optional[int] = None, query_text: Optional[str] = None
) -> Query:
    assert query_text is not None
    assert len(query_text) < 2 ** 16, "Query text must be < 65536 characters."

    query = session.query(Query).where(Query.query_id == id).first()
    query.query_text = query_text

    return query
