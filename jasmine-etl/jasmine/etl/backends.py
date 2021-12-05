from collections.abc import Generator
from contextlib import contextmanager
from functools import cache
from os.path import exists, join
from tempfile import TemporaryDirectory

from pymysql import connect
from pymysql.cursors import DictCursor
from sqlalchemy import create_engine, inspect, text

from jasmine.etl.app_base import sqla_uri_from_config_section
from jasmine.models import Backend
from jasmine.sql.analysis import is_readonly_query
from jasmine.sql.table_spec import TableSpec


class ReadOnlyDictCursor(DictCursor):
    def execute(self, query, args=None):
        assert is_readonly_query(
            query
        ), f"Attempted to run mutating or combined statement using readonly DictCursor. Query:\n{query}"

        return super().execute(query, args=args)


@contextmanager
def new_backend_conn(backend: Backend, readonly: bool = False):
    assert (
        backend.backend_type == "mysql"
    ), "Only MySQL backends are currently supported."

    cursor = ReadOnlyDictCursor if readonly else DictCursor

    # MyPy override: pymysql type stubs are incomplete - they don't capture the contextmanager API
    # specifically documented in the examples: https://pymysql.readthedocs.io/en/latest/user/examples.html
    with connect(
        cursorclass=cursor, **backend.spec["connection_args"]
    ) as conn:  # type: ignore
        try:
            with conn.cursor() as cursor:
                yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
