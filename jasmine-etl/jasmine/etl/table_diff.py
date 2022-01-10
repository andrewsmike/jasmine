from jasmine.etl.region_tools import Region, in_region_expr
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


def columns_equal_expr(
    left_alias: str, right_alias: str, column_names: list[str]
) -> str:
    """
    >>> print("    ON " + columns_equal_expr("left", "right", ["event_id", "title", "updated_ts"]))
        ON left.`event_id` <=> right.`event_id`
       AND left.`title` <=> right.`title`
       AND left.`updated_ts` <=> right.`updated_ts`
    """
    return "\n   AND ".join(
        f"{left_alias}.{escaped(column_name)} <=> {right_alias}.{escaped(column_name)}"
        for column_name in column_names
    )


def columns_null_expr(table_alias: str, column_names: list[str]) -> str:
    """
    >>> print(" WHERE " + columns_null_expr("left", ["event_id", "title", "updated_ts"]))
     WHERE left.`event_id` IS NULL
       AND left.`title` IS NULL
       AND left.`updated_ts` IS NULL
    """
    return "\n   AND ".join(
        f"{table_alias}.{escaped(column_name)} IS NULL" for column_name in column_names
    )


def column_value_updates_expr(column_names: list[str]) -> str:
    """
    The COLUMN = VALUE(COLUMN) expression in INSERT INTO ON DUPLICATE KEY UPDATE.

    >>> print("    ON DUPLICATE KEY UPDATE " + column_value_updates_expr(["event_id", "title", "updated_ts"]))
        ON DUPLICATE KEY UPDATE `event_id` = VALUES(`event_id`),
                                `title` = VALUES(`title`),
                                `updated_ts` = VALUES(`updated_ts`)
    """
    return ",\n                            ".join(
        f"{escaped(column_name)} = VALUES({escaped(column_name)})"
        for column_name in column_names
    )


delete_unchanged_rows_statement_template = """
/* Delete unchanged rows. */
DELETE prev, next
  FROM {prev_db_table} prev
  JOIN {next_db_table} next
    ON {prev_next_columns_equal_expr};
"""[
    1:-1
]


def delete_unchanged_rows_statement(
    db_name: str, prev_temp_table: str, next_temp_table: str, column_names: list[str]
) -> str:
    """
    >>> print(delete_unchanged_rows_statement("`main ' `", " uahtoeua' ", 'next_table"', ["event_id", "title", "updated_ts"]))
    /* Delete unchanged rows. */
    DELETE prev, next
      FROM `main ' `.` uahtoeua' ` prev
      JOIN `main ' `.`next_table"` next
        ON prev.`event_id` <=> next.`event_id`
       AND prev.`title` <=> next.`title`
       AND prev.`updated_ts` <=> next.`updated_ts`;
    """
    return delete_unchanged_rows_statement_template.format(
        prev_db_table=escaped_db_table(db_name, prev_temp_table),
        next_db_table=escaped_db_table(db_name, next_temp_table),
        prev_next_columns_equal_expr=columns_equal_expr("prev", "next", column_names),
    )


def row_count_statement(db_name: str, table_name: str) -> str:
    """
    >>> print(row_count_statement(" main ' ", 'user " '))
    SELECT COUNT(*) FROM ` main ' `.`user " `;
    """
    return f"SELECT COUNT(*) FROM {escaped_db_table(db_name, table_name)};"


def row_count(conn, db_name: str, table_name: str) -> int:
    conn.execute(row_count_statement(db_name, table_name))
    results = conn.fetchone()
    assert len(results) == 1
    return list(results.values())[0]


