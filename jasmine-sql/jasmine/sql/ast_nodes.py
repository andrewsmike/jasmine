"""
Semantic representation of parse trees for query manipulation, analysis, and pretty printing.

These are representations of various SQL expressions (SELECT queries, UNIONs, order expressions, etc).

ASTs discard irrelevant grammatical constructs / separations and convert everything
to more standard python types.

The sql_ast() function visits ParseTrees and encodes them as AST nodes using the list of available
representations (sql_parse_tree_node_type) and singledispatch'd sql_ast submethods.
"""
from dataclasses import dataclass, fields
from functools import singledispatch
from pprint import pformat
from typing import Iterator, Literal, Optional, Type

from antlr4.ParserRuleContext import ParserRuleContext
from antlr4.tree.Tree import TerminalNodeImpl

from jasmine.sql.parser.sql import (
    ParseTree,
    SQLParser,
    children_contexts,
    sql_tree_from_str,
)


class ASTNode:
    """
    A semantic representation of a parse tree.
    """

    def node_type_name(self) -> str:
        return self.__class__.__name__


@dataclass
class MockNode(ASTNode):
    text: str

    def from_parse_tree(cls, parse_tree: Optional[ParseTree]) -> ASTNode:
        raise RuntimeError


def mock_node(text: str):
    return MockNode(text)


@dataclass
class ParseTreeNode(ASTNode):
    """
    An AST node that is just a parse tree node.

    This effectively forms a scaffold over "unrepresented" sections of a the
    parse tree and copies their structure.
    """

    base_node: ParseTree
    children: list[ASTNode]

    def node_type_name(self) -> str:
        node_type_name = type(self.base_node).__name__
        if node_type_name.endswith("Context"):
            node_type_name = node_type_name[: -len("Context")]

        return "raw:" + node_type_name


ParserSymbol = int
ASTNodePattern = Type[ASTNode] | Type[ParserRuleContext] | ParserSymbol


def node_matches(node: ASTNode, node_pattern: ASTNodePattern) -> bool:
    """
    Is the given AST node one of:
    - An instance of the given type directly
    - A ParseTreeNode with a base_node of the given SQLParser context type
    - A ParseTreeNode of a terminal node with the given symbol.

    This is useful for interacting with mixed-type children.
    """
    return (
        (
            isinstance(node_pattern, type)
            and issubclass(node_pattern, ASTNode)
            and isinstance(node, node_pattern)
        )
        or (
            isinstance(node_pattern, type)
            and issubclass(node_pattern, ParserRuleContext)
            and isinstance(node, ParseTreeNode)
            and isinstance(node.base_node, node_pattern)
        )
        or (
            isinstance(node_pattern, int)
            and isinstance(node, ParseTreeNode)
            and isinstance(node.base_node, TerminalNodeImpl)
            and node.base_node.symbol.type == node_pattern
        )
    )


def matching_nodes(
    nodes: list[ASTNode], node_patterns: set[ASTNodePattern]
) -> list[ASTNode]:
    return [
        node
        for node in nodes
        if any(node_matches(node, node_pattern) for node_pattern in node_patterns)
    ]


@dataclass
class SqlProgram(ASTNode):
    queries: list[ASTNode]


@dataclass
class TableRef(ASTNode):
    """
    Doesn't currently resolve anything / unquote escaped identifiers / etc.
    See SelectExpr for tests / examples.

    TODO: Smarter format.
    """

    ref: str


