"""
Autoformatter for MySQL queries.

# Handling enumerated items.
There are a variety of ways to handle enumerated items and deep expression trees.
Here we outline a number of strategies and the situations in which we use them.

Generally, we use either a purely inline rendering (for small expressions) and
multiline-after for longer queries.

## Function arguments
- inline:
    SELECT CONCAT(my_thing, other_thing, blah)

- multiline-single (unused):
    SELECT CONCAT(
               my_thing, other_thing, blah
           )

- multiline-after (unused):
    SELECT CONCAT(my_thing,
                  other_thing,
                  blah)

- multiline-under:
    SELECT CONCAT(
               my_thing,
               other_thing,
               blah
           )

- multiline-under-indent-reset (unused):
    SELECT CONCAT(
        my_thing,
        other_thing,
        blah
    )

## Comma separated expressions
- inline:
    SELECT A, B, C, D, E

- multiline-single (unused)
    SELECT
        A, B, C, D, E

- multiline-after:
    SELECT A,
           B,
           C,
           D,
           E

- multiline-under (unused):
    SELECT
        A,
        B,
        C,
        D,
        E


## AND clauses:
- inline:
    WHERE A = 3 AND B > 4 AND C = blah

- multiline-single (unused):
    WHERE
        A = 3 AND B > 4 AND C = blah

- multline-after:
    WHERE A = 3
      AND B > 4
      AND C = blah

- multline-after-2 (unused):
    WHERE A = 3 AND
          B > 4 AND
          C = blah

- multiline-under (unused):
    WHERE
        A = 3
        AND B > 4
        AND C = blah

# Formatted examples
```sql
SELECT organization.name as Organization,
       CONCAT("[", project.name, "]") as Project,
       `view`.path as Path,
       CAST(AVG(LENGTH(`view`.spec->>"$.query_text")) AS SIGNED) AS `Query length`,
       COUNT(DISTINCT backend_event.backend_event_id) AS Events,
       COUNT(DISTINCT `user`.user_id) AS `Possible users`
  FROM views `view`
  LEFT JOIN projects project
    ON `view`.project_id = project.project_id
  LEFT JOIN backend_events backend_event
    ON `view`.view_id = backend_event.view_id
  LEFT JOIN organizations organization
    ON project.organization_id = organization.organization_id
  LEFT JOIN users `user`
    ON user.organization_id = organization.organization_id
 GROUP BY 1, 2, 3
 ORDER BY 1, 2, 3;
```

"""
from contextlib import contextmanager
from dataclasses import dataclass
from functools import partial, singledispatchmethod
from hashlib import sha256
from itertools import zip_longest
from os.path import dirname, join
from sys import argv
from typing import Any, Optional

from antlr4.tree.Tree import ParseTree, TerminalNodeImpl

from jasmine.sql.ast_base import ASTNode
from jasmine.sql.ast_nodes import (
    JoinSpec,
    ParseTreeNode,
    QuerySpecNode,
    TableJoin,
    matching_nodes,
    sql_ast,
)
from jasmine.sql.parser.sql import (
    SQLLexer,
    SQLParser,
    SQLParserVisitor,
    bracket_printed_sql_parse_tree,
    display_parse_tree,
    sql_tree_from_file,
    sql_tree_from_str,
)

comment_token_types = {
    SQLLexer.BLOCK_COMMENT,
    SQLLexer.POUND_COMMENT,
    SQLLexer.DASHDASH_COMMENT,
    SQLLexer.VERSION_COMMENT_START,
    SQLLexer.VERSION_COMMENT_END,
    SQLLexer.MYSQL_COMMENT_START,
    SQLLexer.COMMENT_SYMBOL,
}


def token_comments_str(tokens):
    return "".join(
        hidden_token.text or ""
        for hidden_token in (tokens or [])
        if hidden_token.type in comment_token_types
    )


