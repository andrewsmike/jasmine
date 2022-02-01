"""
Aggregate a slice of CDC table into a before/after temp table pair for time traveling ETL logic.

Incremental materializations need to determine what portions of their table have changed.
They must be able to reconstruct the state of the source tables from when the ETL last ran
and fix the source tables at a consistent referenc point for next time.

Some backends (notably most ELT solutions) have native time-traveling support.
For others, we have to use preexisting trigger-driven CDC tables to generate temp tables
corresponding to before/after for any changed rows, then use those tables for diffing logic.

Between these two strategies, most backends can be supported.

For (historic_temp_table | (current_temp_table - historic_temp_table)) to accurately reflect the state
of the table at a specific time, we rely on the database engine to provide linearized reads against transaction order.
This _should_ work, as our queries will be dealing with `> timestamp` portions, which should lock the corresponding index.

## Current strategy
Currently, we assume REPEATABLE READ, reducing the number of issues. We determine the deltas from `prev` -> `next`, `prev` -> `now`, and `next` -> `now`.
We use the former one for the "row-has-changed` rows, and the latter two for `historic state of table`  rows.


## TODO
VERIFY THIS ^ IMPORTANT DETAIL. I think `REPEATABLE READ` in MySQL should behave reasonably here.
The really tricky part is edits to the source table _after_ the diff loading logic. Repeatable read should limit the effects of these.



## Notes
Source table states can only be defined _in contrast_ to another when using delta tables.
This means we could (correctly) derive the difference from `prev` -> `next` in two tables, and it will _stay_ correct.
The tricky part is getting the difference from `next` -> `now`, and keeping the results sufficiently fresh for our purposes.
    LOCK FOR READ could help here.
    It'd only need to apply to the `after` -> `now` generation, then updating the history tables, then the actual workunit generating queries.
    ... That's a lot of tables to lock.
"""
from dataclasses import dataclass
from typing import Literal

from jasmine.etl.region_tools import Region, in_region_expr
from jasmine.etl.table_diff import (
    column_value_updates_expr,
    columns_equal_expr,
    columns_null_expr,
    copy_region_statement,
    delete_unchanged_rows_statement,
    row_count,
)
from jasmine.sql.ast_nodes import QuerySpecNode
from jasmine.sql.table_spec import (
    TableSpec,
    create_staging_table_statement,
    drop_table_statement,
)
from jasmine.sql.transforms.escaping import (
    escaped,
    escaped_column_list,
    escaped_db_table,
)


def history_table_format_args(
    db_name: str,
    table_name: str,
    history_table_name: str,
    table_spec: TableSpec,
    history_table_spec: TableSpec,
    prev_timestamp_expr: str,
    next_timestamp_expr: str,
    stage: str,
) -> dict[str, str]:
    """
    >>> from pprint import pprint
    >>> from jasmine.sql.table_spec import example_table_spec

    >>> from jasmine.sql.transforms.history_table import history_table_spec_from_table_spec
    >>> history_table_spec = history_table_spec_from_table_spec(example_table_spec)

    >>> assert history_table_format_args(
    ...     db_name="my_db ' ",
    ...     table_name="my table ",
    ...     history_table_name="my table _history",
    ...     table_spec=example_table_spec,
    ...     history_table_spec=history_table_spec,
    ...     prev_timestamp_expr="@PREV_TIMESTAMP",
    ...     next_timestamp_expr="@NEXT_TIMESTAMP",
    ...     stage="prev",
    ... ) == example_format_args
    """
    primary_key = table_spec.primary_key
    history_column_names = history_table_spec.column_names
    (
        event_id_column_name,
        op_type_column_name,
        *column_names,
        ts_column_name,
    ) = history_column_names

    return {
        "escaped_column_names": escaped_column_list(column_names),
        "escaped_event_id_column_name": escaped(event_id_column_name),
        "escaped_history_column_names": escaped_column_list(history_column_names),
        "escaped_history_table": escaped_db_table(db_name, history_table_name),
        "escaped_op_type_column_name": escaped(op_type_column_name),
        "escaped_pk_column_names": escaped_column_list(primary_key),
        "escaped_table": escaped_db_table(db_name, table_name),
        "escaped_event_ts_column_name": escaped(ts_column_name),
        "next_timestamp_expr": next_timestamp_expr,
        "prev_timestamp_expr": prev_timestamp_expr,
        "timestamp_expr": prev_timestamp_expr
        if stage == "prev"
        else next_timestamp_expr,
        "stage": stage,
    }


