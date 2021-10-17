from functools import wraps
from typing import Optional

from ariadne import ObjectType

from jasmine.etl.worker_tasks import view_result_preview
from jasmine.models import Project, User, View
from jasmine.webserver.graphql_models.query import with_sqla_session
from jasmine.webserver.random_phrase import random_hex, random_phrase

mutation_type_defs = """
interface OperationResult {
    success: Boolean!
    error: String
}

type DeleteResult implements OperationResult {
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
type ViewResult implements OperationResult {
    success: Boolean!
    error: String
    result: View
}

type DataResult implements OperationResult {
    success: Boolean!
    error: String
    result: JSON
}

type Mutation {
    delete_organization(id: ID!): DeleteResult!
    update_organization_name(id: ID!, newName: String!): OrganizationResult!

    delete_user(id: ID!): DeleteResult!
    change_user_email(id: ID!, new_email: String!): UserResult!
    update_user_name(id: ID!, new_name: String!): UserResult!
    update_user_default_project(id: ID!, project_id: ID!): UserResult!

    create_team(organization_id: ID!, name: String!): TeamResult!
    delete_team(id: ID!): DeleteResult!
    update_team_name(id: ID!, new_name: String!): TeamResult!

    add_team_member(team_id: ID!, user_id: ID!): TeamResult!
    remove_team_member(team_id: ID!, user_id: ID!): TeamResult!

    create_backend(organization_id: ID!, name: String!): BackendResult!
    delete_backend(id: ID!): DeleteResult!
    update_backend_name(id: ID!, new_name: String!): BackendResult!

    create_project(organization_id: ID!, name: String!, backend_id: ID!): ProjectResult!
    delete_project(id: ID!): DeleteResult!
    update_project_name(id: ID!, new_name: String!): ProjectResult!

    create_query(project_id: ID, path: String, query_text: String): ViewResult!
    update_query_text(id: ID!, query_text: String!): ViewResult!

    move_view(id: ID!, project_name: String, view_path: String): ViewResult!
    update_view_path(id: ID!, path: String!): ViewResult!
    delete_view(id: ID!): DeleteResult!

    preview_view_result(id: ID!): DataResult!
}
"""
mutation_obj = ObjectType("Mutation")

MAX_ATTEMPTS = 64


def random_view_path(project: Project):
    paths = {view.path for view in project.views}

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
) -> View:
    # Temporary.
    user = session.query(User).where(User.user_id == 1).one()

    assert (
        user.default_project_id is not None
    ), "User must have default project configured."

    if path is None:
        path = random_view_path(user.default_project)

    if query_text is None:
        query_text = ""

    assert path is not None  # For MyPy.
    assert query_text is not None  # For MyPy.

    query = View(
        project_id=user.default_project_id,
        view_type="query",
        path=path,
        spec={"query_text": query_text, "view_type": "query"},
    )

    session.add(query)

    return query


@mutation_obj.field("update_query_text")
@as_wrapped_graphql_payload
@with_sqla_session
def update_query_text(
    session, obj, info, id: Optional[int] = None, query_text: Optional[str] = None
) -> View:
    assert query_text is not None
    assert len(query_text) < 2 ** 16, "Query text must be < 65536 characters."

    view = session.query(View).where(View.view_id == id).one()

    assert view.view_type == "query"
    query = view

    new_spec = dict(query.spec)
    new_spec["query_text"] = query_text
    query.spec = new_spec

    return query


@mutation_obj.field("delete_view")
@as_wrapped_graphql_payload
@with_sqla_session
def delete_view(
    session,
    obj,
    info,
    id: int = None,
):
    session.delete(session.query(View).where(View.view_id == id).one())


@mutation_obj.field("move_view")
@as_wrapped_graphql_payload
@with_sqla_session
def move_view(
    session,
    obj,
    info,
    id: int,
    project_name: Optional[str] = None,
    view_path: Optional[str] = None,
) -> View:
    view = session.query(View).where(View.view_id == id).one()

    if project_name is not None:
        project = session.query(Project).where(Project.name == project_name).one()
        view.project = project

    if view_path is not None:
        view.path = view_path

    return view


@mutation_obj.field("preview_view_result")
@as_wrapped_graphql_payload
@with_sqla_session
def preview_view_result(
    session,
    obj,
    info,
    id: int = None,
):
    task = view_result_preview.delay(id)
    return task.get(timeout=10)
