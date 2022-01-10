"""
Update flat materialized views over monotonically growing data.

Strategy:
- Keep high-water marks
- Do JOINs, filtering (easier because all input tables monotonic)
- Handle gravestone markers?
"""
from jasmine.sql.analysis import query_column_names
from jasmine.sql.ast_nodes import SqlProgram, sql_ast_from_str
from jasmine.sql.pretty_print import pretty_printed_sql_ast
from jasmine.sql.transforms.complex_base import with_constrained_column_values
from jasmine.sql.transforms.basic_statements import upsert_into_statement


def update_upsert_statement(db_name, table_name, query_text, timestamp_column_name):
    """
    Return an UPSERT query that takes a 'last_updated_ts_expr' format expression.

    Upsert queries:
    - INSERT INTO ... SELECT ... ON DUPLICATE KEY UPDATE ...
    - Add WHERE clause for updated_timestamp with {last_updated_ts_expr} format arg.
    - Escape '{' and '}' with '{{' and '}}'.

    >>> example_query_text = \"\"\"
    ... SELECT IFNULL(a.id, a.id2) AS id,
    ...        b.project,
    ...        '{problematic_string}',
    ...        a.a_count + b.b_count AS combined_count,
    ...        a.updated_ts AS timestamp
    ...   FROM a
    ...   JOIN b
    ...     ON a.b_id = b.id
    ...  WHERE a.id != 3
    ...  ORDER BY a.id
    ... \"\"\"

    >>> print(update_upsert_statement(
    ...     db_name="my_db",
    ...     table_name="my_table ' uhaet",
    ...     query_text=example_query_text,
    ...     timestamp_column_name="timestamp",
    ... ))
    INSERT INTO `my_db`.`my_table ' uhaet` (`id`, `project`, `'{{problematic_string}}'`, `combined_count`, `timestamp`)
    SELECT IFNULL(a.id, a.id2) AS id,
           b.project,
           '{{problematic_string}}',
           a.a_count + b.b_count AS combined_count,
           a.updated_ts AS timestamp
      FROM a
     INNER JOIN b
        ON a.b_id = b.id
     WHERE a.id != 3
       AND (a.updated_ts) >= {last_updated_ts_expr}
     ORDER BY a.id ASC
        ON DUPLICATE KEY UPDATE `id` = VALUES(`id`),
                                `project` = VALUES(`project`),
                                `'{{problematic_string}}'` = VALUES(`'{{problematic_string}}'`),
                                `combined_count` = VALUES(`combined_count`),
                                `timestamp` = VALUES(`timestamp`);
    """
    query = sql_ast_from_str(query_text)
    if isinstance(query, SqlProgram):
        assert len(query.queries) == 1
        (query,) = query.queries

    column_names = query_column_names(query)

    # Use placeholder expression, instead of the formatting argument, to sneak by grammatical correctness.
    timestamp_value_placeholder = "'temporary_placeholder_pattern_534324352'"
    if timestamp_value_placeholder in query_text:
        raise RuntimeError()

    timestamp_column_index = column_names.index(timestamp_column_name)
    constrained_query = with_constrained_column_values(
        query,
        {timestamp_column_index: timestamp_value_placeholder},
        constraint_template="{select_column} >= {criteria_expr}",
    )
    pretty_indented_select_query = pretty_printed_sql_ast(constrained_query)

    upsert_sql_query = upsert_into_statement(
        db_name, table_name, pretty_indented_select_query, column_names
    )

    return (
        upsert_sql_query.replace("{", "{{")
        .replace("}", "}}")
        .replace(timestamp_value_placeholder, "{last_updated_ts_expr}")
    )