example_format_args = {
    "escaped_column_names": "`user_id`, `name`, `parent_user_id`",
    "escaped_event_id_column_name": "`_jsmn_event_id_1`",
    "escaped_history_column_names": (
        "`_jsmn_event_id_1`, "
        + "`_jsmn_op_type_1`, "
        + "`user_id`, "
        + "`name`, "
        + "`parent_user_id`, "
        + "`_jsmn_event_ts_1`"
    ),
    "escaped_history_table": "`my_db ' `.`my table _history`",
    "escaped_op_type_column_name": "`_jsmn_op_type_1`",
    "escaped_pk_column_names": "`user_id`",
    "escaped_table": "`my_db ' `.`my table `",
    "escaped_event_ts_column_name": "`_jsmn_event_ts_1`",
    "next_timestamp_expr": "@NEXT_TIMESTAMP",
    "prev_timestamp_expr": "@PREV_TIMESTAMP",
    "stage": "prev",
    "timestamp_expr": "@PREV_TIMESTAMP",
}

# ((temp_table_name, create_temp_table_statement), select_data_for_temp_table_statement)
@dataclass
class StagedResultSpec:
    """
    Intermediate result, stored in a temporary table.
    """

    temp_table_name: str
    column_names: list[str]
    create_table_statement: str
    select_statement: str


def display_staged_result_spec(result_spec: StagedResultSpec):
    print(f"Temp table name: {result_spec.temp_table_name}")
    print(f"Columns: {result_spec.column_names}")
    print(f"CREATE TABLE statement:")
    print("    " + result_spec.create_table_statement.replace("\n", "\n    "))
    print(f"SELECT statement:")
    print("    " + result_spec.select_statement.replace("\n", "\n    "))


history_table_range_affected_pks_template = """
SELECT {escaped_pk_column_names}
  FROM {escaped_history_table}
 WHERE {escaped_event_ts_column_name} BETWEEN {prev_timestamp_expr} AND {next_timestamp_expr} - 1
 GROUP BY {escaped_pk_column_names};
""".strip()


def history_table_range_affected_pks(
    db_name: str,
    history_table_name: str,
    table_spec: TableSpec,
    format_args: dict[str, str],
) -> StagedResultSpec:
    """
    Get the set of primary keys that appear in a range in a history table.

    Note: This is end time exclusive.
    Anything that happens on or after this timestamp is irrelevant. We want the state _going into_ the timestamp.

    >>> from random import seed
    >>> from jasmine.sql.table_spec import example_table_spec

    >>> seed(1337)
    >>> result_spec = history_table_range_affected_pks(
    ...     db_name="my_db ' ",
    ...     history_table_name="my table _history",
    ...     table_spec=example_table_spec,
    ...     format_args=example_format_args,
    ... )

    >>> display_staged_result_spec(result_spec)
    Temp table name: _jsmn_tmp_my table _history_prev_next_affected_pks_MHwKkZ
    Columns: ['user_id']
    CREATE TABLE statement:
        CREATE TABLE `my_db ' `.`_jsmn_tmp_my table _history_prev_next_affected_pks_MHwKkZ` (
            `user_id` INTEGER NOT NULL,
            PRIMARY KEY (`user_id`)
        );
    SELECT statement:
        SELECT `user_id`
          FROM `my_db ' `.`my table _history`
         WHERE `_jsmn_event_ts_1` BETWEEN @PREV_TIMESTAMP AND @NEXT_TIMESTAMP - 1
         GROUP BY `user_id`;
    """

    pk_table_spec = table_spec.pk_table()

    temp_table_name, create_table_statement = create_staging_table_statement(
        base_db_name=db_name,
        base_table_name=history_table_name,
        base_table_spec=pk_table_spec,
        suffix="prev_next_affected_pks",
        real_table=True,
    )

    return StagedResultSpec(
        temp_table_name=temp_table_name,
        column_names=pk_table_spec.column_names,
        create_table_statement=create_table_statement,
        select_statement=history_table_range_affected_pks_template.format(
            **format_args
        ),
    )


