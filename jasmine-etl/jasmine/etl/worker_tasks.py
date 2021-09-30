from functools import wraps

from sqlalchemy import inspect

from jasmine.etl.app import celery_app
from jasmine.etl.app_base import app_db_engine_session, timed_lock
from jasmine.etl.backends import new_backend_conn
from jasmine.models import View, orm_registry


def with_sqla_session(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        engine, session = app_db_engine_session(orm_registry)

        try:
            result = func(session, *args, **kwargs)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise e

    return wrapped


def with_sqla_first_arg(sqla_class):
    def decorator(func):
        @wraps(func)
        def wrapped_func(session, ident, *args, **kwargs):
            sqla_object = session.query(sqla_class).get(ident)

            return func(session, sqla_object, *args, **kwargs)

        return wrapped_func

    return decorator


def sqla_timed_lock(task_timeout, lock_suffix=None):
    def decorator(func):
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

            with timed_lock(*key, task_timeout=task_timeout) as lock:
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


@celery_app.task
def foo(a, b):
    print(a, b)
    return a + b


MINUTES = 60
HOURS = 60 * MINUTES


@celery_app.task
@with_sqla_session
@with_sqla_first_arg(View)
@sqla_timed_lock(task_timeout=5 * MINUTES, lock_suffix="result_preview")
def view_result_preview(session, view, timed_lock=None):
    with new_backend_conn(view.project.backend) as conn:
        conn.execute(view.spec["query_text"])
        return conn.fetchall()


celery_app.control.time_limit(
    "jasmine.etl.worker_tasks.view_result_preview",
    soft=4 * MINUTES,
    hard=5 * MINUTES,
    reply=True,
)
