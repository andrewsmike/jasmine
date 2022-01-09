from collections.abc import Generator
from contextlib import contextmanager
from functools import cache, partial
from os import getpid
from os.path import exists, join
from socket import gethostname
from tempfile import TemporaryDirectory

from pymysql import connect
from pymysql.cursors import DictCursor
from sqlalchemy import create_engine, inspect, text

from jasmine.etl.app_base import sqla_uri_from_config_section
from jasmine.models import Backend
from jasmine.sql.analysis import is_readonly_query
from jasmine.sql.table_spec import TableSpec
from jasmine.sql.transforms.escaping import escaped, unescaped


class DebuggingDictCursor(DictCursor):
    def __init__(self, *args, backend=None, debug=False, **kwargs):
        self.backend = backend
        self.debug = debug
        super().__init__(*args, **kwargs)

    def execute(self, query, args=None):
        if self.debug:
            org_name = self.backend.organization.name
            backend_name = (
                f"{org_name}.{self.backend.name}(backend_id={self.backend.backend_id})"
            )
            context_str = f"/* Jasmine@{gethostname()}(pid={getpid()}): {self.backend.backend_id} */\n"
        else:
            context_str = ""

        return super().execute(context_str + query, args=args)


class ReadOnlyDictCursor(DebuggingDictCursor):
    def execute(self, query, args=None):
        assert is_readonly_query(
            query
        ), f"Attempted to run mutating or combined statement using readonly DictCursor. Query:\n{query}"

        return super().execute(query, args=args)


@contextmanager
def backend_conn(backend: Backend, readonly: bool = False):
    "Direct driver connection to a given backend."

    assert (
        backend.backend_type == "mysql"
    ), "Only MySQL backends are currently supported."

    cursor = partial(
        ReadOnlyDictCursor if readonly else DebuggingDictCursor,
        backend=backend,
        debug=False,
    )

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

    assert conn._closed


@cache
def backend_engine(backend: Backend):
    return create_engine(
        url=sqla_uri_from_config_section(
            backend.spec["connection_args"],
        ),
        echo=False,
    )


def backend_inspector(backend: Backend):
    return inspect(backend_engine(backend))


def mock_backend(sqla_uri: str) -> Backend:
    return Backend(spec={"connection_args": {"uri": sqla_uri}}, backend_type="mysql")


@contextmanager
def tmp_mock_sqla_backend(
    init_statements: list[str],
) -> Generator[Backend, None, None]:
    """
    Provide a temporary sqlalchemy-accessible database and mock Backend using SQLite
    with optional initialization logic.
    Use this to test your backend and sqlalchemy based methods.

    NOTE: The sqlite database will always be named "main".

    NOTE: new_backend_conn will not work here, as it provides a pymysql connection, rather than
        a sqlalchemy connection. Only useful for testing new_backend_engine/sqlalchemy based logic.

    See jasmine.etl.schema.table_column_infos for examples of how to use this to test methods.
    """
    with TemporaryDirectory() as temp_dir_path:
        db_path = join(temp_dir_path, "pytest_db.sqlite")
        sqlite_uri = f"sqlite:///{db_path}"

        engine = backend_engine(mock_backend(sqlite_uri))
        with engine.connect() as conn:
            for init_statement in init_statements:
                conn.execute(text(init_statement))

        assert exists(db_path)

        yield mock_backend(sqlite_uri)


example_create_sqlite_schema_statements = [
    """
    CREATE TABLE main.`users " ` (
      `user_id` BIGINT AUTO_INCREMENT NOT NULL,
      `name` varchar(96) NOT NULL,
      `parent_user_id` bigint DEFAULT NULL,
      PRIMARY KEY (`user_id`),
      UNIQUE (`name`),
      UNIQUE (`parent_user_id`),
      CONSTRAINT `parent_user_id` FOREIGN KEY (`parent_user_id`) REFERENCES `users \\" ` (`user_id`)
    );
    """,
    'CREATE INDEX `org_name` ON `users " ` (`parent_user_id`,`name`);',
]


