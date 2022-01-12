"""
Answer basic questions about a SQL query.

This is intended to extract semantically important information, such as:
- Is this query read-only?

- What columns does this query produce?
    What are their names, are they tied to the types of any input table columns? [TODO]
- Are there any top-level GROUP BY statements? Do they align cleanly with the SELECT columns? [TODO]
    - Rollups / OLAP options, DISTINCT options, etc

- What tables are used? [TODO]
- What top-level CTEs are there? [TODO]
"""

from antlr4.xpath.XPath import XPath

from jasmine.sql.ast_nodes import (
    ASTNode,
    CTEOrderLimitNode,
    Identifier,
    ParseTreeNode,
    QuerySpecNode,
    SelectExpr,
    SqlProgram,
    UnionNode,
)
from jasmine.sql.parser.sql import SQLParser, children_contexts, sql_tree_from_str
from jasmine.sql.pretty_print import PrettyPrintVisitor, pretty_printed_sql_ast


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
    ...     try:
    ...         print(f"'{query}': {is_readonly_query(query)}")
    ...     except SyntaxError as e:
    ...         print(f"'{query}': Failed to parse query: {e}")
    'INSERT INTO my_table (a) SELECT 1': False
    'REPLACE INTO my_table (a) SELECT 1': False
    'SELECT 1; INSERT INTO my_table (a) VALUES (10)': False
    'CREATE TABLE my_table AS SELECT 1': False
    'SELECT 1; DROP TABLE blah; SELECT 1;': False
    'SELECT 1 INTO OUTFILE "/tmp/bleh.csv"': False
    'SELECT 1 FROM my_table INTO OUTFILE '/tmp/blah.csv'': False
    'SELECT 1 UHTNEONUTHOEH UHONUTHN E': Failed to parse query: At 1:23: mismatched input 'UHONUTHN' expecting {<EOF>, ';'}
    """
    sql_program = sql_tree_from_str(query)

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


def uses_subqueries(query: ASTNode) -> bool:
    """
    Subqueries are used in a variety of places:
    - CTEs
    - FROM / JOIN clauses
    - In expressions (SELECT, ON, WHERE, GROUP BY, HAVING, ...)

    To detect them all, use xpaths on the original parse tree.

    >>> subquery_queries = [
    ...     "SELECT 1 FROM (SELECT 1 FROM dual) GROUP BY 3 LIMIT 10;",
    ...     "SELECT (SELECT 1 FROM dual) FROM dual UNION SELECT 2",
    ...     "SELECT 1 FROM dual WHERE (SELECT 1 FROM dual WHERE DATE(hello) = 3)",
    ...     "SELECT 1 FROM dual GROUP BY id IN (SELECT id FROM my_table)",
    ... ]
    >>> for query in subquery_queries:
    ...     print(f"'{query}': {uses_subqueries(query)}")
    'SELECT 1 FROM (SELECT 1 FROM dual) GROUP BY 3 LIMIT 10;': True
    'SELECT (SELECT 1 FROM dual) FROM dual UNION SELECT 2': True
    'SELECT 1 FROM dual WHERE (SELECT 1 FROM dual WHERE DATE(hello) = 3)': True
    'SELECT 1 FROM dual GROUP BY id IN (SELECT id FROM my_table)': True

    >>> flat_queries = [
    ...     'WITH blah AS (SELECT 1 FROM dual) SELECT 1 FROM a JOIN b JOIN c',
    ...     'SELECT 1 FROM a JOIN b JOIN c',
    ...     "SELECT 1 FROM my_table  GROUP BY abcd",
    ...     "SELECT 1 FROM UHTNEONUTHOEH ",
    ... ]
    >>> for query in flat_queries:
    ...     try:
    ...         print(f"'{query}': {uses_subqueries(query)}")
    ...     except SyntaxError as e:
    ...         print(f"'{query}': Failed to parse query: {e}")
    'WITH blah AS (SELECT 1 FROM dual) SELECT 1 FROM a JOIN b JOIN c': False
    'SELECT 1 FROM a JOIN b JOIN c': False
    'SELECT 1 FROM my_table  GROUP BY abcd': False
    'SELECT 1 FROM UHTNEONUTHOEH ': False
    """
    sql_program = sql_tree_from_str(query)

    statements = children_contexts(sql_program.statement)
    assert len(statements) == 1, "Cannot analyze multiple queries at a time."
    (statement,) = statements

    subquery_clauses = XPath.findAll(
        sql_program, "//!commonTableExpression/subquery", sql_program.parser
    )
    return len(subquery_clauses) > 0


def query_column_names(node: ASTNode) -> list[str]:
    """
    Infer column names from an AST-represented SQL query.

    Note: This cannot currently handle table.* expressions.
        That expansion (based on schema data) can be added later.

    Note: Column names _must_ be escaped before being encoded in SQL. They're not safe.

    >>> from jasmine.sql.ast_nodes import sql_ast_from_str, sql_ast_repr

    >>> print(sql_ast_repr("SELECT 1, 3 AS my_column"))
    {'queries': [{'select_exprs': [{'expr': ('raw', '1'),
                                    'select_expr_type': 'expr',
                                    'type': 'SelectExpr'},
                                   {'expr': ('raw', '3'),
                                    'expr_alias': 'my_column',
                                    'select_expr_type': 'expr',
                                    'type': 'SelectExpr'}],
                  'type': 'QuerySpecNode'}],
     'type': 'SqlProgram'}
    >>> query_column_names(sql_ast_from_str("SELECT 1, 3 AS my_column"))
    ['1', 'my_column']

    >>> query_column_names(sql_ast_from_str(
    ...     "SELECT table_one.a, table_two.b, SUM(table_three.c) FROM a JOIN b USING (bleh) GROUP BY 1"
    ... ))
    ['a', 'b', 'SUM(table_three.c)']


    >>> query_column_names(sql_ast_from_str("SELECT 1, 3 AS my_column UNION SELECT 4, blah.blih AS my_column_2 ORDER BY 1"))
    ['1', 'my_column']

    Error handling:
    >>> query_column_names(sql_ast_from_str("SELECT blah.*"))
    Traceback (most recent call last):
      ...
    NotImplementedError: Cannot infer column names from 'SELECT table.*' queries.

    >>> query_column_names(sql_ast_from_str("SELECT *"))
    Traceback (most recent call last):
      ...
    NotImplementedError: Cannot infer column names from 'SELECT *' queries.

    >>> query_column_names(sql_ast_from_str("SELECT 1; SELECT 4"))
    Traceback (most recent call last):
      ...
    AssertionError: Attempted to find resulting column names of multiple queries instead of one...
    """
    match node:
        case SqlProgram(queries=queries):
            assert (
                len(queries) == 1
            ), "Attempted to find resulting column names of multiple queries instead of one."
            return query_column_names(queries[0])

        case SelectExpr(
            select_expr_type=select_expr_type, expr=expr, expr_alias=expr_alias
        ):
            if select_expr_type == "table_star":
                raise NotImplementedError(
                    "Cannot infer column names from 'SELECT table.*' queries."
                )

            elif expr_alias is not None:
                assert isinstance(
                    expr_alias, str
                ), "Parsing error: expression alias should have been a string."
                return expr_alias

            else:
                column_name_parts = column_ref_expr_parts(expr)
                if column_name_parts is not None:
                    return column_name_parts[-1]
                else:
                    return PrettyPrintVisitor().pretty_print(node)

        case QuerySpecNode(select_exprs=select_exprs):
            return [query_column_names(select_expr) for select_expr in select_exprs]

        case UnionNode(subqueries=subqueries):
            return query_column_names(subqueries[0])

        case CTEOrderLimitNode(subquery=subquery):
            return query_column_names(subquery)

        case ParseTreeNode(base_node=base_node):
            if base_node.symbol.type == SQLParser.MULT_OPERATOR:
                raise NotImplementedError(
                    "Cannot infer column names from 'SELECT *' queries."
                )
            else:
                raise ValueError(
                    f"Found non-'*' terminal at top of SELECT expression: {base_node}"
                )

        case _:
            raise ValueError(
                f"Could not derive column names from node of type {type(node)}."
            )

    # For MyPy.
    assert False, "Unreachable."


def column_ref_expr_parts(node: ParseTreeNode | None) -> tuple[str] | None:
    """
    If the given SELECT expression is a direct reference to a source column,
    what are the DB / table / column name parts, if any?

    This is useful for directly inheriting column names as well as inferring types.

    >>> from jasmine.sql.ast_nodes import sql_subexpr_ast

    >>> for expr_str in [
    ...     "my_table.a",
    ...     "my_db.my_table.`u hueahto n; `",
    ...     "abcd",
    ...     "a + b",
    ... ]:
    ...     print(column_ref_expr_parts(sql_subexpr_ast(expr_str, "expr")))
    ('my_table', 'a')
    ('my_db', 'my_table', 'u hueahto n; ')
    ('abcd',)
    None
    """
    # For MyPy.
    if node is None:
        return None

    match node:
        case Identifier():
            return (node.text,)

        # Visit identifier leaf nodes in order and flatten the result.
        case ParseTreeNode(
            base_node=(
                SQLParser.FieldIdentifierContext()
                | SQLParser.QualifiedIdentifierContext()
                | SQLParser.DotIdentifierContext()
            )
        ):
            return (
                tuple(
                    column_name
                    for child in node.children
                    if (column_name_parts := column_ref_expr_parts(child)) is not None
                    for column_name in column_name_parts
                )
                or None
            )

        # Passthrough nodes.
        case ParseTreeNode(
            base_node=(
                SQLParser.ExprIsContext()
                | SQLParser.PrimaryExprPredicateContext()
                | SQLParser.PredicateContext()
                | SQLParser.BitExprContext()
                | SQLParser.SimpleExprColumnRefContext()
                | SQLParser.ColumnRefContext()
            )
        ) if len(node.children) == 1:
            (child,) = node.children
            return column_ref_expr_parts(child)

        case _:
            return None

    # For MyPy.
    assert False, "Unreachable."


def top_level_group_by_column_indices(
    node: ASTNode, column_names: list[str] | None = None
) -> list[int]:
    """
    The column indices for group by expressions.
    Throws a ValueError if the query does not have a clean top-level GROUP BY statement.

    Columns are zero-indexed.

    Note: Column names _must_ be escaped before being encoded in SQL. They're not safe.

    >>> from jasmine.sql.ast_nodes import sql_ast_from_str, sql_ast_repr

    >>> def display_results(query_text):
    ...     print(top_level_group_by_column_indices(sql_ast_from_str(query_text)))

    Simple example:
    >>> display_results("SELECT a, b AS my_column FROM blah GROUP BY b")
    [1]

    >>> display_results("SELECT a, b AS my_column FROM blah GROUP BY 2")
    [1]

    All top-level SELECTs need to have a consistent GROUP BY:
    >>> display_results("SELECT a, b + l, c FROM blah GROUP BY b + l UNION SELECT 1, 2, 3 FROM dual GROUP BY 2;")
    [1]

    Inconsistent GROUP BYs clash:
    >>> display_results("SELECT a, b + l, c FROM blah GROUP BY b + l UNION SELECT 1 AS a, 2, 3 FROM bleh GROUP BY a;")
    Traceback (most recent call last):
      ...
    ValueError: Cannot infer top level GROUP BY clauses; they are inconsistent across UNIONs.


    >>> display_results("SELECT blah.* FROM blah GROUP BY b + l")
    Traceback (most recent call last):
      ...
    ValueError: Cannot infer GROUP BY column indices from 'SELECT table.*' queries.


    >>> display_results("SELECT * FROM blah GROUP BY b + l")
    Traceback (most recent call last):
      ...
    ValueError: Cannot infer top level GROUP BY columns in 'SELECT *' queries.


    >>> display_results("SELECT abcd FROM blah GROUP BY 5 + 34")
    Traceback (most recent call last):
      ...
    ValueError: Cannot infer GROUP BY columns; GROUP BY expression not SELECTed: '5 + 34'
    """
    match node:
        case SqlProgram(queries=queries):
            assert (
                len(queries) == 1
            ), "Attempted to find top-level GROUP BY columns of multiple queries instead of one."
            return top_level_group_by_column_indices(
                queries[0], column_names=column_names
            )

        case QuerySpecNode(
            select_exprs=select_exprs,
            select_options=select_options,
            group_by_exprs=group_by_exprs,
        ):
            if select_options:
                raise ValueError(
                    "Cannot infer top level GROUP BY columns: select options not currently supported."
                )

            if any(
                not isinstance(select_expr, SelectExpr) for select_expr in select_exprs
            ):
                raise ValueError(
                    "Cannot infer top level GROUP BY columns in 'SELECT *' queries."
                )

            if any(
                select_expr.select_expr_type != "expr" for select_expr in select_exprs
            ):
                raise ValueError(
                    "Cannot infer GROUP BY column indices from 'SELECT table.*' queries."
                )

            if not group_by_exprs:
                raise ValueError(
                    "Cannot infer GROUP BY columns; no top-level GROUP BY expression."
                )

            select_expr_identifying_strs = [
                (
                    {pretty_printed_sql_ast(select_expr.expr), select_expr.expr_alias}
                    | (
                        {column_names[select_index]}
                        if column_names is not None
                        else set()
                    )
                )
                for select_index, select_expr in enumerate(select_exprs)
            ]
            column_indices = []
            for group_by_expr in group_by_exprs:
                group_by_expr_str = pretty_printed_sql_ast(group_by_expr)

                try:
                    # Column indices are zero-indexed.
                    column_indices.append(int(group_by_expr_str) - 1)
                    continue
                except Exception as e:
                    pass

                for column_index, identifying_strs in enumerate(
                    select_expr_identifying_strs
                ):
                    if group_by_expr_str in identifying_strs:
                        column_indices.append(column_index)
                        break
                else:
                    raise ValueError(
                        f"Cannot infer GROUP BY columns; GROUP BY expression not SELECTed: '{group_by_expr_str}'"
                    )

            return column_indices

        case UnionNode(subqueries=subqueries):
            subquery_column_indices = set()
            for subquery in subqueries:
                try:
                    subquery_column_indices.add(
                        tuple(
                            top_level_group_by_column_indices(
                                subquery, column_names=column_names
                            )
                        )
                    )
                except ValueError as e:
                    pass

            if len(subquery_column_indices) == 1:
                (column_indices,) = subquery_column_indices
                return list(column_indices)
            else:
                raise ValueError(
                    "Cannot infer top level GROUP BY clauses; they are inconsistent across UNIONs."
                )

        case CTEOrderLimitNode(subquery=subquery):
            return top_level_group_by_column_indices(
                subquery, column_names=column_names
            )

        case _:
            raise ValueError(
                f"Could not derive top level GROUP BY columns from node of type {type(node)}."
            )

    # For MyPy.
    assert False, "Unreachable."
