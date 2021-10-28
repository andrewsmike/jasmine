"""
SQL AST node implementations.

These are representations of various SQL expressions (SELECT queries, UNIONs, order expressions, etc).
See ast_base.py for details.

The sql_ast() function visits ParseTrees and encodes them as AST nodes using the list of available
representations (sql_parse_tree_node_type) and their cls.from_parse_tree() methods.
"""
from dataclasses import dataclass
from typing import Dict, List, Literal, Optional, Type

from antlr4.ParserRuleContext import ParserRuleContext
from antlr4.tree.Tree import TerminalNodeImpl

from jasmine.sql.ast_base import ASTNode
from jasmine.sql.parser.sql import ParseTree, SQLParser, children_contexts


@dataclass
class ParseTreeNode(ASTNode):
    """
    An AST node that is just a parse tree node.

    This effectively forms a scaffold over "unrepresented" sections of a the
    parse tree and copies their structure.
    """

    base_node: ParseTree
    children: List[ASTNode]

    @classmethod
    def from_parse_tree(cls, parse_tree: ParseTree) -> ASTNode:
        children_nodes = [
            sql_ast(child) for child in getattr(parse_tree, "children", [])
        ]
        return cls(parse_tree, children_nodes)

    def node_type_name(self) -> str:
        node_type_name = type(self.base_node).__name__
        if node_type_name.endswith("Context"):
            node_type_name = node_type_name[: -len("Context")]

        return node_type_name

    def __str__(self) -> str:
        if isinstance(self.base_node, TerminalNodeImpl):
            return self.base_node.getText()
        else:
            return super().__str__()


# TODO: Clean this up a bit.
@dataclass
class TableRef:
    ref: str

    @classmethod
    def from_parse_tree(cls, node: ParseTree) -> ASTNode:
        name = ".".join(
            ref_path_part.getText()
            for ref_path_part in children_contexts(node.identifier)
        )
        return cls(ref=name)


@dataclass
class SelectExpr:
    select_expr_type: Literal["expr", "star", "table_star"]

    expr: Optional[ASTNode] = None
    expr_alias: Optional[str] = None

    star_table: Optional[TableRef] = None

    @classmethod
    def from_parse_tree(cls, node: ParseTree) -> ASTNode:
        if isinstance(node, TerminalNodeImpl):
            assert node.getText() == "*"
            return cls(select_expr_type="star")

        assert isinstance(node, SQLParser.SelectItemContext)

        if node.tableWild() is not None:
            return cls(
                select_expr_type="table_star", star_table=TableRef.from_parse_tree(node)
            )

        if node.expr() is not None:
            return cls(
                select_expr_type="expr",
                expr=sql_ast(node.expr()),
                expr_alias=optional_sql_ast(node.selectAlias()),
            )

        raise ValueError(f"Unknown node type: {type(node).__name__}")


# TODO: Better representation.
def select_exprs(select_expr_node: Optional[ParseTree]) -> list[ASTNode]:
    assert select_expr_node is not None, "Given empty select expression list."
    assert isinstance(select_expr_node, SQLParser.SelectItemListContext)

    multi_expr = select_expr_node.MULT_OPERATOR()
    opt_multi_exprs = [multi_expr] if multi_expr is not None else []

    select_exprs = opt_multi_exprs + children_contexts(select_expr_node.selectItem)

    return [sql_ast(select_expr) for select_expr in select_exprs]


def sql_ast_clauses_from_expr(expr_node: SQLParser.ExprContext) -> list[ASTNode]:
    """
    >>> from pprint import pprint
    >>> from jasmine.sql.ast_nodes import sql_ast_clauses_from_expr
    >>> from jasmine.sql.parser.sql import sql_parser_from_str
    >>> from jasmine.sql.pretty_print import PrettyPrintVisitor

    >>> example_exprs = [
    ...     "1 AND my_column = other_table.other_column AND (4 IS NULL OR CONCAT('Hi', 'yo') = 'Hiyo')",
    ... ]

    >>> for example_expr in example_exprs:
    ...     print(f"Input: `{example_expr}`:")
    ...     exprs = sql_ast_clauses_from_expr(sql_parser_from_str(example_expr).expr())
    ...     print("Output:")
    ...     pprint([PrettyPrintVisitor().pretty_print(expr) for expr in exprs])
    Input: `1 AND my_column = other_table.other_column AND (4 IS NULL OR CONCAT('Hi', 'yo') = 'Hiyo')`:
    Output:
    ['1',
     'my_column = other_table . other_column',
     "( 4 IS NULL OR CONCAT ( 'Hi' , 'yo' ) = 'Hiyo' )"]
    """
    if not isinstance(expr_node, SQLParser.ExprAndContext):
        return [sql_ast(expr_node)]

    return [
        clause
        for child_expr_node in children_contexts(expr_node.expr)
        for clause in sql_ast_clauses_from_expr(child_expr_node)
    ]


