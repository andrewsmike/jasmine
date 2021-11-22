from glob import glob
from os.path import dirname, join

from pytest import mark

from jasmine.sql.ast_nodes import sql_ast_from_file, sql_ast_from_str
from jasmine.sql.pretty_print import pretty_printed_sql_ast, sql_pretty_printed

examples_paths = glob(join(dirname(__file__), "examples/*.sql"))
bad_formatted_examples_paths = set(
    glob(join(dirname(__file__), "examples/formatted/bad_*.sql"))
)
formatted_examples_paths = (
    set(glob(join(dirname(__file__), "examples/formatted/*.sql")))
    - bad_formatted_examples_paths
)


@mark.parametrize("query_path", formatted_examples_paths)
def test_formatted_sql(query_path: str):
    with open(query_path, "r") as f:
        query_str = f.read()

    assert (
        query_str.strip() == sql_pretty_printed(query_str).strip()
    ), "Query is not correctly formatted."


@mark.parametrize("query_path", formatted_examples_paths)
def test_pprint_idempotent(query_path: str):
    """
    Verify pretty printing semantics by testing that all pprinted ASTs parse back
    into an identical AST.
    """
    first_query_ast = sql_ast_from_file(query_path)
    pretty_printed_ast_query = pretty_printed_sql_ast(first_query_ast)
    second_query_ast = sql_ast_from_str(pretty_printed_ast_query)
    pretty_printed_second_ast_query = pretty_printed_sql_ast(second_query_ast)

    assert pretty_printed_ast_query == pretty_printed_second_ast_query