class SQLCommentInjector(SQLParserVisitor):
    """
    By default, the MySQL parser parses sends comment strings and whitespace to
    the 'hidden' channel, so they disappear from tokenization onwards.

    This visitor reclaims any comments and attaches them to their nearest tokens.
    As comments may come after the final non-whitespace token, tokens can have
    comments to their left (token.before_comments_str) or right
    (token.after_comments_str).

    Apply this visitor to a parse tree to make the comments available under these
    property names.
    """

    def visitTerminal(self, node):
        token_stream = node.getParent().parser._input
        token_index = node.symbol.tokenIndex

        first_token = token_index == 0
        is_semicolon = node.symbol.type == SQLLexer.SEMICOLON_SYMBOL
        follows_semicolon = (
            token_stream.tokens[token_index - 1].type == SQLParser.SEMICOLON_SYMBOL
        )

        # Comments are attached to the tokens immediately to their left, except
        # at the start of statements when they're attached to the tokens on their right.

        # Exceptional case.
        node.before_comments_str = (
            token_comments_str(token_stream.getHiddenTokensToLeft(token_index))
            if first_token or follows_semicolon
            else ""
        )

        # Typical case.
        node.after_comments_str = (
            token_comments_str(token_stream.getHiddenTokensToRight(token_index))
            if not is_semicolon
            else ""
        )


subexpr_indent_spaces = 4
subquery_indent_spaces = 4


@dataclass
class IndentContext:
    subexpr_indent: int = 0
    subquery_indent: int = 0
    max_width: int = 70

    def indent_width(self) -> int:
        return self.subexpr_indent + self.subquery_indent

    def indent_spaces(self) -> str:
        return " " * self.indent_width()

    def newline_indent(self) -> str:
        return "\n" + " " * self.indent_width()

    @contextmanager
    def indent_subexpr(self, indent_width: Optional[int] = None):
        if indent_width is None:
            indent_width = subexpr_indent_spaces

        try:
            self.subexpr_indent += indent_width
            yield
        finally:
            self.subexpr_indent -= indent_width

    @contextmanager
    def indent_subquery(self, indent_width: Optional[int] = None):
        indent_width = indent_width or subquery_indent_spaces
        try:
            self.subquery_indent += indent_width
            yield
        finally:
            self.subquery_indent -= indent_width

    @contextmanager
    def new_subquery(self):
        try:
            original_subexpr_indent = self.subexpr_indent
            self.subexpr_indent = 0
            yield
        finally:
            self.subexpr_indent = original_subexpr_indent

    @contextmanager
    def shrink_width(self, width: int):
        try:
            self.max_width -= width
            yield
        finally:
            self.max_width += width

    @contextmanager
    def expr_prefix(self, prefix: str):
        try:
            self.max_width -= len(prefix)
            self.subexpr_indent += len(prefix)
            yield prefix
        finally:
            self.subexpr_indent -= len(prefix)
            self.max_width += len(prefix)


def list_joined(separator_item: Any, items: list[Any]) -> list[Any]:
    """
    Like ", ".join(blah), except for lists.

    >>> list_joined("HI", ["yo", "cats"])
    ['yo', 'HI', 'cats']
    """
    return [
        part
        for early_item in items[:-1]
        for part in (early_item, separator_item)  # Weird syntax to flatten tuples.
    ] + items[-1:]


def padded_concat(*values: str, strip: bool = True, sep: str = " ") -> str:
    """
    >>> padded_concat(" hello", "    yolo", "", " ", "yo", strip=True)
    'hello yolo yo'
    >>> padded_concat(" hello", "    yolo", "", " ", "yo", strip=False)
    ' hello     yolo yo'
    >>> padded_concat(" hello", "    yolo", "yo", strip=True, sep="  ")
    'hello  yolo  yo'
    """
    if strip:
        values = tuple(value.strip() for value in values)

    return sep.join(value for value in values if value.strip())


def final_line_length(multiline_value: str) -> int:
    return len(multiline_value.split("\n")[-1])


def is_multiline(value: str, indent: IndentContext) -> bool:
    return "\n" in value or len(value) > indent.max_width


@dataclass
class MockNode(ASTNode):
    text: str

    def from_parse_tree(cls, parse_tree: Optional[ParseTree]) -> ASTNode:
        raise RuntimeError


def mock_node(text: str):
    return MockNode(text)


