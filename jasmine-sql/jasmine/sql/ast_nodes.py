"""
AST representations of various SQL expressions (SELECT queries, UNIONs, order lists, etc)
and a visitor function for generating ASTs from ParseTrees directly.

See ast_base.py for an explanation of what these ASTs represent and do.

The sql_ast() function visits ParseTrees and encodes them as AST nodes using the
list of available representations (sql_parse_tree_node_type) and their
cls.from_parse_tree() methods. These can be serialized back to ParseTrees using
the representations' parse_tree() methods.

Current representations:
- ParserNode: An AST node that's just a parse tree node. This is the default node type.
- OrderExprNode: An AST node for an orderExpr ("date DESC").
- OrderClauseNode: An AST node for an orderClause in the parse tree ("ORDER BY a DESC, b").


TODO: Handle queryExpressions by breaking them into two groups:
- UnionExprTree: queryExpressions which have UNIONs at the top level.
    These represent the union of a set of queryExpressions with optional
    WITH, ORDER, and LIMIT clause.
- QueryExprTree: queryExpressions without UNIONs in them.
    These represent the normal flat query expression and reach into their various
    children for normal metadata.


>>> from jasmine.sql.parser.sql import sql_tree_from_str
>>> from jasmine.sql.pretty_print import pretty_sql_str_from_tree, sql_tree_str
>>> from jasmine.sql.ast_nodes import sql_ast

>>> tree = sql_tree_from_str("SELECT 1 FROM my_db a LEFT JOIN blah b ON a.b_id = b.id ORDER BY a.day;")
>>> parse_tree = tree.statement(0).simpleStatement().selectStatement().queryExpression()
>>> print(pretty_sql_str_from_tree(parse_tree)["multiline"])
SELECT 1
  FROM my_db a    LEFT JOIN blah b
    ON a.b_id = b.id
 ORDER BY a.day

>>> ast = sql_ast(parse_tree)
>>> retranslated_tree = ast.parse_tree()
>>> print(pretty_sql_str_from_tree(retranslated_tree, record_comments=False)["multiline"])
SELECT 1
  FROM my_db a    LEFT JOIN blah b
    ON a.b_id = b.id
 ORDER BY a.day ASC
"""
from dataclasses import dataclass
from typing import Dict, List, Literal, Optional, Type

from antlr4.ParserRuleContext import ParserRuleContext
from antlr4.tree.Tree import TerminalNodeImpl

from jasmine.sql.ast_base import (
    ASTNode,
    ParseTreeTemplate,
    list_joined,
    parse_tree_node,
)
from jasmine.sql.parser.sql import ParseTree, SQLParser, children_contexts


def sql_ast(parse_tree: ParseTree) -> ASTNode:
    """
    The AST corresponding to the given parse tree.

    Uses sql_parse_tree_node_type to discover appropriate representations and falls
    back on the ParserNode AST node.
    """
    parse_tree_type = type(parse_tree)
    if parse_tree_type in sql_parse_tree_node_type:
        return sql_parse_tree_node_type[parse_tree_type].from_parse_tree(parse_tree)
    else:
        return ParserNode.from_parse_tree(parse_tree)


@dataclass
class ParserNode(ASTNode):
    """
    An AST node that is just a parse tree node.
    Allows for nontrivial AST subtrees and uses sql_ast for parsing.

    This effectively forms a scaffold over "unrepresented" sections of a the
    parse tree and copies their structure.
    """

    base_node: ParseTree
    children: List[ASTNode]

    def parse_tree(self):
        if isinstance(self.base_node, TerminalNodeImpl):
            return self.base_node

        assert len(self.children) == len(
            self.base_node.children
        ), "ParserNode node's children need to match the base node's children."

        children_nodes = [child.parse_tree() for child in self.children]

        return parse_tree_node(
            type(self.base_node),
            children_nodes,
        )

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


@dataclass
class OrderExprNode(ASTNode):

    expr: ASTNode
    direction: Literal["ASC", "DESC"]

    @classmethod
    def from_parse_tree(cls, parse_tree: ParseTree) -> ASTNode:
        direction = parse_tree.direction()
        if direction is None or direction.ASC_SYMBOL() is not None:
            direction = "ASC"
        else:
            direction = "DESC"

        return cls(
            expr=sql_ast(parse_tree.expr()),
            direction=direction,
        )

    def parse_tree_template(self) -> ParseTreeTemplate:
        return (
            "orderExpression",
            [self.expr.parse_tree(), ("direction", ["ASC_SYMBOL"])],
        )


@dataclass
class OrderListNode(ASTNode):
    order_exprs: List[OrderExprNode]

    @classmethod
    def from_parse_tree(cls, parse_tree: ParseTree) -> ASTNode:
        return cls(
            order_exprs=[
                sql_ast(child_ctx)
                for child_ctx in children_contexts(parse_tree.orderExpression)
            ],
        )

    def parse_tree_template(self) -> ParseTreeTemplate:
        return (
            "orderList",
            list_joined(
                "COMMA_SYMBOL", [expr.parse_tree() for expr in self.order_exprs]
            ),
        )


@dataclass
class OrderClauseNode(ASTNode):

    order_expr_list: OrderListNode

    @classmethod
    def from_parse_tree(cls, parse_tree: ParseTree) -> ASTNode:
        return cls(order_expr_list=sql_ast(parse_tree.orderList()))

    def parse_tree_template(self) -> ParseTreeTemplate:
        return (
            "orderClause",
            [
                "ORDER_SYMBOL",
                "BY_SYMBOL",
                self.order_expr_list.parse_tree(),
            ],
        )


sql_parse_tree_node_type: Dict[Type[ParserRuleContext], Type[ASTNode]] = {
    SQLParser.OrderExpressionContext: OrderExprNode,
    SQLParser.OrderClauseContext: OrderClauseNode,
}
