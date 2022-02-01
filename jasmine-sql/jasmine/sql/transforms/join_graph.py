"""
Manipulate a JoinSpec's JOIN order while redistributing ON clauses / WHERE clauses.

TODO:
- Resolve table names.
"""
from dataclasses import dataclass, replace
from re import compile
from typing import Iterable

from jasmine.sql.ast_nodes import (
    ASTNode,
    ColumnRef,
    CTESubqueryNode,
    JoinSpec,
    QuerySpecNode,
    TableJoin,
    TableRef,
    all_ast_nodes,
    sql_ast,
    sql_subexpr_ast,
)
from jasmine.sql.parser.sql import parse_tree_get
from jasmine.sql.pretty_print import pretty_printed_sql_ast

JoinClause = ASTNode


def clause_column_refs(clause: JoinClause) -> list[ColumnRef]:
    return list(all_ast_nodes(clause, ColumnRef))


def table_in_clause(table: TableRef, clause: JoinClause) -> bool:
    return any(
        table == column_ref.table_ref for column_ref in clause_column_refs(clause)
    )


@dataclass
class JoinGraph(object):
    tables: list[TableRef]  # Set semantics.
    clauses: list[JoinClause]  # Set semantics.


TablePath = list[TableRef]


class JoinGraphWalker(object):

    join_graph: JoinGraph

    remaining_tables: list[TableRef]  # Set semantics.
    remaining_clauses: list[JoinClause]  # Set semantics.

    def __init__(
        self,
        join_graph: JoinGraph,
        remaining_tables: list[TableRef] | None = None,
        remaining_clauses: list[JoinClause] | None = None,
    ):
        self.join_graph = join_graph
        self.remaining_tables = list(remaining_tables or join_graph.tables)
        self.remaining_clauses = list(remaining_clauses or join_graph.clauses)

    def finished(self):
        assert (
            bool(self.remaining_tables) or not self.remaining_clauses
        ), "Clauses still remaining after walk."
        return (not self.remaining_tables) and (not self.remaining_clauses)

    def copy(self):
        return JoinGraphWalker(
            join_graph=self.join_graph,
            remaining_tables=list(self.remaining_tables),
            remaining_clauses=list(self.remaining_clauses),
        )

    def step(self, next_table: TableRef) -> tuple[TableRef, list[JoinClause]]:
        self.remaining_tables.remove(next_table)
        return next_table, self.pop_joined_clauses()

    def pop_joined_clauses(self) -> list[JoinClause]:
        next_remaining_clauses = []
        fully_joined_clauses = []
        for clause in self.remaining_clauses:
            if any(
                clause_column_refs.table_ref in self.remaining_tables
                for clause_column_refs in clause_column_refs(clause)
            ):
                next_remaining_clauses.append(clause)
            else:
                fully_joined_clauses.append(clause)

        self.remaining_clauses = next_remaining_clauses
        return fully_joined_clauses

    def next_step(self) -> TableRef:

        next_table_join_scores = []
        for proposed_next_table in self.remaining_tables:
            _, join_on_clauses = self.copy().step(proposed_next_table)
            next_table_join_scores.append(
                (
                    proposed_next_table,
                    self.join_score(proposed_next_table, join_on_clauses),
                )
            )

        best_next_table, best_score = sorted(
            next_table_join_scores,
            key=lambda table_score: table_score[1],
        )[-1]

        return best_next_table

    def join_score(self, next_table: TableRef, join_clauses: list[JoinClause]) -> float:
        """
        How "good" is this potential JOIN?

        We want to JOIN to tables when it is likely cheap, roughly meaning "when as many of its JOIN
        columns are available as possible." Because not all columns are equal
        (IE, IDs > UUIDs > strings > timestamps, equality > inequality > complex equations), we
        heuristically weigh clauses by their apparent strictness.

        TODO: Incorporate EXPLAINs and just use that.
        """
        relevant_clauses = [
            clause
            for clause in self.join_graph.clauses
            if table_in_clause(next_table, clause)
        ]

        joined_clauses = [clause_weight(clause) for clause in join_clauses] + [
            clause_weight(clause)
            for clause in relevant_clauses
            if clause not in self.remaining_clauses
        ]

        unjoined_clauses = [
            clause_weight(clause)
            for clause in relevant_clauses
            if clause not in joined_clauses
        ]

        return sum(joined_clauses) / (sum(joined_clauses) + sum(unjoined_clauses))