def table_join_type_str(node: TableJoin, first: bool = False) -> str:
    if first:
        return "FROM"

    elif node.natural_join:
        if node.join_type == "INNER":
            return "NATURAL JOIN"
        else:
            return "NATURAL" + node.join_type.replace("_", " ") + " JOIN"

    elif node.straight_inner_join:
        return "STRAIGHT_JOIN"

    else:
        return node.join_type.replace("_OUTER", "") + " JOIN"


def first_token(prefix: str) -> str:
    lpadding_width = len(prefix) - len(prefix.lstrip())
    return (" " * lpadding_width) + prefix.lstrip().split(" ")[0].split("_")[0]


def prefix_padded(prefix, max_prefix_width):
    prefix_first_token = first_token(prefix)
    prefix_width = len(prefix_first_token)

    prefix_rest = prefix[prefix_width:]

    return prefix_first_token.rjust(max_prefix_width) + prefix_rest


class PrettyPrintVisitor:
    """
    Pretty print SQL expressions encoded as an AST.
    Uses IndentContext to manage indentation state.

    There are three parts here:
    - Helpers for recursively pretty printing / formatting expression lists

    - Pretty print functions for ASTNodes.
        These handle pretty printing AST-represented nodes.
        self.pretty_print() is the entry point and singledispatches out to
        self.pretty_print_{node_type}_{inline|multiline}.
        It handles multiline v inline logic sanely.

    - Pretty print functions for raw / ParseTreeNodes, by SQLParser context type.
        These handle pretty printing nodes that don't have an explicit AST representation yet.
        These aren't yet separated by inline/multiline.
        Singledispatch'd from self.pretty_print_raw_parse_tree_node by context type.
    """

    indent: IndentContext

    def __init__(self):
        self.indent = IndentContext()

    def padded_concat_node_pprints(self, *values) -> str:
        value_strs = []
        for value in values:
            if isinstance(value, str):
                value_strs.append(value)
            elif isinstance(value, list):
                value_strs.extend([self.pretty_print(subvalue) for subvalue in value])
            elif isinstance(value, ASTNode):
                value_strs.append(self.pretty_print(value))

        return padded_concat(*value_strs)

    def inline_expr_list_str(
        self,
        prefix: str,
        elements: list[ASTNode],
        sep: str = " ",
        suffix: str = "",
        use_commas: bool = True,
    ) -> str:
        """
        Inline formatted list.
        Tracks remaining width properly, and correctly handles multiline elements
        resetting the remaining line width.

        >>> nodes = [mock_node(c) for c in "ABCDE"]
        >>> print(PrettyPrintVisitor().inline_expr_list_str(
        ...     prefix="SELECT ",
        ...     elements=nodes,
        ...     sep=" ",
        ...     suffix="",
        ...     use_commas=True,
        ... ))
        SELECT A, B, C, D, E

        >>> print(PrettyPrintVisitor().inline_expr_list_str(
        ...     prefix="SELECT ",
        ...     elements=nodes,
        ...     sep=" ",
        ...     suffix="",
        ...     use_commas=False,
        ... ))
        SELECT A B C D E

        >>> print(PrettyPrintVisitor().inline_expr_list_str(
        ...     prefix="SELECT ",
        ...     elements=nodes,
        ...     sep="AND",
        ...     suffix="",
        ...     use_commas=False,
        ... ))
        SELECT A AND B AND C AND D AND E
        """
        assert (
            sep.strip() == ""
        ) or not use_commas, (
            "Expression separators and commas are mutually incompatible."
        )
        if use_commas:
            sep = ", "
        elif sep.strip() != "":
            sep = f" {sep} "

        result = prefix
        for element_index, element in enumerate(elements):

            if element_index > 0:
                result += sep

            line_length = len(result.split("\n")[-1])
            with self.indent.shrink_width(line_length):
                elem_str = self.pretty_print(element)

            result = (result + elem_str).rstrip()

        return (result + suffix).rstrip()

    def multiline_after_expr_list_str(
        self,
        prefix: str,
        elements: list[ASTNode],
        sep: str = " ",
        suffix: str = "",
        use_commas: bool = True,
    ):
        """
        Multiline-after formatted list.

        >>> nodes = [mock_node(c) for c in "ABCDE"]
        >>> print(PrettyPrintVisitor().multiline_after_expr_list_str(
        ...     prefix="SELECT ",
        ...     elements=nodes,
        ...     sep=" ",
        ...     suffix="",
        ...     use_commas=True,
        ... ))
        SELECT A,
               B,
               C,
               D,
               E

        >>> print(PrettyPrintVisitor().multiline_after_expr_list_str(
        ...     prefix="SELECT ",
        ...     elements=nodes,
        ...     sep=" ",
        ...     suffix="",
        ...     use_commas=False,
        ... ))
        SELECT A
               B
               C
               D
               E

        >>> print(PrettyPrintVisitor().multiline_after_expr_list_str(
        ...     prefix="SELECT ",
        ...     elements=nodes,
        ...     sep="AND",
        ...     suffix="",
        ...     use_commas=False,
        ... ))
        SELECT A
           AND B
           AND C
           AND D
           AND E
        """
        with self.indent.indent_subexpr(len(prefix)):
            assert (
                sep.strip() == ""
            ) or not use_commas, (
                "Expression separators and commas are mutually incompatible."
            )
            if sep.strip() != "":
                sep = "\n" + f"{sep} ".rjust(len(prefix))
            else:
                sep = ("," if use_commas else "") + self.indent.newline_indent()

            result = prefix
            for element_index, element in enumerate(elements):
                if element_index > 0:
                    result += sep

                result = (result + self.pretty_print(element)).rstrip()

        return (result + suffix).rstrip()

    def expr_list_str(
        self,
        prefix: str,
        elements: list[ASTNode],
        sep: str = " ",
        suffix: str = "",
        use_commas: bool = True,
    ):
        """

        Disable commas and give "AND" as a separator for this case.

        They are arranged from most-dense/most-horizontal to least-dense/most-vertical.
        Each has a different remaining-width and indent to pass to the children elements for rendering.
        At the moment, the logic goes:
        - Attempt inline (error if any subelements are multiline or width is exceeded))
        - Return multiline-after

        Future improvements could include shifting to multiline-under and using
        multiline-single if possible.
        """
        pretty_print_args = (
            prefix,
            elements,
            sep,
            suffix,
            use_commas,
        )

        inline_str = self.inline_expr_list_str(*pretty_print_args)
        if not is_multiline(inline_str, self.indent):
            return inline_str
        else:
            return self.multiline_after_expr_list_str(*pretty_print_args)

    @singledispatchmethod
    def pretty_print_inline(self, node) -> str:
        raise ValueError(
            f"Missing pretty print logic for ASTNode type {node.__class__.__name__}."
        )

    @singledispatchmethod
    def pretty_print_multiline(self, node) -> str:
        raise ValueError(
            f"Missing pretty print logic for ASTNode type {node.__class__.__name__}."
        )

    def pretty_print(self, node, force_multiline: bool = False, **kwargs) -> str:
        """
        Pretty print a string using inline / multiline, depending on what's available
        and requested.
        """
        inline_str = self.pretty_print_inline(node, **kwargs)
        if force_multiline or is_multiline(inline_str, self.indent):
            try:
                return self.pretty_print_multiline(node, **kwargs)
            except ValueError:
                pass

        return inline_str

    @pretty_print_inline.register
    def pretty_print_mock_node(self, node: MockNode):
        return node.text

    @pretty_print_inline.register
    def pretty_print_ast_parse_tree_node(self, node: ParseTreeNode) -> str:
        """
        Pretty print terminals (including comments) and ParseTreeNode nodes.
        Terminals include their attached comments, whereas nonterminals handle remaining-width tracking.

        >>> from jasmine.sql.ast_nodes import sql_ast

        >>> sql_pretty_printed("SELECT 1 FROM my_table")
        'SELECT 1 FROM my_table;'
        """
        return self.pretty_print_raw_parse_tree_node(
            node.base_node,
            node.children,
        )

    @singledispatchmethod
    def pretty_print_raw_parse_tree_node(self, node, children: list[ASTNode]) -> str:
        """
        Pretty-print a nonterminal node. This is a fallback handler.

        This handles remaining-width logic, and tries to avoid thinking about
        multiline shenanigans for now. It strips all children before combining them.
        """
        return self.inline_expr_list_str(
            "",
            children,
            " ",
            use_commas=False,
        )

    @pretty_print_raw_parse_tree_node.register
    def pretty_print_raw_terminal_node(
        self, node: TerminalNodeImpl, children: list[ASTNode]
    ) -> str:
        """
        Terminals have left-comments at the beginning of statements, and otherwise
        right-comments.
        (/* left-comment */\n{indent})?TOKEN(  /* right-comment */)?
        """
        if node.symbol.type == SQLParser.EOF:
            return ""

        left_comment = getattr(node, "before_comments_str", "").strip()
        token_text = node.getText().strip()
        right_comment = getattr(node, "after_comments_str", "").strip()

        if left_comment:
            left_comment = left_comment + self.indent.newline_indent()
        if right_comment:
            right_comment = f"  {right_comment}"

        return f"{left_comment}{token_text}{right_comment}"

    @pretty_print_raw_parse_tree_node.register
    def pretty_print_raw_sql_program_node(
        self, node: SQLParser.SqlProgramContext, children: list[ASTNode]
    ) -> str:
        statements = matching_nodes(children, {SQLParser.StatementContext})
        return (
            ";\n".join(self.pretty_print(statement) for statement in statements) + ";"
        )

    @pretty_print_raw_parse_tree_node.register
    def pretty_print_raw_simple_expr_node(
        self, node: SQLParser.SimpleExprContext, children: list[ASTNode]
    ) -> str:
        # Only strip separators before / after OPEN_PAR_SYMBOL and before CLOSE_PAR_SYMBOL.
        no_sep_before_nodes = matching_nodes(
            children,
            {
                SQLParser.OPEN_PAR_SYMBOL,
                SQLParser.CLOSE_PAR_SYMBOL,
                SQLParser.JsonOperatorContext,
            },
        )
        no_sep_after_nodes = matching_nodes(
            children,
            {
                SQLParser.OPEN_PAR_SYMBOL,
            },
        )

        result = ""
        for child, next_child in zip_longest(children, children[1:]):
            needs_sep = (
                next_child is not None
                and next_child not in no_sep_before_nodes
                and child not in no_sep_after_nodes
            )
            sep = " " if needs_sep else ""

            with self.indent.shrink_width(len(result)):
                result += self.pretty_print(child) + sep

        return result

    @pretty_print_raw_parse_tree_node.register
    def pretty_print_raw_sum_expr_node(
        self, node: SQLParser.SumExprContext, children: list[ASTNode]
    ) -> str:
        # Put an extra space before this node.
        before_nodes = matching_nodes(
            children,
            {
                SQLParser.WindowingClauseContext,
            },
        )
        # Put spaces between nodes of these types.
        between_nodes = matching_nodes(
            children,
            {
                SQLParser.DISTINCT_SYMBOL,
                SQLParser.ALL_SYMBOL,
                SQLParser.MULT_OPERATOR,
                SQLParser.InSumExprContext,
                SQLParser.ExprListContext,
                SQLParser.OrderClauseContext,
                SQLParser.SEPARATOR_SYMBOL,
                SQLParser.TextStringContext,
            },
        )

        result = ""
        for child, next_child in zip_longest(children, children[1:]):
            needs_sep = next_child is not None and (
                next_child in before_nodes
                or ((child in between_nodes) and (next_child in between_nodes))
            )
            sep = " " if needs_sep else ""

            with self.indent.shrink_width(len(result)):
                result += self.pretty_print(child) + sep

        return result

    @pretty_print_raw_parse_tree_node.register(SQLParser.DotIdentifierContext)
    @pretty_print_raw_parse_tree_node.register(SQLParser.FieldIdentifierContext)
    @pretty_print_raw_parse_tree_node.register(SQLParser.FunctionCallContext)
    @pretty_print_raw_parse_tree_node.register(SQLParser.GrantIdentifierContext)
    @pretty_print_raw_parse_tree_node.register(SQLParser.JsonOperatorContext)
    @pretty_print_raw_parse_tree_node.register(SQLParser.QualifiedIdentifierContext)
    @pretty_print_raw_parse_tree_node.register(SQLParser.SimpleIdentifierContext)
    @pretty_print_raw_parse_tree_node.register(
        SQLParser.TableReferenceListParensContext
    )
    @pretty_print_raw_parse_tree_node.register(SQLParser.WindowSpecContext)
    def pretty_print_raw_no_spaces(self, node, children: list[ASTNode]) -> str:
        return self.inline_expr_list_str(
            "",
            children,
            "",
            use_commas=False,
        )

    @pretty_print_raw_parse_tree_node.register(SQLParser.ExprListContext)
    @pretty_print_raw_parse_tree_node.register(SQLParser.OrderListContext)
    @pretty_print_raw_parse_tree_node.register(SQLParser.TableReferenceListContext)
    @pretty_print_raw_parse_tree_node.register(SQLParser.UdfExprListContext)
    def pretty_print_raw_comma_exprs(self, node, children: list[ASTNode]) -> str:
        subexpr_types = {
            SQLParser.OrderExpressionContext,
            SQLParser.ExprContext,
            SQLParser.UdfExprContext,
            SQLParser.TableReferenceContext,
        }
        return self.inline_expr_list_str(
            "",
            matching_nodes(children, subexpr_types),
            " ",
            use_commas=True,
        )

    @pretty_print_inline.register
    def pretty_print_table_join_inline(
        self,
        node: TableJoin,
        first_table: bool = False,
        max_prefix_width: int = 6,  # len("SELECT")
    ) -> str:
        join_type_str = table_join_type_str(node, first_table)
        join_type_prefix_length = len(join_type_str.split(" ")[0].split("_")[0])

        table_str = self.pretty_print(node.table_factor)

        using_str = ""
        if node.using_columns:
            using_str = (
                "USING ("
                + ", ".join(self.pretty_print(column) for column in node.using_columns)
                + ")"
            )

        on_clauses_str = ""
        if node.on_clauses:
            on_clauses_str = self.inline_expr_list_str(
                "ON ", node.on_clauses, sep="AND", use_commas=False
            )

        return " ".join(
            [
                part_str
                for part_str in [
                    join_type_str,
                    table_str,
                    using_str,
                    on_clauses_str,
                ]
                if part_str
            ]
        )

    @pretty_print_multiline.register
    def pretty_print_table_join_multiline(
        self,
        node: TableJoin,
        first_table: bool = False,
        max_prefix_width: int = 6,  # len("SELECT")
    ) -> str:
        join_type_str = table_join_type_str(node, first_table)

        # max_prefix_width = max(len(first_token(join_type_str)), len("SELECT"))
        padded = partial(prefix_padded, max_prefix_width=max_prefix_width)

        table_str = self.pretty_print(node.table_factor)

        using_str = ""
        if node.using_columns:
            using_str = (
                " USING ("
                + ", ".join(self.pretty_print(column) for column in node.using_columns)
                + ")"
            )

        on_clauses_str = ""
        if node.on_clauses:
            on_clauses_str = (
                self.indent.newline_indent()
                + self.multiline_after_expr_list_str(
                    padded("ON") + " ", node.on_clauses, sep="AND", use_commas=False
                )
            )

        return f"{padded(join_type_str)} {table_str}{using_str}{on_clauses_str}"

    @pretty_print_inline.register
    def pretty_print_join_spec_inline(self, node: JoinSpec) -> str:
        return " ".join(
            self.pretty_print(table_join, first_table=table_index == 0)
            for table_index, table_join in enumerate(node.table_joins)
        )

    @pretty_print_multiline.register
    def pretty_print_join_spec_multiline(self, node: JoinSpec) -> str:
        max_prefix_width = max(
            max(
                len(
                    first_token(
                        table_join_type_str(table_join, first=table_join_index == 0)
                    )
                )
                for table_join_index, table_join in enumerate(node.table_joins)
            ),
            len("SELECT"),
        )

        return self.indent.newline_indent().join(
            self.pretty_print(
                table_join,
                force_multiline=True,
                first_table=table_index == 0,
                max_prefix_width=max_prefix_width,
            )
            for table_index, table_join in enumerate(node.table_joins)
        )

    @pretty_print_inline.register
    def pretty_print_query_spec_inline(self, node: QuerySpecNode) -> str:
        """
        >>> print(sql_pretty_printed("SELECT 1 FROM my_table GROUP BY 1, 2, 3"))
        SELECT 1 FROM my_table GROUP BY 1, 2, 3;
        """
        select_options_str = ""
        if node.select_options:
            select_options_str = (
                " ".join(self.pretty_print(option) for option in node.select_options)
                + " "
            )

        select_exprs_str = self.inline_expr_list_str(
            f"SELECT {select_options_str}", node.select_exprs
        )

        where_clauses_str = ""
        if node.where_clauses:
            where_clauses_str = self.inline_expr_list_str("WHERE ", node.where_clauses)

        group_by_exprs_str = ""
        if node.group_by_exprs:
            group_by_exprs_str = self.inline_expr_list_str(
                "GROUP BY ", node.group_by_exprs
            )

        having_clauses_str = ""
        if node.having_clauses:
            having_clauses_str = self.inline_expr_list_str(
                "HAVING ", node.having_clauses
            )

        return self.padded_concat_node_pprints(
            self.indent,
            select_exprs_str,
            node.into_clause,
            node.from_clause,
            where_clauses_str,
            group_by_exprs_str,
            node.olap_options,
            having_clauses_str,
            node.window_clause,
        )

    @pretty_print_multiline.register
    def pretty_print_query_spec_multiline(self, node: QuerySpecNode) -> str:
        """
          >>> print(sql_pretty_printed(
          ...     "SELECT uhteautneoanuetoahuoueoa, uehtaonuteountoeuhoanueo "
          ...     + "FROM my_table WHERE uhteautneoanuetoahuoueoa IS NULL AND "
          ...     + "uaoetnueohueotautnoauhtuoa / 2 = 4 AND uheaonuteuheaonueoatuhaeohtnu > 3 "
          ...     + "GROUP BY uehatnua, ueahtnu, ueahtonuao WITH ROLLUP"
          ... ))
          SELECT uhteautneoanuetoahuoueoa, uehtaonuteountoeuhoanueo
            FROM my_table
           WHERE uhteautneoanuetoahuoueoa IS NULL
             AND uaoetnueohueotautnoauhtuoa / 2 = 4
             AND uheaonuteuheaonueoatuhaeohtnu > 3
           GROUP BY uehatnua, ueahtnu, ueahtonuao WITH ROLLUP;

          >>> print(sql_pretty_printed(
          ...     "SELECT uhteautneoanuetoahuoueoa, uehtaonuteountoeuhoanueo "
          ...     + "FROM my_table WHERE uhteautneoanuetoahuoueoa IS NULL AND "
          ...     + "uaoetnueohueotautnoauhtuoa / 2 = 4 AND uhetanuetoahuetaonuhoean > 3 "
          ...     + "GROUP BY uehatnua, ueahtnu, ueahtonuao WITH ROLLUP"
          ... ))
          SELECT uhteautneoanuetoahuoueoa, uehtaonuteountoeuhoanueo
            FROM my_table
           WHERE uhteautneoanuetoahuoueoa IS NULL
             AND uaoetnueohueotautnoauhtuoa / 2 = 4
             AND uhetanuetoahuetaonuhoean > 3
           GROUP BY uehatnua, ueahtnu, ueahtonuao WITH ROLLUP;

          >>> print(sql_pretty_printed(
          ...     "SELECT 1 FROM my_table GROUP BY uehatnua, ueahtnu, ueahtonuao WITH ROLLUP"
          ... ))
          SELECT 1
            FROM my_table
           GROUP BY uehatnua, ueahtnu, ueahtonuao WITH ROLLUP;

          Prefixes:
          SELECT
            FROM
            JOIN
         NATURAL LEFT JOIN # Longer than SELECT
        STRAIGHT_JOIN # Longer than SELECT
            LEFT JOIN
           INNER JOIN
           OUTER JOIN
           RIGHT JOIN
            LEFT OUTER JOIN
           CROSS JOIN
           USING
              ON
             AND
           WHERE
           GROUP BY
            WITH ROLLUP
          HAVING
           UNION
        """
        # FROM clause contains all keywords that are longer than "SELECT".
        # Calculate its multiline string first, extract the prefix, then use
        # that for all future padding.
        from_clause_str = self.pretty_print(node.from_clause, force_multiline=True)
        from_clause_indent = len("FROM") + len(from_clause_str.split("FROM")[0])

        max_prefix_width = max(len("SELECT"), from_clause_indent)

        padded = partial(prefix_padded, max_prefix_width=max_prefix_width)

        select_options_str = ""
        if node.select_options:
            select_options_str = (
                " ".join(self.pretty_print(option) for option in node.select_options)
                + " "
            )

        select_exprs_str = self.expr_list_str(
            padded(f"SELECT {select_options_str}"), node.select_exprs
        )

        where_clauses_str = ""
        if node.where_clauses:
            where_clauses_str = self.expr_list_str(
                padded("WHERE "), node.where_clauses, sep="AND", use_commas=False
            )

        group_by_exprs_str = ""
        if node.group_by_exprs:
            group_by_exprs_str = self.expr_list_str(
                padded("GROUP BY "), node.group_by_exprs
            ) + (
                " " + self.pretty_print(node.olap_options) if node.olap_options else ""
            )

        having_clauses_str = ""
        if node.having_clauses:
            having_clauses_str = self.expr_list_str(
                padded("HAVING "), node.having_clauses
            )

        return self.indent.newline_indent().join(
            (
                self.pretty_print(section_spec, force_multiline=True)
                if isinstance(section_spec, ASTNode)
                else section_spec
            )
            for section_spec in [
                select_exprs_str,
                node.into_clause,
                from_clause_str,
                where_clauses_str,
                group_by_exprs_str,
                having_clauses_str,
                node.window_clause,
            ]
            if section_spec
        )


