"""
SQL query transformations.

Note: Since these are large dataclass datastructures, use recursive replace() calls.
Deepcopy() may not work well here, and you risk stepping on other queries' toes.

Initial tests:
- Add criteria on first two SELECT columns [CHECK]
- Add "WHERE updated_ts > NOW() - weeks" [CHECK]

- Extract set of table/column references by paths
- Map identifiers to table/column references

- Propagate WHERE criteria down to subqueries where applicable
    - Ex: INNER joins w/o RIGHT joins, right side of RIGHT joins, WHERE IN clauses?
- Remove a JOIN
- Add a JOIN
- Replace a table
- UNION multiple variants of a query (IE sharding).
- Remove GROUP BY
- Building an aggregate table
- Breaking out a recursive query into multiple CTEs
- Combining a view tree into a single CTE-based expr
- Renaming columns
- Add denormalization, normalization (add JOIN, change SELECT.)
"""
from dataclasses import replace
from functools import partial
from os.path import dirname, join
from sys import argv
from typing import Callable

from jasmine.sql.ast_nodes import (
    ASTNode,
    CTEOrderLimitNode,
    QuerySpecNode,
    SelectExpr,
    SqlProgram,
    UnionNode,
    sql_ast,
    sql_subexpr_ast,
)
from jasmine.sql.parser.sql import sql_tree_from_file
from jasmine.sql.pretty_print import pretty_printed_sql_ast


def passthrough_transformation(
    node: ASTNode,
    transform_func: Callable,
) -> ASTNode:
    """
    When writing transformations, we typically want to recurse down the top-level structure of a query.
    These may or may not block, manipulate, or be the end-point for a given transformation.

    To handle this, have transformations 'inherit' from this base passthrough transformation using matching.

    IE, if your transformation only cares about QuerySpecNodes, and passes through UNIONs / etc, do the following:
    ```
    def my_transform(node, ...):
        match node:
            case QuerySpecNode(...):
                ...
            case _:
                return passthrough_transformation(node, partial(my_transformation, ...))
    ```
    """
    match node:
        case SqlProgram():
            return replace(
                node,
                queries=[transform_func(query) for query in node.queries],
            )

        case UnionNode():
            return replace(
                node,
                subqueries=[transform_func(subquery) for subquery in node.subqueries],
            )

        case CTEOrderLimitNode():
            return replace(node, subquery=transform_func(node.subquery))

        case QuerySpecNode():
            return node

        case _:
            raise ValueError(f"Unknown node type: {type(node).__name__}")


def with_constrained_column_values(
    node: ASTNode,
    select_column_criteria: dict[int, str],
    constraint_template: str = "{select_column} = {criteria_expr}",
) -> ASTNode:
    """
    Add 'WHERE <col> = <expr>' clauses to a set of output columns, identified by their zero-indexed position.

    Expressions are unquoted; you can put anything in there. Be careful to escape things properly.

    You can specify other constraints (`>=`, `!=`, `IFNULL(..., ) = `, etc) by passing in a constraint_template.
    This setup is a bit limited, and should be genericized in the future.

    >>> from jasmine.sql.ast_nodes import sql_ast_from_str
    >>> from jasmine.sql.pretty_print import pretty_printed_sql_ast

    >>> query = sql_ast_from_str("SELECT a.id, a.value + b.value FROM a JOIN b WHERE a.id > 0")
    >>> constrained_query = with_constrained_column_values(
    ...     query,
    ...     select_column_criteria={1: "1"},
    ...     constraint_template="{select_column} >= {criteria_expr}",
    ... )
    >>> print(pretty_printed_sql_ast(constrained_query))
    SELECT a.id, a.value + b.value
      FROM a
     INNER JOIN b
     WHERE a.id > 0 AND (a.value + b.value) >= 1;
    """
    match node:
        case QuerySpecNode():
            assert all(
                isinstance(node.select_exprs[select_column_index], SelectExpr)
                and node.select_exprs[select_column_index].select_expr_type == "expr"
                for select_column_index in select_column_criteria.keys()
            ), "Cannot constrain column values for queries using wildcard (table.*) expressions."

            return replace(
                node,
                where_clauses=(
                    (node.where_clauses or [])
                    + [
                        sql_subexpr_ast(
                            constraint_template.format(
                                select_column="("
                                + pretty_printed_sql_ast(
                                    node.select_exprs[select_column_index].expr
                                )
                                + ")",
                                criteria_expr=criteria_expr_str,
                            ),
                            "expr",
                        )
                        for select_column_index, criteria_expr_str in select_column_criteria.items()
                    ]
                ),
            )

        case _:
            return passthrough_transformation(
                node,
                partial(
                    with_constrained_column_values,
                    select_column_criteria=select_column_criteria,
                    constraint_template=constraint_template,
                ),
            )


def display_transformed_query():
    sql_source_path = join(
        dirname(__file__),
        "examples",
        f"{argv[1]}.sql",
    )

    query = sql_ast(sql_tree_from_file(sql_source_path))

    print("Before transformation:")
    print(pretty_printed_sql_ast(query))
    print()

    transformed_query = with_constrained_column_values(
        query,
        {
            1: '"My company"',
            2: '"dev"',
        },
    )

    print("After constrained_column transformation:")
    print(pretty_printed_sql_ast(transformed_query))
    print()
