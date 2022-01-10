from jasmine.sql.analysis import query_column_names
from jasmine.sql.ast_nodes import sql_ast_from_str
from jasmine.sql.transforms.escaping import (
    escaped,
    escaped_column_list,
    escaped_db_table,
)


def insert_into_statement(db_name, table_name, query_text, column_names=None):
    """
    Create a vanilla INSERT statement for the given query.
    Optionally derive the column names from the query directly.

    >>> print(insert_into_statement(
    ...     "my_db",
    ...     "my_table ' uea$3}",
    ...     "SELECT 1 + 4, my_other_table.a FROM my_other_table WHERE 4",
    ... ))
    INSERT INTO `my_db`.`my_table ' uea$3}` (`1 + 4`, `a`)
    SELECT 1 + 4, my_other_table.a FROM my_other_table WHERE 4;
    """
    if column_names is None:
        column_names = query_column_names(sql_ast_from_str(query_text))

    return (
        f"INSERT INTO {escaped_db_table(db_name, table_name)} ({escaped_column_list(column_names)})\n"
        + query_text
        + ";"
    )


def upsert_into_statement(db_name, table_name, query_text, column_names=None):
    """
    Create an UPSERT statement for the given query.
    Optionally derive the column names from the query directly.

    >>> print(upsert_into_statement(
    ...     "my_db",
    ...     "my_table ' uea$3}",
    ...     "SELECT 1 + 4, my_other_table.a FROM my_other_table WHERE 4",
    ... ))
    INSERT INTO `my_db`.`my_table ' uea$3}` (`1 + 4`, `a`)
    SELECT 1 + 4, my_other_table.a FROM my_other_table WHERE 4
        ON DUPLICATE KEY UPDATE `1 + 4` = VALUES(`1 + 4`),
                                `a` = VALUES(`a`);
    """
    if column_names is None:
        column_names = query_column_names(sql_ast_from_str(query_text))

    return (
        "\n".join(
            [
                f"INSERT INTO {escaped_db_table(db_name, table_name)} ({escaped_column_list(column_names)})",
                query_text,
                "    ON DUPLICATE KEY UPDATE "
                + ",\n                            ".join(
                    f"{escaped(column_name)} = VALUES({escaped(column_name)})"
                    for column_name in column_names
                ),
            ]
        )
        + ";"
    )