historic_to_present_patch_template = """\
  WITH {stage}_curr_cdc_chunk AS (
    SELECT RANK() OVER (
               PARTITION BY {escaped_pk_column_names}
                   ORDER BY {escaped_event_ts_column_name} ASC, {escaped_event_id_column_name} ASC
         ) AS __jsmn_row_rank,
           {escaped_history_column_names}
      FROM {escaped_table}
     WHERE {escaped_event_ts_column_name} >= {timestamp_expr}
   )
SELECT {escaped_history_column_names}
  FROM {stage}_curr_cdc_chunk
 WHERE __jsmn_row_rank = 1;\
"""


def historic_to_present_patch(
    db_name: str,
    history_table_name: str,
    history_table_spec: TableSpec,
    format_args: dict[str, str],
) -> StagedResultSpec:
    """
    >>> from random import seed
    >>> from jasmine.sql.table_spec import example_table_spec

    >>> from jasmine.sql.transforms.history_table import history_table_spec_from_table_spec
    >>> example_history_table_spec = history_table_spec_from_table_spec(example_table_spec)

    >>> seed(1337)
    >>> result_spec = historic_to_present_patch(
    ...     db_name="my_db ' ",
    ...     history_table_name="my table _history",
    ...     history_table_spec=example_history_table_spec,
    ...     format_args=example_format_args,
    ... )
    >>> display_staged_result_spec(result_spec)
    Temp table name: _jsmn_tmp_my table _history_prev_curr_patch_MHwKkZ
    Columns: ['_jsmn_event_id_1', '_jsmn_op_type_1', 'user_id', 'name', 'parent_user_id', '_jsmn_event_ts_1']
    CREATE TABLE statement:
        CREATE TABLE `my_db ' `.`_jsmn_tmp_my table _history_prev_curr_patch_MHwKkZ` (
            `_jsmn_event_id_1` bigint NOT NULL AUTO_INCREMENT,
            `_jsmn_op_type_1` enum("INSERT", "INSERT_UPDATE", "DELETE", "DELETE_UPDATE") NOT NULL,
            `user_id` INTEGER NOT NULL,
            `name` VARCHAR(96) NOT NULL,
            `parent_user_id` BIGINT,
            `_jsmn_event_ts_1` bigint NOT NULL,
            PRIMARY KEY (`_jsmn_event_id_1`),
            KEY _jsmn_key_0 (`_jsmn_event_ts_1`),
            KEY _jsmn_key_1 (`name`),
            KEY _jsmn_key_2 (`parent_user_id`, `name`),
            KEY _jsmn_key_3 (`user_id`, `_jsmn_event_ts_1`)
        );
    SELECT statement:
          WITH prev_curr_cdc_chunk AS (
            SELECT RANK() OVER (
                       PARTITION BY `user_id`
                           ORDER BY `_jsmn_event_ts_1` ASC, `_jsmn_event_id_1` ASC
                 ) AS __jsmn_row_rank,
                   `_jsmn_event_id_1`, `_jsmn_op_type_1`, `user_id`, `name`, `parent_user_id`, `_jsmn_event_ts_1`
              FROM `my_db ' `.`my table `
             WHERE `_jsmn_event_ts_1` >= @PREV_TIMESTAMP
           )
        SELECT `_jsmn_event_id_1`, `_jsmn_op_type_1`, `user_id`, `name`, `parent_user_id`, `_jsmn_event_ts_1`
          FROM prev_curr_cdc_chunk
         WHERE __jsmn_row_rank = 1;
    """
    temp_table_name, create_table_statement = create_staging_table_statement(
        base_db_name=db_name,
        base_table_name=history_table_name,
        base_table_spec=history_table_spec,
        suffix=f"{format_args['stage']}_curr_patch",
        real_table=True,
    )
    return StagedResultSpec(
        temp_table_name=temp_table_name,
        column_names=history_table_spec.column_names,
        create_table_statement=create_table_statement,
        select_statement=historic_to_present_patch_template.format(**format_args),
    )


patch_affected_pks_template = """
SELECT {escaped_pk_column_names}
  FROM {escaped_history_table}
 WHERE {escaped_event_ts_column_name} >= {timestamp_expr}
 GROUP BY {escaped_pk_column_names};
""".strip()


