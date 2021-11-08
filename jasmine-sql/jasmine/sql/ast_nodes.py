"""
SQL AST node implementations.

These are representations of various SQL expressions (SELECT queries, UNIONs, order expressions, etc).
See ast_base.py for details.

The sql_ast() function visits ParseTrees and encodes them as AST nodes using the list of available
representations (sql_parse_tree_node_type) and their cls.from_parse_tree() methods.
"""
from dataclasses import dataclass
from typing import Dict, Iterator, List, Literal, Optional, Type

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


# TODO: More intelligent representation.
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


JoinType = Literal[
    "INNER",
    "LEFT_OUTER",
    "RIGHT_OUTER",
]


def outer_join(join_type: JoinType) -> bool:
    return join_type in ("LEFT_OUTER", "RIGHT_OUTER")


@dataclass
class TableJoin(ASTNode):
    """
    Individual JOIN in a FROM clause.

    The first table is necessarily an INNER JOIN.
    """

    # JOIN'd table.
    # May either be a tableFactor or a DUAL_SYMBOL. May have subqueries or (a, b, c CROSS JOIN d) syntax.
    table_factor: ASTNode

    # JOIN type
    join_type: JoinType = "INNER"

    # JOIN condition.
    natural_join: bool = False  # Ugh, NATURAL JOINs

    on_clauses: list[ASTNode] | None = None
    using_columns: list[ASTNode] | None = None

    # Index hints.
    straight_inner_join: bool = (
        False  # STRAIGHT_INNER_JOIN is special syntax / an index hint.
    )

    def __post_init__(self):
        has_join_condition = bool(self.on_clauses or self.using_columns)

        assert (not self.straight_inner_join) or self.join_type == "INNER"
        if self.natural_join:
            assert not self.straight_inner_join, "NATURAL STRAIGHT_JOIN isn't a thing."
            assert (
                not has_join_condition
            ), "Natural JOINs cannot have ON or USING clauses."

        assert (
            not outer_join(self.join_type) or has_join_condition
        ), "OUTER JOINs must have ON or USING clauses."

    @classmethod
    def from_parse_tree(cls, node: ParseTree) -> ASTNode:
        """
        There's no clear 1-1 mapping here, as the necessary information for this is contextual and
        split among joinedTable and tableReferences.
        This node is created manually by JoinSpec's helpers.

        See JoinSpec's __doc__ for more details.
        """
        raise NotImplementedError


def sql_ast_identifiers_from_list(
    identifier_list: SQLParser.IdentifierListContext,
) -> list[ASTNode]:
    return [
        sql_ast(identifier)
        for identifier in children_contexts(identifier_list.identifier)
    ]


JoinTreeNodeContext = (
    SQLParser.TableReferenceListContext
    | SQLParser.TableReferenceContext
    | SQLParser.JoinedTableContext
    | SQLParser.TableFactorContext
    | TerminalNodeImpl
)


def join_type_table_join_args(joined_table: SQLParser.JoinedTableContext) -> dict:
    """
    Resolve *JoinType ParseTree into relevant keyword arguments for TableJoin.
    """
    assert isinstance(joined_table, SQLParser.JoinedTableContext)

    join_type = "INNER"
    direction = None
    is_straight_join = False

    natural_join = joined_table.naturalJoinType() is not None
    outer_join = joined_table.outerJoinType() is not None
    inner_join = joined_table.innerJoinType() is not None

    # Exactly one will be non-None.
    type_node = (
        joined_table.naturalJoinType()
        or joined_table.outerJoinType()
        or joined_table.innerJoinType()
    )

    if natural_join:
        left_join = type_node.LEFT_SYMBOL() is not None
        right_join = type_node.RIGHT_SYMBOL() is not None

        join_type = "OUTER" if (left_join or right_join) else "INNER"
        if join_type == "OUTER":
            direction = "LEFT" if left_join else "RIGHT"

    elif outer_join:
        join_type = "OUTER"
        direction = "LEFT" if type_node.LEFT_SYMBOL() is not None else "RIGHT"

    elif inner_join:
        is_straight_join = type_node.STRAIGHT_JOIN_SYMBOL() is not None

    else:
        raise ValueError(f"Unknown JOIN type: {joined_table}")

    straight_inner_join = (
        (join_type == "INNER")
        and not natural_join
        and type_node.STRAIGHT_JOIN_SYMBOL() is not None
    )

    if join_type == "OUTER":
        assert direction is not None
        join_type = f"{direction}_OUTER"

    return {
        "join_type": join_type,
        "natural_join": natural_join,
        "straight_inner_join": is_straight_join,
    }


def joined_table_table_join_args(joined_table: SQLParser.JoinedTableContext) -> dict:
    """
    Resolve a joinedTable ParseTree node into relevant keyword arguments for TableJoin.
    These will be pushed down and applied to the child TableRef.
    """
    assert isinstance(joined_table, SQLParser.JoinedTableContext)

    on_clauses = None
    if joined_table.expr() is not None:
        on_clauses = sql_ast_clauses_from_expr(joined_table.expr())

    using_columns = None
    if joined_table.identifierListWithParentheses() is not None:
        using_columns = sql_ast_identifiers_from_list(
            joined_table.identifierListWithParentheses().identifierList()
        )

    return {
        "on_clauses": on_clauses,
        "using_columns": using_columns,
        **join_type_table_join_args(joined_table),
    }