# TODO: proper caching.
@cache
def backend_table_spec(backend: Backend, db_name: str, table_name: str) -> TableSpec:
    """
    >>> from jasmine.etl.backends import example_create_sqlite_schema_statements, tmp_mock_sqla_backend
    >>> from pprint import pprint

    >>> with tmp_mock_sqla_backend(example_create_sqlite_schema_statements) as backend:
    ...     pprint(backend_table_spec(backend, "main", '`users " `'))
    TableSpec(column_names=['user_id', 'name', 'parent_user_id'],
              column_type_decls={'name': 'VARCHAR(96) NOT NULL',
                                 'parent_user_id': 'BIGINT',
                                 'user_id': 'INTEGER NOT NULL'},
              primary_key=['user_id'],
              indices={'org_name': ['parent_user_id', 'name']},
              unique_indices={'unique_key_0': ['name'],
                              'unique_key_1': ['parent_user_id']},
              foreign_keys=[ForeignKey(name=None,
                                       dest_db_name='main',
                                       dest_table_name='users \\\\" ',
                                       source_columns=['parent_user_id'],
                                       dest_columns=['user_id'])])
    """
    return TableSpec.from_sqla_inspector(
        backend_inspector(backend), unescaped(db_name), unescaped(table_name)
    )


def table_exists(backend: Backend, db_name: str, table_name: str) -> bool:
    """
    >>> from jasmine.etl.backends import example_create_sqlite_schema_statements, tmp_mock_sqla_backend
    >>> from pprint import pprint

    >>> create_view_statement = 'CREATE VIEW `view " ` AS SELECT 1;'
    >>> with tmp_mock_sqla_backend(example_create_sqlite_schema_statements + [create_view_statement]) as backend:
    ...     pprint(table_exists(backend, "main", '`users " `'))
    ...     pprint(table_exists(backend, "main", 'users'))
    ...     pprint(table_exists(backend, "main", 'view " '))
    True
    False
    False
    """
    return backend_inspector(backend).has_table(
        unescaped(table_name), schema=unescaped(db_name)
    ) and not view_exists(backend, db_name, table_name)


def view_exists(backend: Backend, db_name: str, view_name: str) -> bool:
    """
    >>> from jasmine.etl.backends import example_create_sqlite_schema_statements, tmp_mock_sqla_backend
    >>> from pprint import pprint

    >>> create_view_statement = 'CREATE VIEW `bleh " ` AS SELECT 1;'
    >>> with tmp_mock_sqla_backend(example_create_sqlite_schema_statements + [create_view_statement]) as backend:
    ...     pprint(view_exists(backend, "main", '`bleh " `'))
    ...     pprint(view_exists(backend, "main", 'bleh'))
    True
    False
    """
    return unescaped(view_name) in backend_inspector(backend).get_view_names(
        unescaped(db_name)
    )


def create_view_statement(backend: Backend, db_name: str, view_name: str) -> str:
    """
    Note: Engines may "mangle", reformat, and restructure the original view queries.
    Apparently SQLite is rather unimaginative and saves the raw string.

    >>> from jasmine.etl.backends import example_create_sqlite_schema_statements, tmp_mock_sqla_backend
    >>> from pprint import pprint

    >>> create_view = 'CREATE VIEW `bleh " ` AS SELECT 1;'
    >>> with tmp_mock_sqla_backend(example_create_sqlite_schema_statements + [create_view]) as backend:
    ...     print(create_view_statement(backend, "main", '`bleh " `'))
    CREATE VIEW `bleh " ` AS SELECT 1
    """
    return backend_inspector(backend).get_view_definition(
        unescaped(view_name), schema=unescaped(db_name)
    )


def table_view_exists(*args, **kwargs) -> bool:
    return table_exists(*args, **kwargs) or view_exists(*args, **kwargs)


def trigger_exists_with_pattern(
    backend: Backend, db_name: str, trigger_pattern: str
) -> bool:
    assert isinstance(trigger_pattern, str)

    with backend_engine(backend).connect() as conn:
        conn.execute(
            text(f"SHOW TRIGGERS IN {escaped(db_name)} LIKE %s;", trigger_pattern)
        )

        return conn.fetchone() is not None