def patch_affected_pks(
    db_name: str,
    table_name: str,
    table_spec: TableSpec,
    format_args: dict[str, str],
) -> StagedResultSpec:
    """
    Get the set of primary keys that appear in a patch table.

    WHAT TO DO TOMORROW:
    - Finish these three functions
    - Set up dict of part -> name, then add table names to subsequent queries.y
    - Generate for each subtable, make sure temp table names are exported in dict
    - Walk through a query, generating each JOIN CTE, slowly generating a new query.
        - This too generates a PK temporary result

    >>> from random import seed
    >>> from jasmine.sql.table_spec import example_table_spec

    >>> seed(1337)
    >>> result_spec = patch_affected_pks(
    ...     db_name="my_db ' ",
    ...     table_name="my table ",
    ...     table_spec=example_table_spec,
    ...     format_args=example_format_args,
    ... )
    >>> display_staged_result_spec(result_spec)
    Temp table name: _jsmn_tmp_my table _prev_curr_affected_pks_MHwKkZ
    Columns: ['user_id']
    CREATE TABLE statement:
        CREATE TABLE `my_db ' `.`_jsmn_tmp_my table _prev_curr_affected_pks_MHwKkZ` (
            `user_id` INTEGER NOT NULL,
            PRIMARY KEY (`user_id`)
        );
    SELECT statement:
        SELECT `user_id`
          FROM `my_db ' `.`my table _history`
         WHERE `_jsmn_event_ts_1` >= @PREV_TIMESTAMP
         GROUP BY `user_id`;
    """
    pk_table_spec = table_spec.pk_table()

    temp_table_name, create_table_statement = create_staging_table_statement(
        base_db_name=db_name,
        base_table_name=table_name,
        base_table_spec=pk_table_spec,
        suffix=f"{format_args['stage']}_curr_affected_pks",
        real_table=True,
    )

    return StagedResultSpec(
        temp_table_name=temp_table_name,
        column_names=pk_table_spec.column_names,
        create_table_statement=create_table_statement,
        select_statement=patch_affected_pks_template.format(**format_args),
    )