def sql_ast_exprs_from_orderless_list(
    orderless_list_node: Optional[SQLParser.OrderListContext],
) -> list[ASTNode]:
    """
    The grammar hackily reuses the orderList construct for group-bys.
    This function asserts they don't have directions and returns the AST nodes.
    """
    if orderless_list_node is None:
        return []

    assert isinstance(orderless_list_node, SQLParser.OrderListContext)

    order_expr_nodes = children_contexts(orderless_list_node.orderExpression)

    assert all(
        order_expr_node.direction() is None for order_expr_node in order_expr_nodes
    )

    return [sql_ast(order_expr_node.expr()) for order_expr_node in order_expr_nodes]


OrderDirection = Literal["ASC", "DESC"]


@dataclass
class OrderClause:
    direction: OrderDirection
    expr: ASTNode

    @classmethod
    def from_parse_tree(cls, parse_tree: ParseTree) -> ASTNode:
        assert isinstance(parse_tree, SQLParser.OrderExpressionContext)

        direction = parse_tree.direction()
        if direction is None or direction.ASC_SYMBOL() is not None:
            direction = "ASC"
        else:
            direction = "DESC"

        return cls(direction=direction, expr=sql_ast(parse_tree.expr()))


@dataclass
class QuerySpecNode(ASTNode):
    """
    querySpecification:
        SELECT_SYMBOL selectOption* selectItemList intoClause? fromClause? whereClause? groupByClause? havingClause? (
            {self.serverVersion >= 80000}? windowClause
        )?
    ;
    """

    select_options: list[ASTNode]
    select_exprs: list[SelectExpr]

    # We don't parse this out, as we don't really use it much.
    into_clause: Optional[ASTNode]

    # TODO: Real JOIN representation.
    from_clause: Optional[ASTNode]

    where_clauses: list[ASTNode]

    group_by_exprs: list[ASTNode]
    olap_options: Optional[ASTNode]

    having_clauses: list[ASTNode]

    window_clause: Optional[ASTNode]

    @classmethod
    def from_parse_tree(cls, parse_tree: ParseTree) -> ASTNode:

        assert isinstance(parse_tree, SQLParser.QuerySpecificationContext)

        select_options = [
            sql_ast(context) for context in children_contexts(parse_tree.selectOption)
        ]
        node_select_exprs = select_exprs(parse_tree.selectItemList())

        # TODO: Break this out / make an appropriate join datastructure.
        from_clause = optional_sql_ast(parse_tree.fromClause())

        where_clauses = []
        if parse_tree.whereClause() is not None:
            where_clauses = sql_ast_clauses_from_expr(parse_tree.whereClause().expr())

        group_by_clause = parse_tree.groupByClause()

        group_by_exprs = []
        olap_options = None
        if group_by_clause is not None:
            # The grammar hackily reuses the orderList construct for group-bys.
            # This function asserts they don't have directions.
            group_by_exprs = sql_ast_exprs_from_orderless_list(
                group_by_clause.orderList()
            )
            olap_options = optional_sql_ast(group_by_clause.olapOption())

        having_clauses = []
        if parse_tree.havingClause() is not None:
            having_clauses = sql_ast_clauses_from_expr(parse_tree.havingClause().expr())

        return cls(
            select_options=select_options,
            select_exprs=node_select_exprs,
            into_clause=optional_sql_ast(parse_tree.intoClause()),
            from_clause=from_clause,
            where_clauses=where_clauses,
            group_by_exprs=group_by_exprs,
            olap_options=olap_options,
            having_clauses=having_clauses,
            window_clause=optional_sql_ast(parse_tree.windowClause()),
        )


sql_parse_tree_ast_node_type: Dict[Type[ParserRuleContext], Type[ASTNode]] = {
    SQLParser.QuerySpecificationContext: QuerySpecNode,
}


def sql_ast(parse_tree: ParseTree) -> ASTNode:
    """
        The AST corresponding to the given parse tree.
    y
        Uses sql_parse_tree_ast_node_type to discover appropriate representations and falls
        back to the ParseTreeNode AST node.
    """
    ast_node_type = sql_parse_tree_ast_node_type.get(type(parse_tree), ParseTreeNode)

    return ast_node_type.from_parse_tree(parse_tree)


def optional_sql_ast(parse_tree: Optional[ParseTree]) -> Optional[ASTNode]:
    if parse_tree is not None:
        return sql_ast(parse_tree)
    else:
        return None
