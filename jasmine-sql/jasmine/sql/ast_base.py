"""
Semantic representation of parse trees for query manipulation an analysis.

ASTs have a mostly one-to-one correspondence between themselves and valid parse
trees, but make common transformations (such as adding columns, extracting table
lists, etc) easier.

Nodes may choose to make implicit things explicit, provided they don't change
functionality (IE, adding "ASC" to ORDER BY clauses without an explicit direction.)


This file has the base Node definition, along with a variety of helpers for
serializing ASTs to parse trees.
"""
from abc import ABCMeta, abstractclassmethod, abstractmethod
from dataclasses import fields
from functools import lru_cache
from typing import Any, List, Optional, Tuple, Type, Union

from antlr4.Parser import Parser
from antlr4.ParserRuleContext import ParserRuleContext
from antlr4.Token import CommonToken, Token
from antlr4.tree.Tree import TerminalNodeImpl

from jasmine.sql.parser.sql import ParseTree, SQLParser


def ordered_dataclass_children(obj, child_type):
    children = []
    for field in fields(obj.__class__):
        field_value = getattr(obj, field.name, None)
        if field_value is None:
            continue

        if isinstance(field_value, child_type):
            children.append(field_value)

        elif isinstance(field_value, (list, tuple)):
            if all(
                isinstance(field_subvalue, child_type) for field_subvalue in field_value
            ):
                children.extend(field_value)

    return children


class ASTNode(metaclass=ABCMeta):
    """
    A semantic representation of a parse tree.
    """

    @abstractclassmethod
    def from_parse_tree(cls, parse_tree: ParseTree) -> "ASTNode":
        raise NotImplementedError

    def parse_tree(self) -> ParseTree:
        return sql_parse_tree_from_template(self.parse_tree_template())

    def parse_tree_template(self) -> "ParseTreeTemplate":
        raise NotImplementedError

    def node_type_name(self) -> str:
        return self.__class__.__name__

    def __str__(self) -> str:
        children = ordered_dataclass_children(self, ASTNode)

        parts = [self.node_type_name()] + [str(child) for child in children]

        can_abbreviate = (
            len(parts) < 5
            and not any("\n" in part for part in parts)
            and max(len(part) for part in parts) < 80
        )
        if can_abbreviate:
            body = f"{', '.join(parts)}"
        else:
            body = ",\n ".join(part.replace("\n", "\n   ") for part in parts)

        return f"[{body}]"


def terminal_parse_tree_node(
    parser_symbol: Optional[Token] = None,
    parser_token: Optional[int] = None,
    text: Optional[str] = None,
    before_comments: Optional[str] = None,
    after_comments: Optional[str] = None,
) -> ParseTree:
    """
    Generate a terminal parse tree node.
    Excludes any metadata, but allows for pretty printing.
    Includes before/after comments.
    """
    assert bool(parser_symbol) != bool(parser_token)

    if parser_symbol is None:
        parser_symbol = CommonToken(type=parser_token)
        if text is not None:
            parser_symbol.text = text

    assert parser_symbol is not None  # For mypy.

    node = TerminalNodeImpl(parser_symbol)
    node.before_comments_str = before_comments
    node.after_comments_str = after_comments

    return node


@lru_cache(maxsize=None)
def empty_parent_ctx():
    return SQLParser.SqlProgramContext(None)


def parse_tree_node(
    parse_tree_node_class: Type[ParseTree],
    children: List[ParseTree],
):
    """
    Generate a parse tree node with the given class and children.
    Used to build novel parse trees in transformations.

    Parse tree node will _not_ have the normal metadata associated with a parse tree.
    """
    node = parse_tree_node_class(None, empty_parent_ctx())
    node.children = children
    return node


def parser_rule_context(parser: Parser, rule_name: str) -> Type[ParserRuleContext]:
    rule_context_class_name = rule_name[0].upper() + rule_name[1:] + "Context"
    assert hasattr(
        parser, rule_name
    ), f"Can't find rule context class on parser: {rule_context_class_name} ({rule_name})"
    return getattr(parser, rule_context_class_name)


