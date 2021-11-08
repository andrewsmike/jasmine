from glob import glob
from os.path import dirname, join

from pytest import mark

from jasmine.sql.pretty_print import sql_pretty_printed

formatted_examples_paths = glob(join(dirname(__file__), "examples/formatted/*.sql"))


@mark.parametrize("query_path", formatted_examples_paths)
def test_formatted_sql(query_path: str):
    with open(query_path, "r") as f:
        query_str = f.read()

    assert (
        sql_pretty_printed(query_str) == query_str
    ), "Query is not correctly formatted."