def patch_format_args(
    db_name: str,
    table_name: str,
    prev_temp_table: str,
    next_temp_table: str,
    column_names: list[str],
    primary_key_columns: list[str],
) -> dict[str, str]:
    """
    >>> from pprint import pprint
    >>> pprint(patch_format_args(
    ...     db_name="my_db ' ",
    ...     table_name="curr_table",
    ...     prev_temp_table="prev_temp",
    ...     next_temp_table="next_temp",
    ...     column_names=["event_id", "org_id", "desc"],
    ...     primary_key_columns=["event_id", "org_id"],
    ... ))
    {'column_list': '`event_id`, `org_id`, `desc`',
     'column_value_updates': '`event_id` = VALUES(`event_id`),\\n'
                             '                            `org_id` = '
                             'VALUES(`org_id`),\\n'
                             '                            `desc` = VALUES(`desc`)',
     'curr_db_table': "`my_db ' `.`curr_table`",
     'next_db_table': "`my_db ' `.`next_temp`",
     'next_pk_is_null_expr': 'next.`event_id` IS NULL\\n'
                             '   AND next.`org_id` IS NULL',
     'prev_curr_pk_equal_expr': 'prev.`event_id` <=> curr.`event_id`\\n'
                                '   AND prev.`org_id` <=> curr.`org_id`',
     'prev_db_table': "`my_db ' `.`prev_temp`",
     'prev_next_pk_equal_expr': 'prev.`event_id` <=> next.`event_id`\\n'
                                '   AND prev.`org_id` <=> next.`org_id`'}
    """
    return {
        "prev_db_table": escaped_db_table(db_name, prev_temp_table),
        "curr_db_table": escaped_db_table(db_name, table_name),
        "next_db_table": escaped_db_table(db_name, next_temp_table),
        "prev_next_pk_equal_expr": columns_equal_expr(
            "prev", "next", primary_key_columns
        ),
        "prev_curr_pk_equal_expr": columns_equal_expr(
            "prev", "curr", primary_key_columns
        ),
        "next_pk_is_null_expr": columns_null_expr("next", primary_key_columns),
        "column_list": escaped_column_list(column_names),
        "column_value_updates": column_value_updates_expr(column_names),
    }


example_format_args = patch_format_args(
    db_name="my_db ' ",
    table_name="curr_table",
    prev_temp_table="prev_temp",
    next_temp_table="next_temp",
    column_names=["event_id", "org_id", "desc"],
    primary_key_columns=["event_id", "org_id"],
)

patch_deleted_rows_statement_template = """
/* Delete deleted rows. */
DELETE curr
  FROM {prev_db_table} prev
  LEFT JOIN {next_db_table} next  /* If this is NULL, delete. If not, don't delete. */
    ON {prev_next_pk_equal_expr}
  JOIN {curr_db_table} curr
    ON {prev_curr_pk_equal_expr}
 WHERE {next_pk_is_null_expr};  /* If row is in `next`, don't delete. */
"""[
    1:-1
]


def patch_deleted_rows_statement(format_args: dict[str, str]) -> str:
    """
    /* Delete deleted rows. */
    >>> print(patch_deleted_rows_statement(example_format_args))
    /* Delete deleted rows. */
    DELETE curr
      FROM `my_db ' `.`prev_temp` prev
      LEFT JOIN `my_db ' `.`next_temp` next  /* If this is NULL, delete. If not, don't delete. */
        ON prev.`event_id` <=> next.`event_id`
       AND prev.`org_id` <=> next.`org_id`
      JOIN `my_db ' `.`curr_table` curr
        ON prev.`event_id` <=> curr.`event_id`
       AND prev.`org_id` <=> curr.`org_id`
     WHERE next.`event_id` IS NULL
       AND next.`org_id` IS NULL;  /* If row is in `next`, don't delete. */
    """
    return patch_deleted_rows_statement_template.format(**format_args)


patch_inserted_updated_rows_statement_template = """
/* Insert / update next rows. */
INSERT INTO {curr_db_table} ({column_list})
SELECT {column_list}
  FROM {next_db_table} next
    ON DUPLICATE KEY UPDATE {column_value_updates};
"""[
    1:-1
]


def patch_inserted_updated_rows_statement(format_args):
    """
    >>> print(patch_inserted_updated_rows_statement(example_format_args))
    /* Insert / update next rows. */
    INSERT INTO `my_db ' `.`curr_table` (`event_id`, `org_id`, `desc`)
    SELECT `event_id`, `org_id`, `desc`
      FROM `my_db ' `.`next_temp` next
        ON DUPLICATE KEY UPDATE `event_id` = VALUES(`event_id`),
                                `org_id` = VALUES(`org_id`),
                                `desc` = VALUES(`desc`);
    """
    return patch_inserted_updated_rows_statement_template.format(**format_args)