# For abbreviated doctests and simple access to this library.
def sql_pretty_printed(sql_query: str, record_comments: bool = True) -> str:
    parse_tree = sql_tree_from_str(sql_query)

    if record_comments:
        SQLCommentInjector().visit(parse_tree)

    return PrettyPrintVisitor().pretty_print(sql_ast(parse_tree))


def pretty_printed_parse_tree(
    parse_tree: ParseTree, record_comments: bool = True
) -> str:
    if record_comments:
        SQLCommentInjector().visit(parse_tree)

    return PrettyPrintVisitor().pretty_print(sql_ast(parse_tree))


def display_example_query():
    sql_source_path = join(
        dirname(__file__),
        "examples",
        f"{argv[1]}.sql",
    )

    try:
        sql_tree = sql_tree_from_file(sql_source_path)
    except SyntaxError as e:
        print("Failed to parse, dropping into debugger mode.")
        from pdb import post_mortem

        post_mortem(e.__traceback__)
        raise e

    print("Verbose parse tree:")
    print(bracket_printed_sql_parse_tree(sql_tree, reduce_tree=False))

    print("Pretty SQL tree string:")
    print(bracket_printed_sql_parse_tree(sql_tree))

    print("SQL string:")
    print(pretty_printed_parse_tree(sql_tree))

    print("Rendering graph...")
    display_parse_tree(sql_tree)


