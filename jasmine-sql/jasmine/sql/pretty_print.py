"""
TODO: Real tests.
Okay, actual TODO:
- Replace entire pretty printing return type with multiline / inline symbols.
- Have _distinct_ levels make the decision whether they need to break out.
    (Inline/multiline is just stretches of the tree that breakout _together_.)


>>> 2 + 2
4
"""

from contextlib import contextmanager
from functools import reduce
from hashlib import sha256
from os.path import dirname, join
from pprint import pformat
from sys import argv
from textwrap import dedent

from antlr4.tree.Tree import ParseTree
from antlr4.tree.Trees import Trees

from jasmine.sql.parser.sql import (
    SQLLexer,
    SQLParser,
    SQLParserVisitor,
    children_contexts,
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


def padded_concat(*values: str, strip: bool = True) -> str:
    return " ".join(value.strip() if strip else value for value in values if value)


def token_comments_str(tokens):
    return "".join(
        hidden_token.text or ""
        for hidden_token in (tokens or [])
        if hidden_token.type in comment_token_types
    )


class SQLCommentInjector(SQLParserVisitor):
    def visitTerminal(self, node):
        token_stream = node.getParent().parser._input
        token_index = node.symbol.tokenIndex

        node.before_comments_str = (
            token_comments_str(token_stream.getHiddenTokensToLeft(token_index))
            if token_index == 0
            else ""
        )

        node.after_comments_str = (
            token_comments_str(token_stream.getHiddenTokensToRight(token_index))
            if node.symbol.type != SQLLexer.SEMICOLON_SYMBOL
            else ""
        )


query_keyword_rjust = 7


def rjust_first_keyword(value: str) -> str:
    value_parts = value.strip().split(" ")
    return " ".join([value_parts[0].rjust(query_keyword_rjust)] + value_parts[1:])


def strs_map(values, func):
    return {key: func(value) for key, value in values.items()}


class SQLPrettyPrinter(SQLParserVisitor):
    """
    Pretty print SQL parse trees.
    This printer combines two concepts:
    - Custom printing of various parse nodes (IE `SUM ( a )` => `SUM(a)`)
    - Breaking out long lines onto multiple lines (inline to multiline).

    This visitor returns {"inline": inline_str, "multiline": multiline_str} documents
    and tracks remaining-max-width while generating expressions.
    NOTE: remaining-max-width only needs to be decremented for the multiline path.
    The inline path necessarily has a smaller remaining-max-width, and any
    violations will be caught at the appropriate layer.

    TODO:
    - Remove spaces within function calls
    - Adaptively newline-or-break-out lists.
    - Adaptively newline-or-breakout function calls
    - Apply uniform length and newlines to basic query keywords
    - Break out ANDs/ORs when nontrivial.
    """

    def __init__(self, max_width: int = 80):
        self.max_width = max_width
        self.indent = 0

    def visitChildren(self, ctx):
        """
        Custom visitChildren that updates self.max_width as it goes along
        """
        current_result = self.defaultResult()
        for child_ctx in children_contexts(ctx.getChild):
            if not self.shouldVisitNextChild(ctx, current_result):
                break

            min_indent = min(len(current_result["inline"].split("\n")[-1]), 4)
            with self.multiline_indent(min_indent):
                next_result = self.wrapping_visit(child_ctx)
            current_result = self.aggregateResult(current_result, next_result)

        return current_result

    def defaultResult(self):
        return {"inline": "", "multiline": ""}

    def aggregateResult(self, current_result, next_result):
        return {
            "inline": padded_concat(current_result["inline"], next_result["inline"]),
            "multiline": padded_concat(
                current_result["multiline"], next_result["multiline"], strip=False
            ),
        }

    def visitTerminal(self, node):
        terminal_str = padded_concat(
            getattr(node, "before_comments_str", ""),
            node.getText(),
            getattr(node, "after_comments_str", ""),
        )
        return {
            "inline": terminal_str,
            "multiline": terminal_str,
        }

    @contextmanager
    def multiline_indent(self, indent: int):
        self.indent += indent
        try:
            yield self.indent
        finally:
            self.indent -= indent

    def should_multiline(self, value: str) -> bool:
        return "\n" in value or self.indent + len(value) > self.max_width

    def wrapping_visit(self, ctx):
        result = self.visit(ctx)
        if isinstance(result, str):
            return {"inline": result, "multiline": result}
        else:
            return result

    def visit_dynamic(self, ctx):
        results = self.wrapping_visit(ctx)
        if self.should_multiline(results["inline"]):
            return results["multiline"]
        else:
            return results["inline"]

    def visit_inline(self, ctx):
        return self.wrapping_visit(ctx)["inline"]

    def visit_multiline(self, ctx):
        return self.wrapping_visit(ctx)["multiline"]

    def visitSqlProgram(self, ctx):
        """
        Top level node.

        Returns a single string, not an inline/multiline choice.
        """
        statements = children_contexts(ctx.statement)

        if not statements:
            return ""
        else:
            return (
                ";\n\n".join(self.visit_dynamic(statement) for statement in statements)
                + ";"
            )

    def list_str_with_prefix(self, items, prefix):
        inline_str = f"{prefix} {', '.join(items)}"
        if self.should_multiline(inline_str):
            sep = ",\n" + " " * (len(prefix) + 1)
            return f"{prefix} " + sep.join(items)
        else:
            return inline_str

    def visitQuerySpecification(self, ctx):
        """
        Query specification exports inline and multiline versions for
        queryExpressionBody to handle.
        """
        select_item_strs = [
            self.wrapping_visit(select_item_ctx)
            for select_item_ctx in (
                children_contexts(ctx.selectItemList().selectItem)
                + [ctx.selectItemList().MULT_OPERATOR()]
            )
            if select_item_ctx is not None
        ]

        select_item_strs[:-1] = [
            strs_map(item_strs, lambda value: value + ",")
            for item_strs in select_item_strs[:-1]
        ]

        select_options_item_strs = [
            self.wrapping_visit(select_option_ctx)
            for select_option_ctx in children_contexts(ctx.selectOption)
        ]
        if select_options_item_strs:
            select_item_strs = [
                reduce(self.aggregateResult, select_options_item_strs)
            ] + select_item_strs

        select_inline_str = "SELECT " + " ".join(
            item_strs["inline"] for item_strs in select_item_strs
        )
        select_multiline_str = " SELECT " + "\n".join(
            item_strs["multiline"] for item_strs in select_item_strs
        ).replace("\n", "\n       ")
        if self.should_multiline(select_inline_str):
            select_clauses_str = select_multiline_str
        else:
            select_clauses_str = select_inline_str

        clause_strs = [select_clauses_str] + [
            self.visit_dynamic(child_ctx)
            for child_ctx in [
                ctx.intoClause(),
                ctx.fromClause(),
                ctx.whereClause(),
                ctx.groupByClause(),
                ctx.havingClause(),
                ctx.windowClause(),
            ]
            if child_ctx is not None
        ]

        return {
            "inline": padded_concat(*clause_strs),
            "multiline": "\n".join(clause_strs),
        }

    def visitHavingClause(self, ctx):
        return " HAVING " + self.visit_dynamic(ctx.expr())

    def visitWhereClause(self, ctx):
        return "  WHERE " + self.visit_dynamic(ctx.expr())

    def visitLimitClause(self, ctx):
        return "  LIMIT " + self.visit_dynamic(ctx.limitOptions())

    def visitOrderClause(self, ctx):
        order_line_strs = [
            self.visit_inline(child_ctx)
            for child_ctx in children_contexts(ctx.orderList().orderExpression)
        ]
        order_line_strs[0] = f"BY {order_line_strs[0]}"

        return self.list_str_with_prefix(order_line_strs, "  ORDER")

    def visitGroupByClause(self, ctx):
        grouping_exprs = [
            self.visit_dynamic(child_ctx)
            for child_ctx in (
                children_contexts(ctx.orderList().orderExpression) + [ctx.olapOption()]
            )
            if child_ctx
        ]
        return self.list_str_with_prefix(grouping_exprs, "  GROUP BY")

    def visitFromClause(self, ctx):
        return "   FROM " + " ".join(
            [
                self.visit_dynamic(child_ctx)
                for child_ctx in [ctx.DUAL_SYMBOL(), ctx.tableReferenceList()]
                if child_ctx
            ]
        )

    def visitJoinedTable(self, ctx):
        join_type_str = rjust_first_keyword(
            self.visit_dynamic(
                ctx.innerJoinType() or ctx.outerJoinType() or ctx.naturalJoinType()
            )
        )
        table_ref_str = self.visit_dynamic(ctx.tableReference() or ctx.tableFactor())

        on_expr_ctx = ctx.expr()
        on_expr_str = (
            f"\n     ON {self.visit_dynamic(on_expr_ctx)}" if on_expr_ctx else ""
        )

        using_expr_ctx = ctx.identifierListWithParentheses()
        using_expr_str = (
            f" USING {self.visit_dynamic(using_expr_ctx)}" if using_expr_ctx else ""
        )

        return f"{join_type_str} {table_ref_str}{using_expr_str}{on_expr_str}"

    def visitQueryExpression(self, ctx):
        part_strs = [
            self.wrapping_visit(part_ctx)
            for part_ctx in [
                ctx.withClause(),
                ctx.queryExpressionBody(),
                ctx.queryExpressionParens(),
                ctx.orderClause(),
                ctx.limitClause(),
                ctx.procedureAnalyseClause(),
            ]
            if part_ctx
        ]

        inline_str_parts = [part["inline"] for part in part_strs]
        multiline_str_parts = [part["multiline"] for part in part_strs]

        inline_str = padded_concat(*inline_str_parts)
        multiline_str = dedent(rjust_first_keyword("\n".join(multiline_str_parts)))
        return {
            "inline": inline_str,
            "multiline": multiline_str,
        }

    def visitQueryExpressionParens(self, ctx):
        parens_query_ctx = ctx.queryExpressionParens()
        if parens_query_ctx is not None:
            return self.visit_dynamic(parens_query_ctx)

        with self.multiline_indent(4):
            subquery_strs = self.wrapping_visit(ctx.queryExpression())

            locking_clause_ctx = ctx.lockingClauseList()
            if locking_clause_ctx is not None:
                subquery_strs = self.aggregateResult(
                    subquery_strs, self.wrapping_visit(locking_clause_ctx)
                )

        return {
            "inline": f"({subquery_strs['inline']})",
            "multiline": (
                "(\n\t" + subquery_strs["multiline"].replace("\n", "\n\t") + "\n\t)"
            ),
        }

    def visitFunctionCall(self, ctx):
        identifier_str = self.visit_inline(
            ctx.pureIdentifier() or ctx.qualifiedIdentifier()
        )
        args_ctx = ctx.udfExprList() or ctx.exprList()
        args_strs = (
            self.visit(args_ctx)
            if args_ctx is not None
            else {"inline": "", "multiline": ""}
        )

        return {
            "inline": f"{identifier_str}({args_strs['inline']})",
            "multiline": f"{identifier_str}("
            + args_strs["multiline"].replace("\n", "\n    ")
            + "\n)",
        }

    def visitIdentifierListWithParentheses(self, ctx):
        return f"({self.visit_dynamic(ctx.identifierList())})"

    def visitFieldIdentifier(self, ctx):
        parts = []
        if (qual_ident_ctx := ctx.qualifiedIdentifier()) is not None:
            parts.append(self.visit_inline(qual_ident_ctx))
        if (dot_ident_ctx := ctx.dotIdentifier()) is not None:
            parts.append(self.visit_inline(dot_ident_ctx.identifier()))

        return ".".join(parts)

    def visitQualifiedIdentifier(self, ctx):
        parts = [self.visit_inline(ctx.identifier())]

        if (dot_ident_ctx := ctx.dotIdentifier()) is not None:
            parts.append(self.visit_inline(dot_ident_ctx.identifier()))

        return ".".join(parts)

    def visit_comma_list(self, ctx_func):
        parts = [self.visit_dynamic(child) for child in children_contexts(ctx_func)]

        return {
            "inline": ", ".join(parts),
            "multiline": ",\n".join(parts),
        }

    def visitSelectItemList(self, ctx):
        return self.visit_dynamic_comma_list(ctx.selectItem)

    def visitOrderList(self, ctx):
        return self.visit_dynamic_comma_list(ctx.orderExpression)


def pretty_sql_str_from_tree(tree: ParseTree, record_comments: bool = True) -> str:
    if record_comments:
        SQLCommentInjector().visit(tree)
    return SQLPrettyPrinter().visit(tree)


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

    TODO: Render with basic toString, get rid of volatile autoformatter dependency.

    >>> sql_query_semantic_hash('SELECT 1   FROM my_data /* woop! */;')
    'e1c0904a'
    >>> sql_query_semantic_hash('/* blaaaah */ SELECT    1 FROM my_data;')
    'e1c0904a'
    """
    pretty_sql_str = pretty_sql_str_from_tree(
        sql_tree_from_str(query), record_comments=False
    )
    return hash_str_prefix(pretty_sql_str, chars=8)


def sql_tree_str(tree: ParseTree) -> str:
    return tree.toStringTree(recog=SQLParser)


def bracketed_sql_tree(tree: ParseTree):
    node_text = Trees.getNodeText(tree, ruleNames=SQLParser.ruleNames)

    if tree.getChildCount() == 0:
        return node_text
    else:
        return [node_text] + [
            bracketed_sql_tree(tree.getChild(child_index))
            for child_index in range(tree.getChildCount())
        ]


def sql_tree_pretty_str(tree: ParseTree) -> str:
    return pformat(bracketed_sql_tree(tree))


def sql_from_bracketed_tree(bracketed_sql_tree) -> str:
    parts = []
    for child in bracketed_sql_tree[1:]:
        if isinstance(child, list):
            child_str = sql_from_bracketed_tree(child)
        else:
            child_str = str(child)

        if child_str:
            parts.append(child_str)

    return " ".join(parts) if parts else ""


def reduced_bracketed_tree(bracketed_sql_tree):
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


def pretty_printed_sql_str(sql_query: str) -> str:
    return pretty_sql_str_from_tree(sql_tree_from_str(sql_query))


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

    print("Pretty SQL tree string:")
    print(sql_tree_pretty_str(sql_tree))

    print("SQL string:")
    print(pretty_sql_str_from_tree(sql_tree))
