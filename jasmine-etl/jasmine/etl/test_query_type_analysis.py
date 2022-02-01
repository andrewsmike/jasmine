from pprint import pformat

from jasmine.etl.app_base import app_db_session
from jasmine.etl.materializations.tests.test_materialization import (
    prepopulated_worker_test_backend,
)
from jasmine.etl.query_type_analysis import (
    inferred_query_column_types_table_spec,
    inferred_query_table_spec,
)
from jasmine.models import View, orm_registry
from jasmine.sql.ast_nodes import sql_ast_from_str
from jasmine.sql.table_spec import TableSpec

expected_view_table_spec = TableSpec(
    column_names=[
        "event_id",
        "path",
        "method",
        "state",
        "config",
        "context",
        "title",
        "description",
        "updated_ts",
    ],
    column_type_decls={
        "config": "JSON",
        "context": "JSON",
        "description": "LONGTEXT",
        "event_id": "BIGINT NOT NULL",
        "method": "VARCHAR(32)",
        "path": "VARCHAR(453)",
        "state": "VARCHAR(64)",
        "title": "VARCHAR(256) NOT NULL",
        "updated_ts": "DATETIME NOT NULL",
    },
    primary_key=[],
    indices={},
    unique_indices={},
    foreign_keys=[],
)


def test_inferred_query_column_types():
    with prepopulated_worker_test_backend():
        # Hardcoded in test dump.
        with app_db_session(orm_registry) as session:
            view = session.query(View).get(51)
            backend = view.project.backend
            result = inferred_query_column_types_table_spec(
                backend, sql_ast_from_str(view.spec["query_text"])
            )

    assert (
        result == expected_view_table_spec
    ), f"Unexpected table_spec: \n{pformat(result)}"


expected_view_table_spec_with_pk = TableSpec(
    column_names=[
        "event_id",
        "path",
        "method",
        "state",
        "config",
        "context",
        "title",
        "description",
        "updated_ts",
    ],
    column_type_decls={
        "config": "JSON",
        "context": "JSON",
        "description": "LONGTEXT",
        "event_id": "BIGINT NOT NULL",
        "method": "VARCHAR(40)",
        "path": "VARCHAR(453)",
        "state": "VARCHAR(64)",
        "title": "VARCHAR(256) NOT NULL",
        "updated_ts": "DATETIME NOT NULL",
    },
    primary_key=["event_id"],
    indices={},
    unique_indices={},
    foreign_keys=[],
)


def test_inferred_query_table_spec():
    with prepopulated_worker_test_backend():
        # Hardcoded in test dump.
        with app_db_session(orm_registry) as session:
            view = session.query(View).get(56)
            backend = view.project.backend
            result = inferred_query_table_spec(
                backend, sql_ast_from_str(view.spec["query_text"])
            )

    assert (
        result == expected_view_table_spec_with_pk
    ), f"Unexpected table_spec: \n{pformat(result)}"
