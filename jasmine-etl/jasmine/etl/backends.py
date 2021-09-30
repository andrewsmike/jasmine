from contextlib import contextmanager

from pymysql import connect
from pymysql.cursors import DictCursor

from jasmine.models import Backend


@contextmanager
def new_backend_conn(backend: Backend):
    # pymysql type stubs are incomplete - they don't capture the contextmanager API
    # specifically documented in the examples: https://pymysql.readthedocs.io/en/latest/user/examples.html
    with connect(
        cursorclass=DictCursor, **backend.spec["connection_args"]
    ) as conn:  # type: ignore
        try:
            with conn.cursor() as cursor:
                yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
