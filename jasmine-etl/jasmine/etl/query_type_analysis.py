from dataclasses import replace
from random import choices
from string import ascii_letters, digits

from sqlalchemy import inspect, text

from jasmine.etl.backends import Backend, backend_engine
from jasmine.sql.analysis import top_level_group_by_column_indices
from jasmine.sql.ast_nodes import ASTNode
from jasmine.sql.pretty_print import pretty_printed_sql_ast
from jasmine.sql.table_spec import TableSpec, drop_table_statement
from jasmine.sql.transforms.complex_base import with_limit


def inferred_query_column_types_table_spec(
    backend: Backend, query_node: ASTNode
) -> TableSpec:
    """
    Infer everything about the output data from a SQL query using the actual backend database.

    This method:
    - Creates a SQLAlchemy connection
    - Creates a temporaty table using the `CREATE TEMPORARY TABLE ... AS SELECT ...;` syntax.
    - Applies `LIMIT 0;` to the query, so the engine doesn't actually _do_ anything, but still
        performs column name and column type inference.
    - Uses SQLAlchemy's inspector API to extract an appropriate TableSpec.

    `CREATE TABLE ... AS ... LIMIT 0;` is a recognized strategy for copying the schema of a table
    without its data, and is here used to get the schema of query output instead.

    Currently, this is MySQL specific and untested elsewhere.

    See test_query_type_analysis.py for an example output.
    """
    limited_query_sql = pretty_printed_sql_ast(with_limit(query_node, 0))

    random_table_name = "view_type_testing_" + "".join(
        choices(ascii_letters + digits, k=12)
    )
    create_type_detecting_temp_table = (
        f"CREATE TEMPORARY TABLE {random_table_name} AS {limited_query_sql}"
    )

    engine = backend_engine(backend)
    with engine.connect() as conn:
        conn.execute(text(create_type_detecting_temp_table))
        table_spec = TableSpec.from_sqla_inspector(
            inspect(conn), db_name=None, table_name=random_table_name
        )
        conn.execute(
            text(
                drop_table_statement(
                    db_name=None,
                    table_name=random_table_name,
                    idempotent=False,
                    temporary=True,
                )
            )
        )

    return table_spec


def inferred_query_table_spec(
    backend: Backend, query_node: ASTNode, require_primary_key: bool = False
) -> TableSpec:
    column_table_spec = inferred_query_column_types_table_spec(backend, query_node)

    try:
        top_level_group_by_indices = top_level_group_by_column_indices(
            query_node, column_names=column_table_spec.column_names
        )
        primary_key_columns = [
            column_table_spec.column_names[group_by_column_index]
            for group_by_column_index in top_level_group_by_indices or []
        ]
    except ValueError as e:
        if require_primary_key:
            raise
        else:
            primary_key_columns = []

    return replace(
        column_table_spec,
        primary_key=primary_key_columns,
    )
