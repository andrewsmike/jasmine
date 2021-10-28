from contextlib import contextmanager
from dataclasses import dataclass
from functools import singledispatchmethod
from typing import Any, Optional

from antlr4.tree.Tree import TerminalNodeImpl

from jasmine.sql.ast_base import ASTNode
from jasmine.sql.ast_nodes import ParseTreeNode, QuerySpecNode, sql_ast
from jasmine.sql.parser.sql import ParseTree, SQLParser, sql_tree_from_str

subexpr_indent_spaces = 4
subquery_indent_spaces = 4


@dataclass
class IndentContext:
    subexpr_indent: int = 0
    subquery_indent: int = 0
    max_width: int = 120

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


class PrettyPrintVisitor:
    """
    Pretty print SQL expressions encoded as an AST.
    Uses IndentContext to manage indentation state.
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
        suffix: str,
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
        ...     suffix="",
        ...     use_commas=True,
        ... ))
        SELECT A, B, C, D, E

        >>> print(PrettyPrintVisitor().inline_expr_list_str(
        ...     prefix="SELECT ",
        ...     elements=nodes,
        ...     suffix="",
        ...     use_commas=False,
        ... ))
        SELECT A B C D E
        """
        sep = ", " if use_commas else " "

        result = prefix
        for element_index, element in enumerate(elements):

            if element_index > 0:
                result += sep

            line_length = len(result.split("\n")[-1])
            with self.indent.shrink_width(line_length):
                elem_str = self.pretty_print(element)

            result = (result + elem_str).strip()

        return (result + suffix).strip()

    def multiline_after_expr_list_str(
        self,
        prefix: str,
        elements: list[ASTNode],
        suffix: str,
        use_commas: bool = True,
    ):
        """
        Multiline-after formatted list.

        >>> nodes = [mock_node(c) for c in "ABCDE"]
        >>> print(PrettyPrintVisitor().multiline_after_expr_list_str(
        ...     prefix="SELECT ",
        ...     elements=nodes,
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
        ...     suffix="",
        ...     use_commas=False,
        ... ))
        SELECT A
               B
               C
               D
               E
        """
        sep = "," if use_commas else ""

        with self.indent.indent_subexpr(len(prefix)):
            result = prefix
            for element_index, element in enumerate(elements):
                if element_index > 0:
                    result += sep + self.indent.newline_indent()

                result = (result + self.pretty_print(element)).strip()

        return (result + suffix).strip()

    def expr_list_str(
        self,
        prefix: str,
        elements: list[ASTNode],
        suffix: str,
        use_commas: bool = True,
    ):
        """
        There are various ways to indent a list:
        - inline:
            SELECT CONCAT(my_thing, other_thing, blah)

        - multiline-single (not currently used):
            SELECT CONCAT(
                       my_thing, other_thing, blah
                   )

        - multiline-after:
            SELECT CONCAT(my_thing,
                          other_thing,
                          blah)

        - multiline-under:
            SELECT CONCAT(
                       my_thing,
                       other_thing,
                       blah
                   )

        - multiline-under-indent-reset (not currently supported):
            SELECT CONCAT(
                my_thing,
                other_thing,
                blah
            )

        Different examples:
            inline:
                SELECT A, B, C, D, E

            multiline-single
                SELECT
                    A, B, C, D, E

            multiline-after:
                SELECT A,
                       B,
                       C,
                       D,
                       E

            multiline-under:
                SELECT
                    A,
                    B,
                    C,
                    D,
                    E

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
            suffix,
            use_commas,
        )

        inline_str = self.inline_expr_list_str(*pretty_print_args)
        if not is_multiline(inline_str, self.indent):
            return inline_str
        else:
            return self.multiline_after_expr_list_str(*pretty_print_args)

    @singledispatchmethod
    def pretty_print(self, node) -> str:
        raise ValueError(
            f"Missing pretty print logic for ASTNode type {node.__class__.__name__}."
        )

    @pretty_print.register
    def pretty_print_mock_node(self, node: MockNode):
        return node.text

    @pretty_print.register
    def pretty_print_parse_tree_node(self, node: ParseTreeNode) -> str:
        """
        Pretty print terminals (including comments) and ParseTreeNode nodes.
        Terminals include their attached comments, whereas nonterminals handle remaining-width tracking.

        >>> from jasmine.sql.parser.sql import sql_ast

        >>> sql_pretty_printed("SELECT 1 FROM my_table")
        'SELECT 1 FROM my_table'
        """
        if isinstance(node.base_node, TerminalNodeImpl):
            return self.pretty_print_terminal_parse_tree_node(node)
        else:
            return self.pretty_print_nonterminal_parse_tree_node(node)

    def pretty_print_terminal_parse_tree_node(self, parse_tree: ParseTreeNode) -> str:
        """
        Terminals have left-comments at the beginning of statements, and otherwise
        right-comments.
        (/* left-comment */\n{indent})?TOKEN(  /* right-comment */)?
        """
        terminal = parse_tree.base_node

        if terminal.symbol.type == SQLParser.EOF:
            return ""

        left_comment = getattr(terminal, "before_comments_str", "").strip()
        token_text = terminal.getText().strip()
        right_comment = getattr(terminal, "after_comments_str", "").strip()

        if left_comment:
            left_comment = left_comment + self.indent.newline_indent()
        if right_comment:
            right_comment = f"  {right_comment}"

        return f"{left_comment}{token_text}{right_comment}"

    def pretty_print_nonterminal_parse_tree_node(
        self, parse_tree: ParseTreeNode
    ) -> str:
        """
        Pretty-print a nonterminal node.
        This handles remaining-width logic, and tries to avoid thinking about
        multiline shenanigans for now. It strips all children before combining them.
        """
        return self.inline_expr_list_str(
            "",
            parse_tree.children,
            "",
            use_commas=False,
        )

    @pretty_print.register
    def pretty_print_query_spec(self, node: QuerySpecNode) -> str:
        """
        >>> print(sql_pretty_printed("SELECT 1 FROM my_table GROUP BY 1, 2, 3"))
        SELECT 1 FROM my_table GROUP BY 1 , 2 , 3

        print(sql_pretty_printed(
        ...     "SELECT 1 FROM my_table GROUP BY abcdueoyatnhuneaothuant, "
        ...     + "uheaotnunhteoutnoauehaotnutnaeohuntaeohunaoe, ueahtonuao WITH ROLLUP"
        ... ))
        SELECT 1
          FROM my_table
         GROUP BY abcdueoatnhuneaothuant ASC,
                  uheaotnunhteoutnoauehaotnutnaeohuntaeohunaoe ASC,
                  ueahtonuao ASC WITH ROLLUP
        """
        return self.padded_concat_node_pprints(
            self.indent,
            "SELECT ",
            node.select_options,
            node.select_exprs,
            node.into_clause,
            node.from_clause,
            node.where_clauses,
            node.group_by_exprs,
            node.olap_options,
            node.having_clauses,
            node.window_clause,
        )


# For abbreviated doctests and simple access to this library.
def sql_pretty_printed(sql_query: str) -> str:
    return PrettyPrintVisitor().pretty_print(sql_ast(sql_tree_from_str(sql_query)))
