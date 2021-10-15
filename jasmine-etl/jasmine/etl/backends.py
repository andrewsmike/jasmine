from contextlib import contextmanager

from antlr4.xpath.XPath import XPath
from pymysql import connect
from pymysql.cursors import DictCursor

from jasmine.models import Backend
from jasmine.sql.parser.sql import children_contexts, sql_tree_from_str


def is_readonly_query(query: str) -> bool:
    """
    >>> readonly_queries = [
    ...     "SELECT 1 FROM my_table GROUP BY 3 LIMIT 10;",
    ...     "SELECT 1 UNION SELECT 2",
    ...     "SELECT 1 FROM (SELECT DATE(hello) FROM blah);",
    ... ]
    >>> for query in readonly_queries:
    ...     print(f"'{query}': {is_readonly_query(query)}")
    'SELECT 1 FROM my_table GROUP BY 3 LIMIT 10;': True
    'SELECT 1 UNION SELECT 2': True
    'SELECT 1 FROM (SELECT DATE(hello) FROM blah);': True


    >>> mutating_queries = [
    ...     "INSERT INTO my_table (a) SELECT 1",
    ...     "REPLACE INTO my_table (a) SELECT 1",
    ...     "SELECT 1; INSERT INTO my_table (a) VALUES (10)",
    ...     "CREATE TABLE my_table AS SELECT 1",
    ...     "SELECT 1; DROP TABLE blah; SELECT 1;",
    ...     'SELECT 1 INTO OUTFILE "/tmp/bleh.csv"',
    ...     "SELECT 1 FROM my_table INTO OUTFILE '/tmp/blah.csv'",
    ...     "SELECT 1 UHTNEONUTHOEH UHONUTHN E",
    ... ]
    >>> for query in mutating_queries:
    ...     print(f"'{query}': {is_readonly_query(query)}")
    'INSERT INTO my_table (a) SELECT 1': False
    'REPLACE INTO my_table (a) SELECT 1': False
    'SELECT 1; INSERT INTO my_table (a) VALUES (10)': False
    'CREATE TABLE my_table AS SELECT 1': False
    'SELECT 1; DROP TABLE blah; SELECT 1;': False
    'SELECT 1 INTO OUTFILE "/tmp/bleh.csv"': False
    'SELECT 1 FROM my_table INTO OUTFILE '/tmp/blah.csv'': False
    'SELECT 1 UHTNEONUTHOEH UHONUTHN E': False
    """
    try:
        sql_program = sql_tree_from_str(query)
    except SyntaxError as syntax_error:
        return False

    statements = children_contexts(sql_program.statement)
    if len(statements) != 1:
        return False

    (statement,) = statements

    into_clauses = XPath.findAll(sql_program, "//intoClause", sql_program.parser)
    if into_clauses:
        return False

    # Yes, this is monstrous. It can be layed out properly,
    # use actual xpaths, or simulate xpath-like traversal in the future.
    return ((simple_statement := statement.simpleStatement()) is not None) and (
        (select_statement := simple_statement.selectStatement()) is not None
        and (select_statement.selectStatementWithInto() is None)
    )


class ReadOnlyDictCursor(DictCursor):
    def execute(self, query, args):
        assert is_readonly_query(
            query
        ), f"Attempted to run mutating or combined statement using readonly DictCursor. Query:\n{query}"

        return super().execute(query, args)


@contextmanager
def new_backend_conn(backend: Backend):
    assert (
        backend.backend_type == "mysql"
    ), "Only MySQL backends are currently supported."
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
