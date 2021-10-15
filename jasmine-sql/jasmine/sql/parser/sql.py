from typing import Callable, List, Optional

from antlr4.CommonTokenStream import CommonTokenStream
from antlr4.FileStream import FileStream
from antlr4.InputStream import InputStream
from antlr4.error.ErrorListener import ErrorListener
from antlr4.tree.Tree import ParseTree

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
