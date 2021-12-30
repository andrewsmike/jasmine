from contextlib import contextmanager
from functools import wraps
from traceback import format_exc

from jasmine.etl.app_base import app_db_session
from jasmine.etl.ddl_tools import ResourceNames
from jasmine.models import orm_registry
from jasmine.models.materializations import Materialization
from jasmine.models.project_models import BackendEvent


# TODO: Connection caching semantics.
def log_backend_event(
    title: str,
    description: str,
    materialization=None,
    view=None,
    project=None,
    backend=None,
):
    mat_id = view_id = project_id = backend_id = None

    if materialization is not None:
        materialization_id = materialization.materialization_id
        view = view or materialization.view

    if view is not None:
        view_id = view.view_id
        project = project or view.project

    if project is not None:
        project_id = project.project_id
        backend = backend or project.backend

    if backend is not None:
        backend_id = backend.backend_id

    with app_db_session(orm_registry) as session:
        log_event = BackendEvent(
            title=title,
            description=description,
            materialization=materialization,
            view=view,
            project=project,
            backend=backend,
        )

        session.add(log_event)
        session.commit()


def attempt_log_backend_event(*args, **kwargs):
    return log_backend_event(*args, **kwargs)


def set_state_on_exception(failure_state: str, error_types: tuple[Exception]):
    def wrapper(func):
        @wraps(func)
        def wrapped(materialization, session, *args, **kwargs):
            assert (
                failure_state in materialization.state_machine_type.states
            ), f"Failure state {failure_state} not valid for materialization type {type(materialization).__name__}"
            # TODO: Testing
            try:
                return func(materialization, session, *args, **kwargs)
            except error_types as e:
                attempt_log_backend_event(
                    title="Materialization event failed",
                    description=(
                        f"Failed to run; Entering {failure_state}.\n"
                        + f"Reason: {e}\n"
                        + f"{format_exc()}"
                    ),
                    materialization=materialization,
                )

                return failure_state

        return wrapped

    return wrapper


@contextmanager
def edit_resources(mat: Materialization):
    resources = ResourceNames.from_materialization(mat)
    yield resources
    mat.context["claimed_resources"] = resources.to_dict()
