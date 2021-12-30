from functools import wraps
from logging import exception

from sqlalchemy import inspect

from jasmine.etl.app import celery_app
from jasmine.etl.app_base import app_db_session, timed_lock
from jasmine.etl.backends import backend_conn
from jasmine.etl.materializations import materialization_event_funcs
from jasmine.models import Materialization, View, orm_registry

MINUTES = 60
HOURS = 60 * MINUTES


def with_sqla_session(func):
    """
    Inject a SQLAlchemy session object as the first argument to the function.
    """

    @wraps(func)
    def wrapped(*args, **kwargs):
        with app_db_session(orm_registry) as session:
            return func(session, *args, **kwargs)

    return wrapped


def with_sqla_first_arg(sqla_class):
    """
    For functions structured as `handle_sqla_object(session, object_pk_id, ...)`,
    replace object_pk_id with a loaded SQLAlchemy object.

    Primary key tuples may or may not be supported; check SQLAlchemy's session.get
    arguments.
    """

    def decorator(func):
        @wraps(func)
        def wrapped_func(session, ident, *args, **kwargs):
            sqla_object = session.query(sqla_class).get(ident)

            return func(session, sqla_object, *args, **kwargs)

        return wrapped_func

    return decorator


def sqla_timed_lock(
    soft_timeout=4 * MINUTES,
    hard_timeout=5 * MINUTES,
    lock_suffix=None,
):
    def decorator(func):
        celery_app.control.time_limit(
            f"{func.__module__}.{func.__name__}",
            soft=soft_timeout,
            hard=hard_timeout,
            reply=True,
        )

        @wraps(func)
        def wrapped(session, sqla_object, *args, **kwargs):
            if lock_suffix:
                key_suffix = [lock_suffix]
            else:
                key_suffix = []

            key = [
                sqla_object.__class__.__name__,
                str(inspect(sqla_object).identity),
            ] + key_suffix

            with timed_lock(key, task_timeout=hard_timeout + 30) as lock:
                return func(session, sqla_object, *args, timed_lock=lock, **kwargs)

        return wrapped

    return decorator


"""
def backend_event_from_sqla_obj(sqla_object, **kwargs):

def log_backend_event(title: str):
    def decorator(func):
        @wraps(func)
        def wrapped_func(session, sqla_object, *arg, **kwargs):
            backend_event = backend_event_from_sqla_obj(sqla_object, title=title)
            session.add(backend_event)
            try:
                start_time = time()
                return func(session, sql_object, *args, **kwargs)
            finally:
                session.add(backend_event)
@log_backend_event("Preview view data.")
"""


# TODO: These locking semantics are dreadfully wrong. Restart from scratch.
@celery_app.task
@with_sqla_session
@with_sqla_first_arg(View)
# @sqla_timed_lock(
#     soft_timeout=4 * MINUTES,
#     hard_timeout=5 * MINUTES,
#     lock_suffix="result_preview",
# )
def view_result_preview(session, view):  # timed_lock=None
    with backend_conn(view.project.backend, readonly=True) as ro_conn:
        ro_conn.execute(view.spec["query_text"])
        return ro_conn.fetchall()


# TODO: These locking semantics are dreadfully wrong. Restart from scratch.
@celery_app.task
@with_sqla_session
@with_sqla_first_arg(Materialization)
# @sqla_timed_lock(
#     soft_timeout=4 * MINUTES,
#     hard_timeout=5 * MINUTES,
#     lock_suffix="run_event",
# )
def execute_materialization_event(
    session, materialization, event_name  # , timed_lock=None
):
    assert event_name in materialization.state_machine_type.state_events.get(
        materialization.state, set()
    ), f"Cannot '{event_name}' a[n] '{materialization.state}' {type(materialization).__name__}."

    event_func = materialization_event_funcs[materialization.materialization_name][
        event_name
    ]

    next_state = event_func(materialization, session)

    materialization.state = next_state


@celery_app.task
@with_sqla_session
@with_sqla_first_arg(Materialization)
def execute_materialization_event_or_cleanup(
    session,
    mat,
    expected_start_state: str,
    event: str,
    cleanup_action_event: str | None = "terminate",
):

    if mat.state == expected_start_state:
        try:
            execute_materialization_event(mat.materialization_id, event)
            return
        except Exception as e:
            initial_error = e
    else:
        initial_error = AssertionError(
            f"Materialization state was {mat.state}, expected {expected_start_state}."
        )

    if not mat.terminal() and cleanup_action_event is not None:
        try:
            execute_materialization_event(mat.materialization_id, cleanup_action_event)
        except Exception as cleanup_exception:
            exception(cleanup_exception)

    raise initial_error


def execute_materialization_events(
    materialization_id: int,
    expected_state_names: list[str],
    event_names: list[str],
    onfail_action_event: str | None = "terminate",
    sync: bool = True,
):
    promise = execute_materialization_event_or_cleanup.starmap(
        [
            (materialization_id, expected_state_name, event_name, onfail_action_event)
            for expected_state_name, event_name in zip(
                expected_state_names, event_names
            )
        ]
    )
    if sync:
        promise.delay().get()
    else:
        promise.apply_async()
