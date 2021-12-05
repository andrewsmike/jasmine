"""
Escaping tools.
"""

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


def escaped(name: str) -> str:
    if "`" in name:
        name = unescaped(name)

    return f"`{name}`"


def escaped_db_table(db_name: str, table_name: str) -> str:
    return escaped(db_name) + "." + escaped(table_name)


def escaped_column_list(column_names: list[str]) -> str:
    return ", ".join(escaped(column_name) for column_name in column_names)
