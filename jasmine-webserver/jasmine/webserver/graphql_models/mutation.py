from functools import wraps
from logging import exception
from typing import Optional

from ariadne import ObjectType

from jasmine.etl.worker_tasks import (
    execute_materialization_event,
    execute_materialization_events,
    schedule_materialization,
    view_result_preview,
)
from jasmine.models import Materialization, Project, User, View, new_materialization
from jasmine.models.materializations.base import (
    history_table_preferred_materialization_order,
)
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
type MaterializationResult implements OperationResult {
    success: Boolean!
    error: String
    result: Materialization
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

    create_history_table(project_id: ID, source_view_id: ID, source_db_name: String, source_table_name: String): ViewResult!

    move_view(id: ID!, project_name: String, view_path: String): ViewResult!
    update_view_path(id: ID!, path: String!): ViewResult!
    delete_view(id: ID!, force_no_cleanup: Boolean): DeleteResult!

    preview_view_result(id: ID!): DataResult!

    create_materialization(view_id: ID!, materialization_type: MaterializationType, config: JSON): MaterializationResult!
    terminate_materialization(materialization_id: ID!): DeleteResult!
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


def history_table_path(project: Project, db_name: str, table_name: str) -> str:
    paths = {view.path for view in project.views}

    base = table_name + "_history"
    if base not in paths:
        return base

    for i in range(MAX_ATTEMPTS):
        if f"{base}_{i+1}" not in paths:
            return f"{base}_{i+1}"
    else:
        raise RuntimeError(
            "Too many history tables with same name to create a new one. They can be reused!"
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
            exception(str(e))
            return {
                "success": False,
                "error": str(e),
                "result": None,
            }

    return wrapper


def active_materializations(view):
    return [mat for mat in view.materializations if not mat.terminal()]


def create_view_materialization(session, query, mat_type="view", config=None):

    preexisting_mats = [
        mat for mat in query.materializations if mat.materialization_type == mat_type
    ]

    assert (
        len(preexisting_mats) <= 1
    ), f"Multiple {mat_type} materializations per view is not currently supported."
    preexisting_mat = (preexisting_mats + [None])[0]

    mat = new_materialization(
        view=query,
        mat_type_name=mat_type,
        config=config or {},
        preexisting_mat=preexisting_mat,
    )
    session.add(mat)

    session.commit()

    result = execute_materialization_events(
        mat.materialization_id,
        ["proposed", "accepted"],
        ["verify", "create"],
        sync=True,
    )

    # The RPC has made our transaction state stale. Refresh by rolling back.
    session.rollback()


def terminate_view_materialization(session, query, mat_type="view"):
    preexisting_mats = [
        mat
        for mat in query.materializations
        if mat.materialization_type == mat_type
        if not mat.terminal()
    ]

    if not preexisting_mats:
        return

    assert (
        len(preexisting_mats) == 1
    ), f"Multiple {mat_type} materializations per view is not currently supported."
    (preexisting_mat,) = preexisting_mats

    execute_materialization_event.delay(
        preexisting_mat.materialization_id, "terminate"
    ).get()

    # The RPC has made our transaction state stale. Refresh by rolling back.
    session.rollback()
    session.expire_all()


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
    session.commit()

    try:
        create_view_materialization(session, query)
    except Exception as e:
        pass

    return query


def best_history_table_base_mat(source_view: View) -> Materialization:
    mats = active_materializations(source_view)
    assert (
        mats
    ), "Source view doesn't have any materializations to attach history table to."

    for mat_type in history_table_preferred_materialization_order:
        mats_of_type = [mat for mat in mats if mat.materialization_type == mat_type]
        if mats_of_type:
            assert (
                len(mats_of_type) == 1
            ), "Cannot choose between multiple materializations of the same type."
            (mat,) = mats_of_type
            return mat
    else:
        raise ValueError(
            "Cannot create a history table for a non-concrete materialization type."
        )


@mutation_obj.field("create_history_table")
@as_wrapped_graphql_payload
@with_sqla_session
def create_history_table(
    session,
    obj,
    info,
    project_id: int | None = None,
    source_view_id: int | None = None,
    source_db_name: str = "",
    source_table_name: str = "",
) -> View:
    assert source_view_id != (
        source_db_name and source_table_name
    ), "History tables need either a source view or a database/table."

    # Temporary.
    user = session.query(User).where(User.user_id == 1).one()

    assert (
        user.default_project_id is not None
    ), "User must have default project configured."

    if source_view_id is not None:
        source_view = session.query(View).where(View.view_id == source_view_id).one()

        mat = best_history_table_base_mat(source_view)

        source_db_name, source_table_name = mat.db_name, mat.table_name

    assert source_db_name is not None and source_table_name is not None

    path = history_table_path(user.default_project, source_db_name, source_table_name)

    history_table = View(
        project_id=user.default_project_id,
        view_type="history_table",
        path=path,
        spec={
            "source_db_name": source_db_name,
            "source_table_name": source_table_name,
            "view_type": "history_table",
        },
    )

    session.add(history_table)
    session.commit()

    try:
        create_view_materialization(session, history_table, mat_type="history_table")
    except Exception as e:
        pass

    return history_table


@mutation_obj.field("update_query_text")
@as_wrapped_graphql_payload
@with_sqla_session
def update_query_text(
    session, obj, info, id: Optional[int] = None, query_text: Optional[str] = None
) -> View:
    assert query_text is not None
    assert len(query_text) < 2 ** 16, "Query text must be < 65536 characters."

    view = session.query(View).where(View.view_id == id).one()

    assert (
        view.view_type == "query"
    ), "History tables don't use queries, cannot update_query_text()."
    query = view

    terminate_view_materialization(session, query)

    assert (
        len(active_materializations(query)) == 0
    ), "Cannot update a view with active materializations."

    new_spec = dict(query.spec)
    new_spec["query_text"] = query_text
    query.spec = new_spec

    try:
        create_view_materialization(session, query)
    except Exception as e:
        pass

    return query


@mutation_obj.field("delete_view")
@as_wrapped_graphql_payload
@with_sqla_session
def delete_view(
    session,
    obj,
    info,
    id: int = None,
    force_no_cleanup: bool = False,
):
    view = session.query(View).where(View.view_id == id).one()

    if view.view_type in ("query", "history_table"):
        mat_type = {"query": "view", "history_table": "history_table"}[view.view_type]
        terminate_view_materialization(session, view, mat_type=mat_type)

    assert force_no_cleanup or (
        len(active_materializations(view)) == 0
    ), "Cannot delete a view with active materializations."

    session.delete(view)


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

    if view.view_type == "query":
        terminate_view_materialization(session, view, mat_type="view")
    elif view.view_type == "history_table":
        terminate_view_materialization(session, view, mat_type="history_table")

    assert (
        len(active_materializations(view)) == 0
    ), "Cannot move a view with active materializations."

    if project_name is not None:
        new_project = session.query(Project).where(Project.name == project_name).one()
        view.project = new_project

    if view_path is not None:
        view.path = view_path

    if view.view_type == "query":
        try:
            create_view_materialization(session, view)
        except Exception as e:
            pass
    elif view.view_type == "history_table":
        try:
            create_view_materialization(session, view, mat_type="history_table")
        except Exception as e:
            pass

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


@mutation_obj.field("create_materialization")
@as_wrapped_graphql_payload
@with_sqla_session
def create_materialization(
    session,
    obj,
    info,
    view_id: int,
    materialization_type: str,
    config=None,
) -> Materialization:
    view = session.query(View).where(View.view_id == view_id).one()

    preexisting_mats = (
        session.query(Materialization)
        .where(Materialization.view_id == view_id)
        .where(Materialization.materialization_type == materialization_type)
        .all()
    )
    if preexisting_mats:
        (preexisting_mat,) = preexisting_mats
        assert (
            preexisting_mat.terminal()
        ), f"{materialization_type} materialization already exists!"
    else:
        preexisting_mat = None

    mat = new_materialization(
        view=view,
        mat_type_name=materialization_type,
        config=config or {},
        preexisting_mat=preexisting_mat,
    )

    session.add(mat)

    session.commit()
    schedule_materialization(session, mat)

    return mat


@mutation_obj.field("terminate_materialization")
@as_wrapped_graphql_payload
@with_sqla_session
def terminate_materialization(
    session,
    obj,
    info,
    materialization_id: int,
) -> Materialization:

    # TODO: Locking logic.
    execute_materialization_event.delay(materialization_id, "terminate")

    return None