def patch_real_table(
    conn,
    format_args,
) -> dict[str, int]:
    patch_deleted_rows_sql = patch_deleted_rows_statement(format_args)
    patch_inserted_updated_rows_sql = patch_inserted_updated_rows_statement(format_args)

    stats = {}
    stats["deleted_count"] = conn.execute(patch_deleted_rows_sql)
    stats["inserted_updated_count"] = conn.execute(patch_inserted_updated_rows_sql)

    return stats


def patch_mock_conn():
    """
    A mock for simulating a patching session where the table:
    - Starts and ends with 100 rows
    - Has 50 unchanged rows
    - Has 15 deleted rows, 15 inserted rows, and 35 updated rows.
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

    return mock


def apply_minimized_patch(
    conn,
    db_name: str,
    table_name: str,
    prev_temp_table: str,
    next_temp_table: str,
    column_names: list[str],
    primary_key_columns: list[str],
) -> dict[str, int]:
    """
    Minimize, then apply, a row-patch / row-diff represented by a previous and a new temp table.
    Return row change statistics.

    Should be roughly equivalent to:
    - DELETE curr_table FROM curr_table WHERE curr_table.pk IN prev_table;
    - INSERT INTO curr_table SELECT * FROM next_table ON DUPLICATE KEY UPDATE ...;

    Example usage, statistics results, and underlying database interactions:
    >>> from pprint import pprint
    >>> mock_conn = patch_mock_conn()
    >>> pprint(apply_minimized_patch(
    ...     mock_conn,
    ...     "my_db",
    ...     'my_table " ',
    ...     "`prev temp`",
    ...     "next temp",
    ...     column_names=["event_id", "org_id", "updated_ts"],
    ...     primary_key_columns=["event_id", "org_id"],
    ... ))
    {'deleted_count': 15,
     'inserted_count': 15,
     'next_count': 100,
     'prev_count': 100,
     'unchanged_count': 50,
     'updated_count': 35}

    >>> for sql_query in mock_conn.sql_queries:
    ...     print(sql_query)
    SELECT COUNT(*) FROM `my_db`.`prev temp`;
    SELECT COUNT(*) FROM `my_db`.`next temp`;
    /* Delete unchanged rows. */
    DELETE prev, next
      FROM `my_db`.`prev temp` prev
      JOIN `my_db`.`next temp` next
        ON prev.`event_id` <=> next.`event_id`
       AND prev.`org_id` <=> next.`org_id`
       AND prev.`updated_ts` <=> next.`updated_ts`;
    /* Delete deleted rows. */
    DELETE curr
      FROM `my_db`.`prev temp` prev
      LEFT JOIN `my_db`.`next temp` next  /* If this is NULL, delete. If not, don't delete. */
        ON prev.`event_id` <=> next.`event_id`
       AND prev.`org_id` <=> next.`org_id`
      JOIN `my_db`.`my_table " ` curr
        ON prev.`event_id` <=> curr.`event_id`
       AND prev.`org_id` <=> curr.`org_id`
     WHERE next.`event_id` IS NULL
       AND next.`org_id` IS NULL;  /* If row is in `next`, don't delete. */
    /* Insert / update next rows. */
    INSERT INTO `my_db`.`my_table " ` (`event_id`, `org_id`, `updated_ts`)
    SELECT `event_id`, `org_id`, `updated_ts`
      FROM `my_db`.`next temp` next
        ON DUPLICATE KEY UPDATE `event_id` = VALUES(`event_id`),
                                `org_id` = VALUES(`org_id`),
                                `updated_ts` = VALUES(`updated_ts`);
    """
    raw_prev_count = row_count(conn, db_name, prev_temp_table)
    raw_next_count = row_count(conn, db_name, next_temp_table)

    format_args = patch_format_args(
        db_name,
        table_name,
        prev_temp_table,
        next_temp_table,
        column_names,
        primary_key_columns,
    )

    unchanged_count = (
        conn.execute(
            delete_unchanged_rows_statement(
                db_name, prev_temp_table, next_temp_table, column_names
            ),
        )
        // 2
    )

    changed_prev_count = raw_prev_count - unchanged_count
    changed_next_count = raw_next_count - unchanged_count

    patch_stats = patch_real_table(
        conn,
        format_args,
    )

    updated_count = changed_prev_count - patch_stats["deleted_count"]
    inserted_count = changed_next_count - updated_count

    assert (
        patch_stats["inserted_updated_count"] == inserted_count + updated_count * 2
    ), "Row counts didn't add up when applying changes."

    return {
        "inserted_count": inserted_count,
        "updated_count": updated_count,
        "unchanged_count": unchanged_count,
        "deleted_count": patch_stats["deleted_count"],
        "prev_count": raw_prev_count,
        "next_count": raw_next_count,
    }


copy_region_statement_template = """
/* Copy old data into temp table for diff'ing. */
INSERT INTO {dest_db_table} ({column_names})
SELECT {column_names}
  FROM {src_db_table} src
 WHERE {src_in_region_expr};
