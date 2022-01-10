from json import loads
from pprint import pprint
from sys import argv
from time import time

from sqlalchemy import text

from jasmine.etl.ddl_tools import names_status_str
from jasmine.etl.materializations import materialization_resource_names_funcs
from jasmine.etl.sqla_tools import with_sqla_first_arg, with_sqla_session
from jasmine.models.materializations import materialization_type, new_materialization
from jasmine.models.project_models import Project, View
from jasmine.models.user_models import Organization

try:
    # This won't work if we're not in a properly configured environment (IE, not in the docker container.)
    # Ignore import error and let the command fail.
    from jasmine.etl.worker_tasks import execute_materialization_event
except Exception as e:

    def execute_materialization_event(*args, **kwargs):
        # Just re-import to throw the same error. Exception clousers are weird.
        from jasmine.etl.worker_tasks import execute_materialization_event

        return execute_materialization_event(*args, **kwargs)


@with_sqla_session
@with_sqla_first_arg(View)
def perform_action(session, view, mat_type, action, config):
    view_mats = [
        mat for mat in view.materializations if mat.materialization_type == mat_type
    ]
    mat = view_mats[0] if view_mats else None

    if action == "init":
        if mat and not mat.terminal():  # If already proposed, terminate and recreate.
            # Avoid locking issues by flushing.
            session.commit()
            execute_materialization_event(
                mat.materialization_id,
                "terminate",
                schedule_next_event=False,
            )
            assert mat.state == "terminated"

        mat = new_materialization(
            view=view,
            mat_type_name=mat_type,
            config=config,
            preexisting_mat=mat,
        )
        session.add(mat)
        session.commit()
        assert mat.state == "proposed"
    else:
        assert mat is not None, f"Materialization doesn't exist, cannot {action} it."
        session.commit()
        execute_materialization_event(
            mat.materialization_id,
            action,
            schedule_next_event=False,
        )
        session.commit()


def print_mat_state(mat):
    print(
        f"[view {mat.view.view_id}, {mat.materialization_type}] {mat.state_machine_type.state_desc[mat.state]}"
    )
    print("Materialization's state:")
    state = {
        "materialization_id": mat.materialization_id,
        "state": mat.state,
        "config": mat.config,
        "context": mat.context,
    }
    pprint(state)
    print()

    resource_names = materialization_resource_names_funcs[mat.materialization_type](mat)
    print("Total resources:")
    pprint(resource_names)
    print()

    backend = mat.view.project.backend
    print("Current resources:")
    print(names_status_str(backend, resource_names))
    print()


@with_sqla_session
@with_sqla_first_arg(View)
def print_mat_type_state(session, view, mat_type):
    view_mats = [
        mat for mat in view.materializations if mat.materialization_type == mat_type
    ]
    mat = view_mats[0] if view_mats else None

    if not mat:
        print(f"[view {view.view_id}] Materialization {mat_type} does not yet exist.")
    else:
        print_mat_state(mat)


def camel_case_progressive_verb(mat_type, action):
    if action == "init":
        return "Initializing"

    progressive_verb = materialization_type[
        mat_type
    ].state_machine_type.event_progressive_verb[action]
    return progressive_verb[0].upper() + progressive_verb[1:]


@with_sqla_session
def display_backend_messages(session, start_time, view_id):
    assert isinstance(view_id, int)
    assert isinstance(start_time, (float, int))
    event_query = f"SELECT title, description FROM backend_events WHERE view_id = {view_id} AND created_time >= FROM_UNIXTIME({start_time})"
    events = session.execute(text(event_query)).fetchall()
    if events:
        print("Backend events:")
    for title, desc in events:
        print(f"{title}:\n{desc}\n")


@with_sqla_session
def resolved_view_id(session, view_id_str: str):
    try:
        return int(view_id_str)
    except Exception as e:
        pass

    assert ":" in view_id_str, "Format: <view_id> | org_name:[project]/path/to/query"
    org_name, project_view_path = view_id_str.split(":", maxsplit=1)
    bracketed_project_name, view_path = project_view_path.split("/", maxsplit=1)
    project_name = bracketed_project_name[1:-1]

    return (
        (
            session.query(View)
            .join(View.project)
            .join(Project.organization)
            .where(Organization.name == org_name)
            .where(Project.name == project_name)
            .where(View.path == view_path)
        )
        .one()
        .view_id
    )


def step_materialization():
    assert len(argv) in (
        4,
        5,
    ), f"Usage: {argv[0]} (<view_id> | org_name:[project]/path/to/view) <mat_type> <action1,action2,...> [config]?"
    view_id, mat_type, actions, *rest = argv[1:]

    view_id = resolved_view_id(view_id)

    if rest:
        config = loads(rest[0])
    else:
        config = None

    print_mat_type_state(view_id, mat_type)
    for action in actions.split(","):
        print(
            f"{camel_case_progressive_verb(mat_type, action)} view {view_id}'s {mat_type} materialization."
        )
        start_time = time()
        perform_action(view_id, mat_type, action, config=config)
        display_backend_messages(start_time, view_id)
        print_mat_type_state(view_id, mat_type)