@dataclass
class SelectExpr(ASTNode):
    """
    A SELECT expression, including wildcards.

    A naked * is currently represented as a literal token in the SELECT list. Should be brought here
    eventually.

    >>> print(sql_ast_repr("SELECT my_table.`a`"))
    {'queries': [{'select_exprs': [{'expr': ('raw', 'my_table.`a`'),
                                    'select_expr_type': 'expr',
                                    'type': 'SelectExpr'}],
                  'type': 'QuerySpecNode'}],
     'type': 'SqlProgram'}

    >>> print(sql_ast_repr("SELECT my_table.*"))
    {'queries': [{'select_exprs': [{'select_expr_type': 'table_star',
                                    'star_table': {'ref': 'my_table',
                                                   'type': 'TableRef'},
                                    'type': 'SelectExpr'}],
                  'type': 'QuerySpecNode'}],
     'type': 'SqlProgram'}

    >>> print(sql_ast_repr("SELECT `my_table`.*"))
    {'queries': [{'select_exprs': [{'select_expr_type': 'table_star',
                                    'star_table': {'ref': '`my_table`',
                                                   'type': 'TableRef'},
                                    'type': 'SelectExpr'}],
                  'type': 'QuerySpecNode'}],
     'type': 'SqlProgram'}

    >>> print(sql_ast_repr("SELECT *"))
    {'queries': [{'select_exprs': [('raw', '*')], 'type': 'QuerySpecNode'}],
     'type': 'SqlProgram'}
    """

    select_expr_type: Literal["expr", "table_star"]

    expr: Optional[ASTNode] = None
    expr_alias: Optional[str] = None

    star_table: Optional[TableRef] = None


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

    See JoinSpec for tests / examples.
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
        """
        Verify JOIN conditions do not conflict.
        """
        has_join_condition = bool(self.on_clauses or self.using_columns)

        assert (not self.straight_inner_join) or self.join_type == "INNER"
        if self.natural_join:
            assert not self.straight_inner_join, "NATURAL STRAIGHT_JOIN isn't a thing."
            assert (
                not has_join_condition
            ), "Natural JOINs cannot have ON or USING clauses."
        else:
            assert (
                not outer_join(self.join_type) or has_join_condition
            ), "OUTER JOINs must have ON or USING clauses."


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

    General case:
    >>> print(sql_ast_repr("SELECT 1 FROM a JOIN b LEFT JOIN c ON 1"))
    {'queries': [{'from_clause': {'table_joins': [{'join_type': 'INNER',
                                                   'table_factor': ('raw', 'a'),
                                                   'type': 'TableJoin'},
                                                  {'join_type': 'INNER',
                                                   'table_factor': ('raw', 'b'),
                                                   'type': 'TableJoin'},
                                                  {'join_type': 'LEFT_OUTER',
                                                   'on_clauses': [('raw', '1')],
                                                   'table_factor': ('raw', 'c'),
                                                   'type': 'TableJoin'}],
                                  'type': 'JoinSpec'},
                  'select_exprs': [{'expr': ('raw', '1'),
                                    'select_expr_type': 'expr',
                                    'type': 'SelectExpr'}],
                  'type': 'QuerySpecNode'}],
     'type': 'SqlProgram'}

    NATURAL and RIGHT joins:
    >>> print(sql_ast_repr("SELECT 1 FROM a NATURAL RIGHT JOIN b"))
    {'queries': [{'from_clause': {'table_joins': [{'join_type': 'INNER',
                                                   'table_factor': ('raw', 'a'),
                                                   'type': 'TableJoin'},
                                                  {'join_type': 'RIGHT_OUTER',
                                                   'natural_join': True,
                                                   'table_factor': ('raw', 'b'),
                                                   'type': 'TableJoin'}],
                                  'type': 'JoinSpec'},
                  'select_exprs': [{'expr': ('raw', '1'),
                                    'select_expr_type': 'expr',
                                    'type': 'SelectExpr'}],
                  'type': 'QuerySpecNode'}],
     'type': 'SqlProgram'}

    Testing out STRAIGHT_JOIN and that weird JOIN syntax:
    >>> print(sql_ast_repr("SELECT 1 FROM a STRAIGHT_JOIN b JOIN c ON bleh ON blah"))
    {'queries': [{'from_clause': {'table_joins': [{'join_type': 'INNER',
                                                   'table_factor': ('raw', 'a'),
                                                   'type': 'TableJoin'},
                                                  {'join_type': 'INNER',
                                                   'on_clauses': [('raw', 'blah')],
                                                   'straight_inner_join': True,
                                                   'table_factor': ('raw', 'b'),
                                                   'type': 'TableJoin'},
                                                  {'join_type': 'INNER',
                                                   'on_clauses': [('raw', 'bleh')],
                                                   'table_factor': ('raw', 'c'),
                                                   'type': 'TableJoin'}],
                                  'type': 'JoinSpec'},
                  'select_exprs': [{'expr': ('raw', '1'),
                                    'select_expr_type': 'expr',
                                    'type': 'SelectExpr'}],
                  'type': 'QuerySpecNode'}],
     'type': 'SqlProgram'}
    """

    table_joins: list[TableJoin]


OrderDirection = Literal["ASC", "DESC"]


@dataclass
class OrderExpr(ASTNode):
    direction: OrderDirection
    expr: ASTNode


@dataclass
class QuerySpecNode(ASTNode):
    """
    Core SQL query. Includes SELECT, FROM, WHERE, GROUP BY, HAVING, WINDOW clauses, and SELECT, OLAP options.

    >>> print(sql_ast_repr("SELECT DISTINCT a, b FROM my_table NATURAL JOIN other_table WHERE a = 3 GROUP BY 1 WITH ROLLUP HAVING 1"))
    {'queries': [{'from_clause': {'table_joins': [{'join_type': 'INNER',
                                                   'table_factor': ('raw',
                                                                    'my_table'),
                                                   'type': 'TableJoin'},
                                                  {'join_type': 'INNER',
                                                   'natural_join': True,
                                                   'table_factor': ('raw',
                                                                    'other_table'),
                                                   'type': 'TableJoin'}],
                                  'type': 'JoinSpec'},
                  'group_by_exprs': [('raw', '1')],
                  'having_clauses': [('raw', '1')],
                  'olap_options': ('raw', 'WITHROLLUP'),
                  'select_exprs': [{'expr': ('raw', 'a'),
                                    'select_expr_type': 'expr',
                                    'type': 'SelectExpr'},
                                   {'expr': ('raw', 'b'),
                                    'select_expr_type': 'expr',
                                    'type': 'SelectExpr'}],
                  'select_options': [('raw', 'DISTINCT')],
                  'type': 'QuerySpecNode',
                  'where_clauses': [('raw', 'a=3')]}],
     'type': 'SqlProgram'}
    """

    select_options: list[ASTNode]
    select_exprs: list[SelectExpr]

    # We don't parse this out, as we don't really use it much.
    into_clause: Optional[ASTNode]

    from_clause: JoinSpec

    where_clauses: list[ASTNode]

    group_by_exprs: list[ASTNode]
    olap_options: Optional[ASTNode]

    having_clauses: list[ASTNode]

    window_clause: Optional[ASTNode]


@dataclass
class UnionNode(ASTNode):
    """
    There are a few players in this game:
    - selectStatement: Top level. Paren'd, queryExpression + optional locking, or selectStatementWithInto.
    - queryExpressionParens: Recursive paren-wrapped selectStatement, but without selectStatementWithInto.
        Optionally with lockingClauseList (ie FOR SHARE)

    - queryExpression: with/CTE, (queryExpressionBody | paren'd queryExpression w/ opt locks), order, limit, procedureAnalyseClause
    - queryExpressionBody: Sequence of (queryPrimary | paren'd queryExpression w/ opt locks) with unions in between
        This largely handles UNION unrolling. It is subjected to parent WITH CTE / ORDER BY / LIMIT clauses, but allows
        the same clauses in its children.

    - queryPrimary: Either a normal query sans CTE/order/limit (querySpecification), or one of two special syntaxes.
        This is the "core expression". It handles most of the complicated stuff.

    My aliases:
    - selectStatement: Passthrough. Drop parens, assert no locking.
    - queryExpressionParams: Passthrough. Drop parens, assert no locking.

    - queryExpression: CTEOrderLimitNode
    - queryExpressionBody: UnionNode
        Note: This must propagate through queryExpressionParens / no-op queryExpressions.
    - queryPrimary: QuerySpecNode | ASTNode

    Thoughts:
    - ORDER BY / LIMIT can't be reduced in most circumstances.
    - I think WITH clauses can distribute in all circumstances, but that's an optimization.
    - UNIONs can't reduce, ORDER BY / LIMITs can't distribute in.

    So... yeah. These need their own nodes.
    Question: Do I pack it into the existing complex node type and have it have many dummy-nodes, or
    do I make another type?

    Good news: WITH / ORDER BY / LIMIT are unambiguous defined - they require parens around
        subexprs with the args.

    UNIONs may either pass duplicate rows unaffected, or deduplicate their final result.
    They default to UNION DISTINCT (UNION ALL being the alternative.)
    When you have a chain of UNIONs, they're left recursive. This has the nice property that
    any UNION [DISTINCT] affects all UNIONs earlier in the sequence.
    To represent this, we store the number of subqueries that aren't deduplicated.
    These are always at the end of the list (subqueries[-count:]), and the number ranges
    from zero to n.

    >>> print(sql_ast_repr("SELECT 1 UNION SELECT 2 UNION ALL (SELECT 2 FROM a LIMIT 1) ORDER BY 3"))
    {'queries': [{'order_by_clauses': [{'direction': 'ASC',
                                        'expr': ('raw', '3'),
                                        'type': 'OrderExpr'}],
                  'subquery': {'subqueries': [{'select_exprs': [{'expr': ('raw',
                                                                          '1'),
                                                                 'select_expr_type': 'expr',
                                                                 'type': 'SelectExpr'}],
                                               'type': 'QuerySpecNode'},
                                              {'select_exprs': [{'expr': ('raw',
                                                                          '2'),
                                                                 'select_expr_type': 'expr',
                                                                 'type': 'SelectExpr'}],
                                               'type': 'QuerySpecNode'},
                                              {'limit_options': ('raw', '1'),
                                               'subquery': {'from_clause': {'table_joins': [{'join_type': 'INNER',
                                                                                             'table_factor': ('raw',
                                                                                                              'a'),
                                                                                             'type': 'TableJoin'}],
                                                                            'type': 'JoinSpec'},
                                                            'select_exprs': [{'expr': ('raw',
                                                                                       '2'),
                                                                              'select_expr_type': 'expr',
                                                                              'type': 'SelectExpr'}],
                                                            'type': 'QuerySpecNode'},
                                               'type': 'CTEOrderLimitNode'}],
                               'type': 'UnionNode',
                               'unfiltered_subqueries': 1},
                  'type': 'CTEOrderLimitNode'}],
     'type': 'SqlProgram'}

    >>> print(sql_ast_repr("SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3"))
    {'queries': [{'subqueries': [{'select_exprs': [{'expr': ('raw', '1'),
                                                    'select_expr_type': 'expr',
                                                    'type': 'SelectExpr'}],
                                  'type': 'QuerySpecNode'},
                                 {'select_exprs': [{'expr': ('raw', '2'),
                                                    'select_expr_type': 'expr',
                                                    'type': 'SelectExpr'}],
                                  'type': 'QuerySpecNode'},
                                 {'select_exprs': [{'expr': ('raw', '3'),
                                                    'select_expr_type': 'expr',
                                                    'type': 'SelectExpr'}],
                                  'type': 'QuerySpecNode'}],
                  'type': 'UnionNode',
                  'unfiltered_subqueries': 3}],
     'type': 'SqlProgram'}

    >>> print(sql_ast_repr("SELECT 1 UNION ALL SELECT 2 UNION DISTINCT SELECT 3"))
    {'queries': [{'subqueries': [{'select_exprs': [{'expr': ('raw', '1'),
                                                    'select_expr_type': 'expr',
                                                    'type': 'SelectExpr'}],
                                  'type': 'QuerySpecNode'},
                                 {'select_exprs': [{'expr': ('raw', '2'),
                                                    'select_expr_type': 'expr',
                                                    'type': 'SelectExpr'}],
                                  'type': 'QuerySpecNode'},
                                 {'select_exprs': [{'expr': ('raw', '3'),
                                                    'select_expr_type': 'expr',
                                                    'type': 'SelectExpr'}],
                                  'type': 'QuerySpecNode'}],
                  'type': 'UnionNode'}],
     'type': 'SqlProgram'}
    """

    subqueries: list[ASTNode]

    unfiltered_subqueries: int = 0


@dataclass
class CTESubqueryNode(ASTNode):
    """
    >>> print(sql_ast_repr("WITH RECURSIVE my_cte (a, b, c) AS (SELECT 1) SELECT 1 FROM blah"))
    {'queries': [{'cte_subqueries': [{'allow_recursion': True,
                                      'column_names': ['a', 'b', 'c'],
                                      'name': 'my_cte',
                                      'query': {'select_exprs': [{'expr': ('raw',
                                                                           '1'),
                                                                  'select_expr_type': 'expr',
                                                                  'type': 'SelectExpr'}],
                                                'type': 'QuerySpecNode'},
                                      'type': 'CTESubqueryNode'}],
                  'subquery': {'from_clause': {'table_joins': [{'join_type': 'INNER',
                                                                'table_factor': ('raw',
                                                                                 'blah'),
                                                                'type': 'TableJoin'}],
                                               'type': 'JoinSpec'},
                               'select_exprs': [{'expr': ('raw', '1'),
                                                 'select_expr_type': 'expr',
                                                 'type': 'SelectExpr'}],
                               'type': 'QuerySpecNode'},
                  'type': 'CTEOrderLimitNode'}],
     'type': 'SqlProgram'}
    """

    name: str
    column_names: list[str] | None
    query: ASTNode
    allow_recursion: bool


@dataclass
class CTEOrderLimitNode(ASTNode):
    """
    The SQL grammar places these three operations together in their own layer.
    This has semantic implications, and thus this is distinct from the query spec node.

    >>> print(sql_ast_repr("SELECT 1 ORDER BY 1 LIMIT 1;"))
    {'queries': [{'limit_options': ('raw', '1'),
                  'order_by_clauses': [{'direction': 'ASC',
                                        'expr': ('raw', '1'),
                                        'type': 'OrderExpr'}],
                  'subquery': {'select_exprs': [{'expr': ('raw', '1'),
                                                 'select_expr_type': 'expr',
                                                 'type': 'SelectExpr'}],
                               'type': 'QuerySpecNode'},
                  'type': 'CTEOrderLimitNode'}],
     'type': 'SqlProgram'}
    """

    cte_subqueries: list[CTESubqueryNode] | None
    subquery: ASTNode
    order_by_clauses: list[OrderExpr] | None
    limit_options: ASTNode | None  # TODO: Actually represent this.


@singledispatch
def sql_ast(parse_tree: None) -> ASTNode:
    """
    The AST corresponding to the given parse tree.
    """
    return None


@sql_ast.register
def parse_tree_sql_ast(parse_tree: ParseTree) -> ASTNode:

    children_nodes = [sql_ast(child) for child in getattr(parse_tree, "children", [])]

    return ParseTreeNode(parse_tree, children_nodes)


@sql_ast.register
def statement_sql_ast(parse_tree: SQLParser.StatementContext) -> ASTNode:

    subquery = parse_tree.simpleStatement()
    assert (
        subquery is not None
    ), "Transaction and procedure statements are not supported."

    return sql_ast(subquery)


@sql_ast.register
def simple_statement_sql_ast(parse_tree: SQLParser.SimpleStatementContext) -> ASTNode:

    subquery = parse_tree.selectStatement()
    assert subquery is not None, "Only read-only SELECT statements are supported."

    return sql_ast(subquery)


@sql_ast.register
def select_statement_sql_ast(parse_tree: SQLParser.SelectStatementContext) -> ASTNode:
    assert (
        parse_tree.selectStatementWithInto() is None
    ), "Mutating SELECT INTO clauses aren't supported."
    assert (
        parse_tree.lockingClauseList() is None
    ), "SELECT locking clauses aren't currently supported."

    subquery = parse_tree.queryExpression() or parse_tree.queryExpressionParens()
    assert subquery is not None

    return sql_ast(subquery)


@sql_ast.register
def query_expression_sql_ast(parse_tree: SQLParser.QueryExpressionContext) -> ASTNode:
    assert (
        parse_tree.procedureAnalyseClause() is None
    ), "PROCEDURE ANALYZE is not supported."

    cte_subqueries = None
    if parse_tree.withClause():
        with_recursive = parse_tree.withClause().RECURSIVE_SYMBOL() is not None

        cte_subqueries = [
            sql_ast(common_table_expr, allow_recursion=with_recursive)
            for common_table_expr in children_contexts(
                parse_tree.withClause().commonTableExpression
            )
        ]

    order_by_clauses = None
    if parse_tree.orderClause() is not None:
        order_by_clauses = [
            sql_ast(child)
            for child in children_contexts(
                parse_tree.orderClause().orderList().orderExpression
            )
        ]

    limit_options = None
    if parse_tree.limitClause() is not None:
        # TODO: Real representation.
        limit_options = sql_ast(parse_tree.limitClause().limitOptions())

    subquery = parse_tree.queryExpressionBody() or parse_tree.queryExpressionParens()
    assert subquery is not None
    subquery_ast = sql_ast(subquery)

    if cte_subqueries is None and order_by_clauses is None and limit_options is None:
        return subquery_ast

    else:
        return CTEOrderLimitNode(
            cte_subqueries=cte_subqueries,
            subquery=subquery_ast,
            order_by_clauses=order_by_clauses,
            limit_options=limit_options,
        )


@sql_ast.register
def common_table_expr_sql_ast(
    parse_tree: SQLParser.CommonTableExpressionContext,
    allow_recursion: bool = False,
) -> ASTNode:
    name = parse_tree.identifier().getText()

    column_names = None
    if parse_tree.columnInternalRefList() is not None:
        column_names = [
            column_ref.getText()
            for column_ref in children_contexts(
                parse_tree.columnInternalRefList().columnInternalRef
            )
        ]

    query = sql_ast(parse_tree.subquery().queryExpressionParens())

    return CTESubqueryNode(
        name=name,
        column_names=column_names,
        query=query,
        allow_recursion=allow_recursion,
    )


@sql_ast.register
def query_expression_parens_sql_ast(
    parse_tree: SQLParser.QueryExpressionParensContext,
) -> ASTNode:
    """
    This is a syntactic construct and is, semantically, a pass-through.
    We assert no locking expressions; they aren't supported.
    """
    assert (
        parse_tree.lockingClauseList() is None
    ), "SELECT locking clauses aren't currently supported."

    child_subquery = parse_tree.queryExpressionParens() or parse_tree.queryExpression()
    assert child_subquery is not None

    return sql_ast(child_subquery)


@sql_ast.register
def table_wild_sql_ast(parse_tree: SQLParser.TableWildContext) -> ASTNode:

    name = ".".join(
        ref_path_part.getText()
        for ref_path_part in children_contexts(parse_tree.identifier)
    )

    return TableRef(ref=name)


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


@sql_ast.register
def from_clause_sql_ast(parse_tree: SQLParser.FromClauseContext) -> ASTNode:

    child_node = parse_tree.DUAL_SYMBOL() or parse_tree.tableReferenceList()

    return JoinSpec(table_joins=list(table_joins(child_node)))


@sql_ast.register
def order_expr_sql_ast(parse_tree: SQLParser.OrderExpressionContext) -> ASTNode:

    direction = parse_tree.direction()
    if direction is None or direction.ASC_SYMBOL() is not None:
        direction = "ASC"
    else:
        direction = "DESC"

    return OrderExpr(direction=direction, expr=sql_ast(parse_tree.expr()))


def select_exprs(
    select_expr_node: SQLParser.SelectItemListContext,
) -> list[ASTNode]:

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
     'my_column = other_table.other_column',
     "(4 IS NULL OR CONCAT('Hi', 'yo') = 'Hiyo')"]
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


@sql_ast.register
def query_spec_sql_ast(parse_tree: SQLParser.QuerySpecificationContext) -> ASTNode:

    select_options = [
        sql_ast(context) for context in children_contexts(parse_tree.selectOption)
    ]
    assert parse_tree.selectItemList() is not None
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
        group_by_exprs = sql_ast_exprs_from_orderless_list(group_by_clause.orderList())
        olap_options = sql_ast(group_by_clause.olapOption())

    having_clauses = []
    if parse_tree.havingClause() is not None:
        having_clauses = sql_ast_clauses_from_expr(parse_tree.havingClause().expr())

    return QuerySpecNode(
        select_options=select_options,
        select_exprs=node_select_exprs,
        into_clause=sql_ast(parse_tree.intoClause()),
        from_clause=from_clause,
        where_clauses=where_clauses,
        group_by_exprs=group_by_exprs,
        olap_options=olap_options,
        having_clauses=having_clauses,
        window_clause=sql_ast(parse_tree.windowClause()),
    )


def is_terminal(node: ParseTree, symbol: int | None) -> bool:
    return isinstance(node, TerminalNodeImpl) and (
        symbol is None or node.symbol.type == symbol
    )


def union_sequence_unfiltered_subqueries(children: list[ParseTree]) -> int:
    """
    The number of subqueries in a sequence of UNION statements whose results are
    returned without deduplication. These subqueries are all at the end of the sequence,
    as UNION statements are left-recursive.

    See: https://dev.mysql.com/doc/refman/8.0/en/union.html#union-distinct-all
    Also see UnionNode for more details.

    Input children are of the format "<subquery> (UNION [ALL|DISTINCT] <subquery>)*".

    Examples:
        A distinct B  => 0
        A all B distinct C => 0
        A distinct B all C => 1
        A all B => 2
        A all B all C => 3

    Scanning from left-to-right, every UNION ALL adds one to the counter (except the first, which adds two),
    and any UNION DISTINCT resets the counter.
    """
    first_union = True
    unfiltered_subqueries = 0
    for child, next_child in zip(children, children[1:]):
        if not is_terminal(child, SQLParser.UNION_SYMBOL):
            continue

        is_any_symbol = isinstance(next_child, SQLParser.UnionOptionContext) and (
            next_child.ALL_SYMBOL() is not None
        )
        if is_any_symbol:
            unfiltered_subqueries += 2 if first_union else 1
        else:
            unfiltered_subqueries = 0

        first_union = False

    return unfiltered_subqueries


@sql_ast.register
def query_expression_body_sql_ast(
    parse_tree: SQLParser.QueryExpressionBodyContext,
) -> ASTNode:

    children = parse_tree.children

    # If this is a pass-through node, don't bother representing it.
    if len(children) == 1:
        (subquery,) = children
        assert isinstance(
            subquery,
            (SQLParser.QueryPrimaryContext, SQLParser.QueryExpressionParensContext),
        )

        return sql_ast(subquery)

    subqueries = [
        sql_ast(child)
        for child in children
        if isinstance(
            child,
            (SQLParser.QueryExpressionParensContext, SQLParser.QueryPrimaryContext),
        )
    ]

    return UnionNode(
        subqueries=subqueries,
        unfiltered_subqueries=union_sequence_unfiltered_subqueries(children),
    )


@sql_ast.register
def select_item_sql_ast(parse_tree: SQLParser.SelectItemContext) -> ASTNode:

    if parse_tree.tableWild() is not None:
        return SelectExpr(
            select_expr_type="table_star", star_table=sql_ast(parse_tree.tableWild())
        )
    else:
        assert parse_tree.expr() is not None
        alias = parse_tree.selectAlias()
        if alias is not None:
            alias = alias.identifier() or alias.textStringLiteral()

        return SelectExpr(
            select_expr_type="expr",
            expr=sql_ast(parse_tree.expr()),
            expr_alias=sql_ast(alias),
        )


@sql_ast.register
def sql_program_ast_node(parse_node: SQLParser.SqlProgramContext) -> ASTNode:
    return SqlProgram(
        queries=[
            sql_ast(child_query)
            for child_query in children_contexts(parse_node.statement)
        ]
    )


@sql_ast.register
def query_primary_sql_ast(parse_node: SQLParser.QueryPrimaryContext) -> ASTNode:
    assert len(parse_node.children) == 1
    return sql_ast(parse_node.children[0])


# For easy visualization / doctesting.


@singledispatch
def ast_repr(value):
    return value


@ast_repr.register
def parse_tree_ast_repr(value: ParseTreeNode):
    return ("raw", value.base_node.getText())


@ast_repr.register
def node_ast_repr(value: ASTNode):
    return ast_repr(
        {
            "type": value.node_type_name(),
            **{
                field.name: getattr(value, field.name, None)
                for field in fields(value.__class__)
            },
        }
    )


@ast_repr.register
def dict_ast_repr(value: dict):
    return {
        key: subvalue_repr
        for key, subvalue in value.items()
        for subvalue_repr in (ast_repr(subvalue),)
        if subvalue_repr
    }


@ast_repr.register
def list_ast_repr(value: list):
    return [ast_repr(subvalue) for subvalue in value]


def sql_ast_repr(sql_query: str) -> str:
    parse_tree = sql_tree_from_str(sql_query)

    return pformat(ast_repr(sql_ast(parse_tree)))


# - WITH CTE, UNION, ORDER BY, LIMIT [CHECK]
# - comments-after-statement?
# - Incremental improvements: caps'ing symbols, [converting implicit joins to explicit], [reordering ON clauses].
# - Symbol capitalization visitor?
# Uncorrelated subqueries: Just align the last character.
# Correlated / inline subqueries / IN() clause subqueries: ?!?