def clause_weight(clause: JoinClause) -> float:
    """
    Equality >> inequality > arbitrary, and ID >> UUID > str > timestamps > rest.
    """
    if direct_equality(clause) is not None:
        comparison_type_score = 5
    elif direct_inequality(clause) is not None:
        comparison_type_score = 2
    else:
        comparison_type_score = 1

    if direct_equality(clause) is not None:
        left, right = direct_equality(clause)
        left_col, right_col = left.column_name, right.column_name
        column_score = column_name_score(left_col) + column_name_score(right_col)
    else:
        column_score = 0

    return comparison_type_score + column_score


def direct_equality(clause: JoinClause) -> tuple[TableRef, TableRef] | None:
    clause = clause.base_node
    # We assume we're starting with expr -> boolPri.
    not_direct_equality_paths = [
        ["boolPri", "type"],
        ["boolPri", "boolPri", "compOp"],
    ]
    if any(
        parse_tree_get(clause, bad_path) is not None
        for bad_path in not_direct_equality_paths
    ):
        return None

    left = parse_tree_get(clause, ["boolPri", "boolPri", "predicate"])
    comp_op = parse_tree_get(clause, ["boolPri", "compOp"])
    right = parse_tree_get(clause, ["boolPri", "predicate"])

    if comp_op.EQUAL_OPERATOR() is None:
        return None

    try:
        left_column_ref = sql_subexpr_ast(
            pretty_printed_sql_ast(sql_ast(left)), "columnRef"
        )
        right_column_ref = sql_subexpr_ast(
            pretty_printed_sql_ast(sql_ast(right)), "columnRef"
        )
    except Exception as e:
        return None

    return left_column_ref, right_column_ref


def direct_inequality(clause: JoinClause) -> tuple[TableRef, str, TableRef] | None:
    clause = clause.base_node
    # We assume we're starting with expr -> boolPri.
    not_direct_equality_paths = [
        ["boolPri", "type"],
        ["boolPri", "boolPri", "compOp"],
    ]
    if any(
        parse_tree_get(clause, bad_path) is not None
        for bad_path in not_direct_equality_paths
    ):
        return None

    left = parse_tree_get(clause, ["boolPri", "boolPri", "predicate"])
    comp_op = parse_tree_get(clause, ["boolPri", "compOp"])
    right = parse_tree_get(clause, ["boolPri", "predicate"])

    if comp_op is None:
        return None

    comp_op_text = pretty_printed_sql_ast(sql_ast(comp_op))
    if comp_op_text not in ("<", ">", ">=", "<="):
        return None

    try:
        left_column_ref = sql_subexpr_ast(
            pretty_printed_sql_ast(sql_ast(left)), "columnRef"
        )
        right_column_ref = sql_subexpr_ast(
            pretty_printed_sql_ast(sql_ast(right)), "columnRef"
        )
    except Exception as e:
        return None

    return left_column_ref, comp_op_text, right_column_ref


id_regex = compile("^" + "|".join([".*autoid", "id", ".id", ".*[^u][^u]id"]) + "$")
uuid_regex = compile("^" + "|".join([".*uuid", "uuid"]) + "$")
str_regex = compile("^" + "|".join([".*type", ".*state", ".*status", ".*path"]) + "$")
timestamp_regex = compile(
    "^" + "|".join([".*_ts", ".*time", ".*timestamp", ".*date", ".*datetime"]) + "$"
)
blob_regex = compile("^" + "|".join([".*text", ".*blob", ".*spec"]) + "$")


