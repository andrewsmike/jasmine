"""
Escaping tools.
"""
from sqlalchemy import String
from sqlalchemy.dialects.mysql import dialect

__all__ = [
    "escaped",
    "escaped_column_list",
    "escaped_db_table",
    "unescaped",
]


def unescaped(name: str) -> str:
    if "`" not in name:
        return name

    assert (
        len(name) > 2 and "`" not in name[1:-1] and (name[0] == "`") and name[-1] == "`"
    ), f"Error unescaping name '{name}': Name contains backticks, but they aren't formatted correctly."

    return name[1:-1]


def string_literal_expr(value: str) -> str:
    """
    >>> print(string_literal_expr("Hello '\\" world!;`"))
    'Hello ''" world!;`'
    """
    return String("").literal_processor(dialect=dialect())(value=value)


def escaped(name: str) -> str:
    if "`" in name:
        name = unescaped(name)

    return f"`{name}`"


def escaped_db_table(db_name: str | None, table_name: str) -> str:
    if db_name is not None:
        return escaped(db_name) + "." + escaped(table_name)
    else:
        return escaped(table_name)


def escaped_column_list(column_names: list[str]) -> str:
    return ", ".join(escaped(column_name) for column_name in column_names)


def escaped_table_column_list(table_name: str, column_names: list[str]) -> str:
    return ", ".join(
        f"{escaped(table_name)}.{escaped(column_name)}" for column_name in column_names
    )
