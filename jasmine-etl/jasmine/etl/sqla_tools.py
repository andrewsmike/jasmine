from functools import wraps

from jasmine.etl.app_base import app_db_session
from jasmine.models import orm_registry


def with_sqla_session(func):
    """
    Inject a SQLAlchemy session object as the first argument to the function.

    See jasmine.sql.worker_tasks for example usages.
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

    See jasmine.sql.worker_tasks for example usages.
    """

    def decorator(func):
        @wraps(func)
        def wrapped_func(session, ident, *args, **kwargs):
            sqla_object = session.query(sqla_class).get(ident)

            return func(session, sqla_object, *args, **kwargs)

        return wrapped_func

    return decorator