def hash_str_prefix(value, chars=8):
    """
    >>> from jasmine.sql.pretty_print import hash_str_prefix
    >>> hash_str_prefix("hello world!")
    '7509e5bd'
    """
    hash_str = sha256(value.encode()).hexdigest()
    return hash_str[:chars]


def sql_query_semantic_hash(query: str) -> str:
    """
    Get a semantic hash key for a given SQL query.
    This throws out all comments and whitespace, but is (currently) sensitive to
    changes in the autoformatter and trivial semantic changes.
    Currently throws out some JOIN formatting stuff.

    >>> sql_query_semantic_hash('SELECT 1   FROM my_data /* woop! */;')
    'e1c0904a'
    >>> sql_query_semantic_hash('/* blaaaah */ SELECT    1 FROM my_data;')
    'e1c0904a'

    Note: It throws away some semantically irrelevant syntactic changes.
    >>> sql_query_semantic_hash('SELECT 1 FROM my_data LEFT OUTER JOIN a ON 1')
    '768b4ffb'
    >>> sql_query_semantic_hash('SELECT 1 FROM my_data LEFT JOIN a ON 1')
    '768b4ffb'
    """
    pretty_sql_str = sql_pretty_printed(query, record_comments=False)

    return hash_str_prefix(pretty_sql_str, chars=8)