def source_table_staged_results(
    db_name: str,
    table_name: str,
    table_spec: str,
    history_table_name: str,
    history_table_spec: str,
    prev_timestamp_expr: str,
    next_timestamp_expr: str,
) -> dict[str, StagedResultSpec]:
    """
    >>> from random import seed
    >>> from jasmine.sql.table_spec import example_table_spec

    >>> from jasmine.sql.transforms.history_table import history_table_spec_from_table_spec
    >>> example_history_table_spec = history_table_spec_from_table_spec(example_table_spec)

    >>> seed(1337)
    >>> table_staged_results = source_table_staged_results(
    ...     db_name="my db ' ",
    ...     table_name="my table ' ",
    ...     table_spec=example_table_spec,
    ...     history_table_name="my table ' _history",
    ...     history_table_spec=example_history_table_spec,
    ...     prev_timestamp_expr="@PREV_TIMESTAMP",
    ...     next_timestamp_expr="@NEXT_TIMESTAMP",
    ... )


    >>> for alias, result_spec in table_staged_results.items():
    ...     print(f"{alias}:")
    ...     print("    " + result_spec.select_statement.replace("\\n", "\\n    "))
    ...     print(".")
    prev_next_affected_pks:
        SELECT `user_id`
          FROM `my db ' `.`my table ' _history`
         WHERE `_jsmn_event_ts_1` BETWEEN @PREV_TIMESTAMP AND @NEXT_TIMESTAMP - 1
         GROUP BY `user_id`;
    .
    prev_curr_patch:
          WITH prev_curr_cdc_chunk AS (
            SELECT RANK() OVER (
                       PARTITION BY `user_id`
                           ORDER BY `_jsmn_event_ts_1` ASC, `_jsmn_event_id_1` ASC
                 ) AS __jsmn_row_rank,
                   `_jsmn_event_id_1`, `_jsmn_op_type_1`, `user_id`, `name`, `parent_user_id`, `_jsmn_event_ts_1`
              FROM `my db ' `.`my table ' `
             WHERE `_jsmn_event_ts_1` >= @PREV_TIMESTAMP
           )
        SELECT `_jsmn_event_id_1`, `_jsmn_op_type_1`, `user_id`, `name`, `parent_user_id`, `_jsmn_event_ts_1`
          FROM prev_curr_cdc_chunk
         WHERE __jsmn_row_rank = 1;
    .
    prev_curr_affected_pks:
        SELECT `user_id`
          FROM `my db ' `.`my table ' _history`
         WHERE `_jsmn_event_ts_1` >= @PREV_TIMESTAMP
         GROUP BY `user_id`;
    .
    next_curr_patch:
          WITH next_curr_cdc_chunk AS (
            SELECT RANK() OVER (
                       PARTITION BY `user_id`
                           ORDER BY `_jsmn_event_ts_1` ASC, `_jsmn_event_id_1` ASC
                 ) AS __jsmn_row_rank,
                   `_jsmn_event_id_1`, `_jsmn_op_type_1`, `user_id`, `name`, `parent_user_id`, `_jsmn_event_ts_1`
              FROM `my db ' `.`my table ' `
             WHERE `_jsmn_event_ts_1` >= @NEXT_TIMESTAMP
           )
        SELECT `_jsmn_event_id_1`, `_jsmn_op_type_1`, `user_id`, `name`, `parent_user_id`, `_jsmn_event_ts_1`
          FROM next_curr_cdc_chunk
         WHERE __jsmn_row_rank = 1;
    .
    next_curr_affected_pks:
        SELECT `user_id`
          FROM `my db ' `.`my table ' _history`
         WHERE `_jsmn_event_ts_1` >= @NEXT_TIMESTAMP
         GROUP BY `user_id`;
    .
    """
    staged_results_by_alias: dict[str, StagedResultSpec] = {}
    for stage in ["prev", "next"]:
        format_args = history_table_format_args(
            db_name=db_name,
            table_name=table_name,
            history_table_name=history_table_name,
            table_spec=table_spec,
            history_table_spec=history_table_spec,
            prev_timestamp_expr=prev_timestamp_expr,
            next_timestamp_expr=next_timestamp_expr,
            stage=stage,
        )

        if stage == "prev":
            # Really stage ambivalent, but I don't want to make another call to format.
            staged_results_by_alias[
                "prev_next_affected_pks"
            ] = history_table_range_affected_pks(
                db_name=db_name,
                history_table_name=history_table_name,
                table_spec=table_spec,
                format_args=format_args,
            )

        staged_results_by_alias[f"{stage}_curr_patch"] = historic_to_present_patch(
            db_name=db_name,
            history_table_name=history_table_name,
            history_table_spec=history_table_spec,
            format_args=format_args,
        )

        staged_results_by_alias[f"{stage}_curr_affected_pks"] = patch_affected_pks(
            db_name=db_name,
            table_name=table_name,
            table_spec=table_spec,
            format_args=format_args,
        )

    return staged_results_by_alias


def blah():
    """
    - Pick timestamps

    - For each source table, generate source "temp" tables
        - Wait. Should I register these resources? Shit. I should. I should also have cleanup logic. Ewww.
            - If data too large, restart with smaller timestamp range.

    - Add "updated PK" StagedResultSpec.

    Next, we either build up an ordered list of StagedResultSpec, or we build up a new expression using CTEs.
    - For each source table, synthesize new query/JoinSpec/WHERE clause. (table templating?)
        - For each JOIN:
            - v1: SELECT *
            - v2: SELECT output columns
            - Generate StagedResultSpec, or add a CTE.
        - Run query/queries, INSERT INTO updated_pk StagedResultSpec.
            - If data too large, restart with smaller timestamp range.

    - Run reload logic, but with "PK IN (SELECT * FROM updated_pk)"
        - If data too large, restart with smaller timestamp range.
    """
    source_table_staged_results


def historic_query(query: QuerySpecNode):
    raise NotImplementedError


def history_tools_mock_conn():
    """
    A mock for simulating a history temp table generation session.
    """
    from unittest.mock import Mock

    mock = Mock()
    mock.sql_queries = []

    def execute_mock(sql):
        mock.sql_queries.append(sql)
        for prefix, value in [
            ("Delete unchanged", 100),
            ("Delete deleted", 15),
            ("Insert / update", 15 + 35 * 2),
        ]:
            if sql.startswith(f"/* {prefix}"):
                return value

        return None

    def fetchone_mock():
        return {"COUNT(*)": 100}

    mock.execute = execute_mock
    mock.fetchone = fetchone_mock

    raise ValueError
    return mock
