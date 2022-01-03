"""
Tools for parsing and visualizing SQL statements using the ANTLR-based SQLParser.
"""
from pprint import pformat
from typing import Callable, Iterable, List, Optional, Tuple

from antlr4.CommonTokenStream import CommonTokenStream
from antlr4.FileStream import FileStream
from antlr4.InputStream import InputStream
from antlr4.Token import Token
from antlr4.error.ErrorListener import ErrorListener
from antlr4.tree.Tree import ParseTree
from antlr4.tree.Trees import Trees
from graphviz import Digraph

from jasmine.sql.parser.SQLLexer import SQLLexer
from jasmine.sql.parser.SQLParser import SQLParser
from jasmine.sql.parser.SQLParserListener import SQLParserListener  # noqa
from jasmine.sql.parser.SQLParserVisitor import SQLParserVisitor  # noqa


class AbortSyntaxErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise SyntaxError(f"At {line}:{column}: {msg}")


def children_contexts(
    ctx_func: Callable[[int], Optional[ParseTree]]
) -> List[ParseTree]:
    """
    The list of elements provided by a zero-indexed (index: int -> Optional[ParseTree])
    function.
    This is a bizarre way of providing this data, and it's usually useful to convert
    it into a proper list.

    >>> # Note: This should return contexts, but making them takes effort.
    >>> def get_word(index: int) -> Optional[str]:
    ...     content = ["hello", "world"]
    ...     if 0 <= index < len(content):
    ...         return content[index]
    ...     else:
    ...         return None
    >>> children_contexts(get_word)
    ['hello', 'world']
    """
    children: List[ParseTree] = []
    while (next_child := ctx_func(len(children))) is not None:
        children.append(next_child)

    return children


def sql_parser_from_str(expr: str) -> SQLParser:
    lexer = SQLLexer(InputStream(expr))
    token_stream = CommonTokenStream(lexer)
    parser = SQLParser(token_stream)

    parser.addErrorListener(AbortSyntaxErrorListener())

    return parser


def sql_raw_token_from_str(expr: str) -> Token:
    lexer = SQLLexer(InputStream(expr))
    return lexer.nextToken()


def sql_tree_from_stream(input_stream: InputStream) -> ParseTree:
    lexer = SQLLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = SQLParser(token_stream)

    parser.addErrorListener(AbortSyntaxErrorListener())

    program = parser.sqlProgram()

    return program


def sql_tree_from_file(path: str) -> ParseTree:
    return sql_tree_from_stream(FileStream(path))


def sql_tree_from_str(query: str) -> ParseTree:
    return sql_tree_from_stream(InputStream(query))


def sql_tree_paren_str(tree: ParseTree) -> str:
    """
    ANTLR default pretty printed parse tree.
    Not particularly nice. Check out bracket_printed_parse_tree for a better one.
    Included here for documentation purposes? Could delete.

    >>> print(sql_tree_paren_str(sql_tree_from_str("SELECT 1 FROM dual")))
    (sqlProgram (statement (simpleStatement (selectStatement (queryExpression (queryExpressionBody (queryPrimary (querySpecification SELECT (selectItemList (selectItem (expr (boolPri (predicate (bitExpr (simpleExpr (literal (numLiteral 1))))))))) (fromClause FROM dual)))))))) <EOF>)
    """
    return tree.toStringTree(recog=SQLParser)


BracketParseTree = list["BracketParseTree"] | str


def bracketed_sql_tree(tree: ParseTree) -> BracketParseTree:
    node_text = Trees.getNodeText(tree, ruleNames=SQLParser.ruleNames)

    if tree.getChildCount() == 0:
        return node_text
    else:
        return [node_text] + [
            bracketed_sql_tree(tree.getChild(child_index))
            for child_index in range(tree.getChildCount())
        ]


def reduced_bracketed_tree(bracketed_sql_tree: BracketParseTree) -> BracketParseTree:
    parts = []
    for child in bracketed_sql_tree[1:]:
        if isinstance(child, list):
            reduced_child = reduced_bracketed_tree(child)
        else:
            reduced_child = child

        if isinstance(reduced_child, list) and len(reduced_child) == 1:
            (reduced_child,) = reduced_child

        if reduced_child:
            parts.append(reduced_child)

    return parts


def bracket_printed_sql_parse_tree(tree: ParseTree, reduce_tree: bool = True) -> str:
    """
    Pretty print SQL parse trees for debugging.
    >>> print(bracket_printed_sql_parse_tree(sql_tree_from_str("SELECT 1 FROM dual")))
    [['SELECT', '1', ['FROM', 'dual']], '<EOF>']
    >>> print(bracket_printed_sql_parse_tree(sql_tree_from_str("SELECT 1 FROM dual"), reduce_tree=False))
    ['sqlProgram',
     ['statement',
      ['simpleStatement',
       ['selectStatement',
        ['queryExpression',
         ['queryExpressionBody',
          ['queryPrimary',
           ['querySpecification',
            'SELECT',
            ['selectItemList',
             ['selectItem',
              ['expr',
               ['boolPri',
                ['predicate',
                 ['bitExpr', ['simpleExpr', ['literal', ['numLiteral', '1']]]]]]]]],
            ['fromClause', 'FROM', 'dual']]]]]]]],
     '<EOF>']
    """
    bracketed_tree = bracketed_sql_tree(tree)
    if reduce_tree:
        bracketed_tree = reduced_bracketed_tree(bracketed_tree)

    return pformat(bracketed_tree)


BracketParseTreePath = list[int]


def bracketed_tree_locations(
    tree: BracketParseTree,
    path_prefix: BracketParseTreePath | None = None,
) -> Iterable[Tuple[BracketParseTreePath, BracketParseTree]]:
    if path_prefix is None:
        path_prefix = []

    assert path_prefix is not None  # For MyPy.

    yield (path_prefix, tree)
    match tree:
        case [str(node_type), *children]:
            for child_index, child in enumerate(children):
                yield from bracketed_tree_locations(child, path_prefix + [child_index])
        case str(node_text):
            pass


def display_parse_tree(tree: ParseTree, comment: str = "ANTLR Parse Tree"):
    tree = bracketed_sql_tree(tree)

    graph = Digraph(comment="ANTLR Parse Tree", format="png")

    node_paths = set()
    for node_path, node_value in bracketed_tree_locations(tree):
        node_paths.add(tuple(node_path))

        parent_node_name = "".join(f"[{index}]" for index in node_path[:-1])
        node_name = "".join(f"[{index}]" for index in node_path)

        if isinstance(node_value, list):
            node_str = node_value[0]
            color_str = "black"
        else:
            node_str = node_value
            color_str = "blue"

        assert isinstance(node_str, str), node_str

        graph.node(node_name, node_str, color=color_str)
        graph.edge(parent_node_name, node_name)

    graph.render("/tmp/parser_tree_vis", view=True)
