"""
View creation / deletion functions.

Note:
- This does not allow you to verify that the target view is semantically equivalent to the view you want to drop.
    If someone moves something else in, you're going to end up dropping it. This may be a usability consideration.

>>> print(create_view_statement("`my db;`", "my_table;;&", "SELECT 1\\n   FROM     blaaaaah"))
CREATE VIEW `my db;`.`my_table;;&` AS
    SELECT 1 FROM blaaaaah;
>>> print(create_view_statement("`my db;`", "my_table;;&", "WITH a (a, b, c) AS SELECT 1, 2, 3 FROM dual SELECT 1 FROM blaaaaah"))
Traceback (most recent call last):
    ...
AssertionError: Can only create views for read-only SELECT statements.
...

>>> print(create_view_statement("`my db;`", "my_table;;&", "DELETE FROM blah"))
Traceback (most recent call last):
    ...
AssertionError: Can only create views for read-only SELECT statements.
...

>>> print(create_view_statement("`my db;`", "my_table;;&", "CREATE VIEW blah AS SELECT 1"))
Traceback (most recent call last):
    ...
AssertionError: Can only create views for read-only SELECT statements.
...

>>> print(drop_view_statement("`my db;`", "my_table;;&"))
DROP VIEW IF EXISTS `my db;`.`my_table;;&`

"""
from jasmine.sql.analysis import is_readonly_query
from jasmine.sql.pretty_print import sql_pretty_printed
from jasmine.sql.transforms.escaping import escaped_db_table


def create_view_statement(db_name: str, table_name: str, query_str: str) -> str:
    assert is_readonly_query(
        query_str
    ), "Can only create views for read-only SELECT statements."

    pretty_indented_query = sql_pretty_printed(query_str).replace("\n", "\n    ")
    return f"CREATE VIEW {escaped_db_table(db_name, table_name)} AS\n    {pretty_indented_query}"


def drop_view_statement(db_name: str, table_name: str) -> str:
    return f"DROP VIEW IF EXISTS {escaped_db_table(db_name, table_name)}"