def table_joins(
    node: JoinTreeNodeContext, context_join_args: dict | None = None
) -> Iterator[TableJoin]:
    """
    Iterate over the table JOIN tree left-to-right and generate flat TableJoin entries.

    TableJoin entry information is spread throughout multiple layers of the tree.
    Handle this by having joinedTable push down context for the next TableJoin.
    (This information can get redirected to the first child of tableReference, which must
    be a tableFactor.)

    See JoinSpec for more context.

    >>> from jasmine.sql.ast_nodes import sql_ast  # For pytest double-import problems >:(
    >>> from jasmine.sql.parser.sql import sql_parser_from_str
    >>> from jasmine.sql.pretty_print import PrettyPrintVisitor

    >>> example_query = \"\"\"
    ...       FROM my_table
    ...       LEFT OUTER JOIN my_other_table
    ...         ON 1
    ...    NATURAL JOIN taaableee
    ...   STRAIGHT_JOIN tuble USING (col1, col2)
    ... \"\"\"
    >>> from_clause_node = sql_ast(sql_parser_from_str(example_query).fromClause())
    >>> print(PrettyPrintVisitor().pretty_print(from_clause_node))
        FROM my_table
        LEFT JOIN my_other_table
          ON 1
     NATURAL JOIN taaableee
    STRAIGHT_JOIN tuble USING (col1, col2)
    """
    match node:
        # Recursive cases:
        case SQLParser.TableReferenceListContext():
            for table_reference in children_contexts(node.tableReference):
                yield from table_joins(table_reference)

        case SQLParser.TableReferenceContext():
            # yield from table_joins(node.tableFactor(), context_join_args)
            for subnode in [node.tableFactor()] + children_contexts(node.joinedTable):
                yield from table_joins(subnode, context_join_args)

        case SQLParser.JoinedTableContext():
            # This parses out the join type / conditions and pushes them down one layer.
            yield from table_joins(
                node.tableReference() or node.tableFactor(),
                context_join_args=joined_table_table_join_args(node),
            )

        # Base cases:
        case SQLParser.TableFactorContext():
            yield TableJoin(
                table_factor=sql_ast(node),
                **(context_join_args or {}),
            )

        case TerminalNodeImpl():
            assert node.getText().upper() == "DUAL"

            yield TableJoin(table_factor=sql_ast(node))

        case _:
            raise ValueError(f"Unexpected node type: {node}")


@dataclass
class JoinSpec(ASTNode):
    """
    Specification of a FROM clause, effectively boiling down to a list of joins.

    Note: This asserts ODBC syntax is not used (see parser notes).

    FROM clauses are pretty messed up in the grammar.
    Generally, they have multiple recursive mechanisms and you just need to do a left-to-right
    walk to extract the sequence of references.

    Recursions:
    - tableReferenceList is put in the top level whenever there are comma-separated
        tables _anywhere_, and it absorbs the whole thing. It pretty much splits the JOINs by ','.
        It does _not_ include the "JOIN" / "FROM" / "NATURAL LEFT OUTER JOIN" / blah symbol.

    - tableReference is the workhorse: It has something table-name-y, then a list of "joinedTables"
        It does _not_ include the "JOIN" / "FROM" / "NATURAL LEFT OUTER JOIN" / blah symbol.

    - joinedTable is the backbone for joins with explicity symbols (IE, not comma joins.)
        It has a JOIN/INNER JOIN/OUTER RIGHT JOIN/NATURAL JOIN / etc keyword, then a __tableReference__.
        It _may_ then have a ON or USING clause.
        If this seems confusing, that's because it is: tableReference already has a list of joinedTables,
        yet joinedTables can recursively represent a sequence of JOINs like this:
            [joinedTable "LEFT JOIN" [tableReference "my_table"  [joinedTable "JOIN" [tableReference "blah" ...]]]]
        yet tableReference does this:
            [tableReference "first_table" [joinedTable "LEFT JOIN" [tableReference "blah"]] [joinedTable ...] ...]
        The first is chosen by the parser by default, but when joinedTables have ON / USING clauses,
        the latter is used (as the former cannot handle this case).

    Additionally:
    - tableFactor: A potentially subquery or "(a CROSS JOIN b)" filled slot where a table identifier goes.
    - outer/inner/naturalJoinTypes: Join types appropriate for each category of JOIN.
        Used by the parser to determine whether ON/USING are required or even allowed.
    - Index hints: Oh god. I just associate them with the table join in the tableFactor.

    """

    table_joins: list[TableJoin]

    @classmethod
    def from_parse_tree(cls, node: ParseTree) -> ASTNode:
        assert isinstance(node, SQLParser.FromClauseContext)

        child_node = node.DUAL_SYMBOL() or node.tableReferenceList()

        return cls(table_joins=list(table_joins(child_node)))


OrderDirection = Literal["ASC", "DESC"]


@dataclass
class OrderExpr:
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
    from_clause: JoinSpec

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

        from_clause = sql_ast(parse_tree.fromClause())

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
    SQLParser.FromClauseContext: JoinSpec,
}


def sql_ast(parse_tree: ParseTree) -> ASTNode:
    """
    The AST corresponding to the given parse tree.

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
