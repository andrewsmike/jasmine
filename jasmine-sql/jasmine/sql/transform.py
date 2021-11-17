"""
SQL query transformations.

Note: Since these are large dataclass datastructures, use recursive replace() calls.
Deepcopy() may not work well here, and you risk stepping on other queries' toes.

Initial tests:
- Add criteria on first two SELECT columns
- Remove a JOIN
- Replace a table
- Add a JOIN
- UNION multiple variants of a query (IE sharding).
- Remove GROUP BY
- Building an aggregate table
- Breaking out a recursive query into multiple CTEs
- Combining a view tree into a single CTE-based expr
- Renaming columns
"""
from dataclasses import replace
from os.path import dirname, join
from sys import argv

from jasmine.sql.ast_nodes import (
    ASTNode,
    CTEOrderLimitNode,
    QuerySpecNode,
    SelectExpr,
    SqlProgram,
    UnionNode,
    sql_ast,
)
from jasmine.sql.parser.sql import sql_parser_from_str, sql_tree_from_file
from jasmine.sql.pretty_print import pretty_printed_sql_ast

# TODO: Replace MockNode with ParseNode construction system. Maybe through pretty printing, then parsing?


def sql_subexpr_ast(sql_subexpr: str, expr_type_str: str):
    parser = sql_parser_from_str(sql_subexpr)

    # Prepare to parse a particular grammatical rule.
    # TODO: This didn't throw an error when it should have.
    parse_func = getattr(parser, expr_type_str)

    parse_tree = parse_func()

    return sql_ast(parse_tree)


def parse_tree_node(
    template_str: str,
    parse_node_type_str: str,
    **keyword_format_args,
):
    rendered_sql_subexpr = template_str.format(
        **{
            keyword: pretty_printed_sql_ast(format_arg)
            for keyword, format_arg in keyword_format_args.items()
        }
    )

    result = sql_subexpr_ast(rendered_sql_subexpr, parse_node_type_str)

    return result


def with_constrained_column_values(
    node: ASTNode,
    select_column_criteria: dict[int, str],
) -> ASTNode:
    match node:
        case SqlProgram():
            return replace(
                node,
                queries=[
                    with_constrained_column_values(query, select_column_criteria)
                    for query in node.queries
                ],
            )
        case UnionNode():
            return replace(
                node,
                subqueries=[
                    with_constrained_column_values(subquery, select_column_criteria)
                    for subquery in node.subqueries
                ],
            )
        case CTEOrderLimitNode():
            return replace(
                node,
                subquery=with_constrained_column_values(node.subquery, select_column_criteria)
            )
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
                        parse_tree_node(
                            f"{{select_column}} = {column_value_str}",
                            parse_node_type_str="expr",
                            select_column=node.select_exprs[select_column_index].expr,  # TODO: Assert no stars
                        )
                        for select_column_index, column_value_str in select_column_criteria.items()
                    ]
                ),
            )

        case _:
            raise ValueError(f"Unknown node type: {type(node).__name__}")


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

    print("After transformation:")
    print(pretty_printed_sql_ast(transformed_query))
    print()