def parser_token(parser: Parser, token_name: str) -> int:
    "The parser token with the given name."
    parser_token = getattr(parser, token_name)
    assert isinstance(
        parser_token, int
    ), f"Could not find token type with name '{token_name}'."

    return parser_token


def default_text_terminal_token(parser: Parser, token_name: str) -> TerminalNodeImpl:
    if token_name.endswith("_SYMBOL"):
        token_text = token_name[: -len("_SYMBOL")]
    else:
        token_text = token_name

    return terminal_parse_tree_node(
        parser_token=parser_token(parser, token_name), text=token_text
    )


# MyPy struggles with recursive types, so exclude this for now.
ParseTreeTemplate = Union[  # type: ignore
    ParseTree,
    str,  # "ALL_SYMBOL", text attempts to remove "_SYMBOL".
    Tuple[str, str],  # ("identifier", "myTable")
    Tuple[int, str],  # (SQLParser.IDENTIFIER, "myTable")
    Tuple[str, List["ParseTreeTemplate"]],  # type: ignore # ("orderList", [...])
]


def parse_tree_from_template(
    parser: Parser,
    template: ParseTreeTemplate,
) -> ParseTree:
    """
    Easy templating for generating ParseTrees.

    You can specify tokens (their parser.SYMBOLs, or their names), parser node
    types (their string name and their children), and ParseTree subexpressions.

    >>> from jasmine.sql.parser.sql import SQLParser
    >>> from jasmine.sql.pretty_print import sql_tree_pretty_str

    For trivial, all-caps symbols, you can provide the name and the text will
    default to the portion of the symbol name before _SYMBOL:
    >>> token_tree = parse_tree_from_template(SQLParser, "DESC_SYMBOL")
    >>> print(sql_tree_pretty_str(token_tree))
    'DESC'

    You can specify token text using tuples:
    >>> token_tree = parse_tree_from_template(SQLParser, (SQLParser.DESC_SYMBOL, "MY_DESC"))
    >>> print(sql_tree_pretty_str(token_tree))
    'MY_DESC'

    You can also specify rule nodes (with required children) using tuples:
    >>> grammar_tree = parse_tree_from_template(
    ...     SQLParser,
    ...     ("direction", ["ASC_SYMBOL"]),
    ... )
    >>> print(sql_tree_pretty_str(grammar_tree))
    ['direction', 'ASC']

    Finally, you can use parse trees directly:
    >>> composed_tree = parse_tree_from_template(
    ...     SQLParser,
    ...     ("direction", [token_tree]),
    ... )
    >>> print(sql_tree_pretty_str(composed_tree))
    ['direction', 'MY_DESC']
    """
    if isinstance(template, (ParserRuleContext, TerminalNodeImpl)):
        return template
    elif isinstance(template, str):
        return default_text_terminal_token(parser, template)

    assert (
        isinstance(template, tuple) and len(template) == 2
    ), f"Invalid template of unknown type: {template}"

    left, right = template
    if isinstance(right, (list, tuple)):
        context_name, children_templates = left, right
        return parse_tree_node(
            parser_rule_context(parser, context_name),
            [
                parse_tree_from_template(parser, child_template)
                for child_template in children_templates
            ],
        )

    elif isinstance(left, (str, int)) and isinstance(right, str):
        if isinstance(left, int):
            token = left
        else:
            token = parser_token(parser, left)

        return terminal_parse_tree_node(parser_token=token, text=right)

    else:
        assert False, f"Invalid template of unknown type: {template}."


def sql_parse_tree_from_template(template: ParseTreeTemplate) -> ParseTree:
    return parse_tree_from_template(SQLParser, template)


def list_joined(separator_item: Any, items: List[Any]) -> List[Any]:
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