def column_name_score(column_name: str) -> float:
    "Generally, ID >> UUID > str > timestamps > blobs ~= unknown"
    for regex_type, score in [
        (id_regex, 2),
        (uuid_regex, 1.5),
        (str_regex, 1),
        (timestamp_regex, 0.75),
        (blob_regex, 0.5),
    ]:
        if regex_type.search(column_name) is not None:
            return score
    else:
        return 1  # Don't want to overly bias against or for unknown columns.


def traverse_graph(
    join_graph: JoinGraph,
    first_steps: list[TableRef] | None = None,
) -> Iterable[tuple[TableRef, list[JoinClause]]]:
    walker = JoinGraphWalker(join_graph)

    for step in first_steps or []:
        yield walker.step(step)

    while not walker.finished():
        yield walker.step(walker.next_step())


def table_join_table_clauses(
    table_join: TableJoin,
) -> tuple[TableRef, list[JoinClause]]:
    assert table_join.join_type == "INNER"  # TODO: Support LEFT JOIN

    assert not table_join.natural_join  # TODO: Support NATURAL JOIN
    assert not table_join.using_columns  # TODO: Support USING

    return (
        table_join.table_factor,
        table_join.on_clauses or [],
    )


def join_graph_from_query(query: QuerySpecNode) -> JoinGraph:
    tables = []
    clauses = []
    for table_join in query.from_clause.table_joins:
        join_table, join_clauses = table_join_table_clauses(table_join)
        tables.append(join_table)
        clauses += join_clauses

    clauses += query.where_clauses

    return JoinGraph(
        tables=tables,
        clauses=clauses,
    )


def join_reordered_query(query: QuerySpecNode) -> QuerySpecNode:
    """
    >>> from jasmine.sql.ast_nodes import sql_ast_from_str
    >>> from jasmine.sql.pretty_print import pretty_printed_sql_ast

    >>> example_ast = sql_ast_from_str(\"\"\"
    ...     SELECT *
    ...       FROM `my_db `.my_first_table my_table_blah
    ...       JOIN `my_db `.my_second_table my_table_bleh
    ...         ON my_table_blah.bleh_id = my_table_bleh.id
    ...       JOIN my_first_table my_table_bleeeh
    ...         ON `my_db `.my_table_blah.updated_ts < my_table_bleeeh.updated_ts
    ...       JOIN my_third_table my_table_bluh
    ...         ON my_table_bleeeh.bluh_id < my_table_bluh.bluh_id
    ...      WHERE my_table_blah.blah_type = "bleeeh"
    ...        AND my_table_bleeeh.type = 3;
    ... \"\"\").queries[0]

    >>> print(pretty_printed_sql_ast(example_ast))
    SELECT *
      FROM `my_db `.my_first_table my_table_blah
     INNER JOIN `my_db `.my_second_table my_table_bleh
        ON my_table_blah.bleh_id = my_table_bleh.id
     INNER JOIN my_first_table my_table_bleeeh
        ON `my_db `.my_table_blah.updated_ts < my_table_bleeeh.updated_ts
     INNER JOIN my_third_table my_table_bluh
        ON my_table_bleeeh.bluh_id < my_table_bluh.bluh_id
     WHERE my_table_blah.blah_type = "bleeeh" AND my_table_bleeeh.type = 3

    >>> print(pretty_printed_sql_ast(join_reordered_query(example_ast)))
    """
    # Capture FROM clauses, WHERE clauses

    join_graph = join_graph_from_query(query)

    table_joins = []
    where_clauses = []
    for join_index, (table_ref, on_clauses) in enumerate(traverse_graph(join_graph)):
        if join_index == 0:
            where_clauses = on_clauses

        table_joins.append(
            TableJoin(
                table_factor=table_ref,
                join_type="INNER",
                on_clauses=on_clauses if join_index != 0 else [],
            )
        )

    return replace(
        query,
        where_clauses=where_clauses,
        from_clause=replace(
            query.from_clause,
            table_joins=table_joins,
        ),
    )