"""[
    1:-1
]


def copy_region_statement(
    db_name: str,
    src_table_name: str,
    dest_table_name: str,
    region: Region | None,
    column_names: list[str],
) -> str:
    """
    SQL to copy region of one table into another.
    We use this to copy the current values of the table into a temp table.

    >>> from jasmine.etl.region_tools import DiscreteRegion, IntersectionRegion, RangeRegion
    >>> region = IntersectionRegion([
    ...     DiscreteRegion(columns=["title"], points=[("my_fav_movie",)]),
    ...     RangeRegion(column="updated_ts", lower_bound_excl=1641769277),
    ... ])
    >>> print(copy_region_statement("my_db", "my_table", "my_temp_table", region, ["event_id", "title", "updated_ts"]))
    /* Copy old data into temp table for diff'ing. */
    INSERT INTO `my_db`.`my_temp_table` (`event_id`, `title`, `updated_ts`)
    SELECT `event_id`, `title`, `updated_ts`
      FROM `my_db`.`my_table` src
     WHERE ((`src`.`title` <=> 'my_fav_movie'))
       AND (1641769277 < `src`.`updated_ts`);

    >>> print(copy_region_statement("my_db", "my_table", "my_temp_table", None, ["event_id", "title", "updated_ts"]))
    /* Copy old data into temp table for diff'ing. */
    INSERT INTO `my_db`.`my_temp_table` (`event_id`, `title`, `updated_ts`)
    SELECT `event_id`, `title`, `updated_ts`
      FROM `my_db`.`my_table` src
     WHERE 1;
    """
    return copy_region_statement_template.format(
        column_names=escaped_column_list(column_names),
        src_db_table=escaped_db_table(db_name, src_table_name),
        dest_db_table=escaped_db_table(db_name, dest_table_name),
        src_in_region_expr=in_region_expr(region, "src") if region is not None else "1",
    )


def patch_target_table_region(
    conn,
    db_name: str,
    table_name: str,
    next_temp_table: str,
    temp_table_spec: TableSpec,
    region: Region | None,
) -> dict[str, int]:
    """
    Intelligently patch a table region to only include values in the given temporary table.

    Example usage, statistics results, and underlying database interactions:
    >>> from random import seed
    >>> from pprint import pprint
    >>> from jasmine.etl.region_tools import DiscreteRegion, IntersectionRegion, RangeRegion

    >>> region = IntersectionRegion([
    ...     DiscreteRegion(columns=["title"], points=[("my_fav_movie",)]),
    ...     RangeRegion(column="updated_ts", lower_bound_excl=1641769277),
    ... ])

    >>> temp_table_spec = TableSpec(
    ...     column_names=["event_id", "title", "updated_ts"],
    ...     column_type_decls={
    ...         "event_id": "BIGINT NOT NULL AUTO_INCREMENT",
    ...         "title": "VARCHAR(256) NOT NULL",
    ...         "updated_ts": "INTEGER NOT NULL",
    ...     },
    ...     primary_key=["event_id"],
    ...     indices={"updated_ts": ["updated_ts"], "title": ["title"]},
    ... )

    >>> seed(1337) # Make randomly generated temp table names consistent.

    >>> mock_conn = patch_mock_conn()
    >>> pprint(patch_target_table_region(
    ...     mock_conn,
    ...     db_name="my_db",
    ...     table_name='my_table " ',
    ...     next_temp_table="next temp",
    ...     temp_table_spec=temp_table_spec,
    ...     region=region,
    ... ))
    {'deleted_count': 15,
     'inserted_count': 15,
     'next_count': 100,
     'prev_count': 100,
     'unchanged_count': 50,
     'updated_count': 35}

    >>> for sql_query in mock_conn.sql_queries:
    ...     print(sql_query)
    CREATE TEMPORARY TABLE `my_db`.`_my_table " _prev_MHwKkZ` (
        `event_id` BIGINT NOT NULL AUTO_INCREMENT,
        `title` VARCHAR(256) NOT NULL,
        `updated_ts` INTEGER NOT NULL,
        PRIMARY KEY (`event_id`),
        KEY updated_ts (`updated_ts`),
        KEY title (`title`)
    );
    /* Copy old data into temp table for diff'ing. */
    INSERT INTO `my_db`.`_my_table " _prev_MHwKkZ` (`event_id`, `title`, `updated_ts`)
    SELECT `event_id`, `title`, `updated_ts`
      FROM `my_db`.`my_table " ` src
     WHERE ((`src`.`title` <=> 'my_fav_movie'))
       AND (1641769277 < `src`.`updated_ts`);
    SELECT COUNT(*) FROM `my_db`.`_my_table " _prev_MHwKkZ`;
    SELECT COUNT(*) FROM `my_db`.`next temp`;
    /* Delete unchanged rows. */
    DELETE prev, next
      FROM `my_db`.`_my_table " _prev_MHwKkZ` prev
      JOIN `my_db`.`next temp` next
        ON prev.`event_id` <=> next.`event_id`
       AND prev.`title` <=> next.`title`
       AND prev.`updated_ts` <=> next.`updated_ts`;
    /* Delete deleted rows. */
    DELETE curr
      FROM `my_db`.`_my_table " _prev_MHwKkZ` prev
      LEFT JOIN `my_db`.`next temp` next  /* If this is NULL, delete. If not, don't delete. */
        ON prev.`event_id` <=> next.`event_id`
      JOIN `my_db`.`my_table " ` curr
        ON prev.`event_id` <=> curr.`event_id`
     WHERE next.`event_id` IS NULL;  /* If row is in `next`, don't delete. */
    /* Insert / update next rows. */
    INSERT INTO `my_db`.`my_table " ` (`event_id`, `title`, `updated_ts`)
    SELECT `event_id`, `title`, `updated_ts`
      FROM `my_db`.`next temp` next
        ON DUPLICATE KEY UPDATE `event_id` = VALUES(`event_id`),
                                `title` = VALUES(`title`),
                                `updated_ts` = VALUES(`updated_ts`);
    DROP TEMPORARY TABLE IF EXISTS `my_db`.`_my_table " _prev_MHwKkZ`;
    """
    # Overzealous, but unique v primary semantics are a bit weird on this one.
    # Require a primary key, disallow unique indices. Primary key should _NOT_ be an internal auto-inc,
    # but a user-defined primary key that makes sense.
    assert temp_table_spec.primary_key, "Expected a primary key."
    assert (
        not temp_table_spec.unique_indices
    ), "Wasn't expecting unique keys; is this a temp table's spec?"

    prev_temp_table, create_staging_table_sql = create_staging_table_statement(
        db_name, table_name, temp_table_spec, suffix="prev"
    )
    conn.execute(create_staging_table_sql)
    try:
        conn.execute(
            copy_region_statement(
                db_name,
                table_name,
                prev_temp_table,
                region,
                temp_table_spec.column_names,
            )
        )

        results = apply_minimized_patch(
            conn,
            db_name,
            table_name,
            prev_temp_table,
            next_temp_table,
            column_names=temp_table_spec.column_names,
            primary_key_columns=temp_table_spec.primary_key,
        )
    finally:
        conn.execute(drop_table_statement(db_name, prev_temp_table, temporary=True))

    return results
