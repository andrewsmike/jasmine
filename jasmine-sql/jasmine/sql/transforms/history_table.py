"""
Change Data Capture tables (AKA history tables, AKA audit tables) record all INSERTs,
UPDATEs, and DELETEs to a given table. Here, we implement this using database triggers.

To do this, we must be able to:
- Generate the audit table's schema, including all necessary keys and additional rows.
    Columns: A no-op autoincrement primary key (because multiple rows per second?), an operation, a timestamp.
    Keys: Primary key indexing (then timestamp), Timestamp

- Generate the trigger statements.
"""
from dataclasses import replace
from typing import Literal

from jasmine.sql.table_spec import TableSpec, create_table_statement, next_indexed_name
from jasmine.sql.transforms.escaping import escaped, escaped_db_table, unescaped


def history_table_spec_from_table_spec(table_spec: TableSpec):
    """
    - Add [event_id, op_type], and [event_ts] columns.
    - Turn foreign, unique, and primary keys into regular keys.
    - Deduplicate regular keys (no key should be a strict prefix of another, retain the longer one.)
    - Primary key event_id
    - Add key event_ts
    - Add key (*primary_key, event_ts)

    Idea: Add event_ts to end of all existing keys. May improve query performance.

    >>> from jasmine.sql.table_spec import create_table_statement, example_table_spec
    >>> from pprint import pprint

    >>> pprint(example_table_spec)
    TableSpec(column_names=['user_id', 'name', 'parent_user_id'],
              column_type_decls={'name': 'VARCHAR(96) NOT NULL',
                                 'parent_user_id': 'BIGINT',
                                 'user_id': 'INTEGER NOT NULL'},
              primary_key=['user_id'],
              indices={'org_name': ['parent_user_id', 'name']},
              unique_indices={'unique_key_0': ['name'],
                              'unique_key_1': ['parent_user_id']},
              foreign_keys=[ForeignKey(name=None,
                                       dest_db_name='main',
                                       dest_table_name='users " ',
                                       source_columns=['parent_user_id'],
                                       dest_columns=['user_id'])])

    >>> pprint(history_table_spec_from_table_spec(example_table_spec))
    TableSpec(column_names=['_jsmn_event_id_1',
                            '_jsmn_op_type_1',
                            'user_id',
                            'name',
                            'parent_user_id',
                            '_jsmn_event_ts_1'],
              column_type_decls={'_jsmn_event_id_1': 'bigint NOT NULL '
                                                     'AUTO_INCREMENT',
                                 '_jsmn_event_ts_1': 'bigint NOT NULL',
                                 '_jsmn_op_type_1': 'enum("INSERT", '
                                                    '"INSERT_UPDATE", "DELETE", '
                                                    '"DELETE_UPDATE") NOT NULL',
                                 'name': 'VARCHAR(96) NOT NULL',
                                 'parent_user_id': 'BIGINT',
                                 'user_id': 'INTEGER NOT NULL'},
              primary_key=['_jsmn_event_id_1'],
              indices={'_jsmn_key_0': ['_jsmn_event_ts_1'],
                       '_jsmn_key_1': ['name'],
                       '_jsmn_key_2': ['parent_user_id', 'name'],
                       '_jsmn_key_3': ['user_id', '_jsmn_event_ts_1']},
              unique_indices={},
              foreign_keys=[])
    >>> print(create_table_statement("main", 'user_history " ', history_table_spec_from_table_spec(example_table_spec)))
    CREATE TABLE `main`.`user_history " ` (
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
    """
    assert table_spec.primary_key, "Table must have a primary key."

    event_id_column = next_indexed_name(set(table_spec.column_names), "_jsmn_event_id")
    op_type_column = next_indexed_name(set(table_spec.column_names), "_jsmn_op_type")
    event_ts_column = next_indexed_name(set(table_spec.column_names), "_jsmn_event_ts")

    # TODO: Expand to other db types.
    bigint = "bigint"

    return (
        replace(
            table_spec,
            primary_key=[event_id_column],
            column_names=[event_id_column, op_type_column]
            + table_spec.column_names
            + [event_ts_column],
            column_type_decls={
                event_id_column: f"{bigint} NOT NULL AUTO_INCREMENT",
                op_type_column: 'enum("INSERT", "INSERT_UPDATE", "DELETE", "DELETE_UPDATE") NOT NULL',
                event_ts_column: f"{bigint} NOT NULL",
                **table_spec.column_type_decls,
            },
        )
        .without_constraints()
        .with_key([event_ts_column])
        .with_key(table_spec.primary_key + [event_ts_column])
        .with_deduped_indices()
    )


def create_history_table_statement(
    base_table_spec: TableSpec,
    db_name: str,
    table_name: str,
    if_not_exists: bool = True,
) -> str:
    """
    The SQL DDL to create the underlying table for a history table, given the source table's spec.

    >>> from jasmine.sql.table_spec import example_table_spec
    >>> print(create_history_table_statement(example_table_spec, "main", 'users " _history'))
    CREATE TABLE IF NOT EXISTS `main`.`users " _history` (
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
    """
    return create_table_statement(
        db_name,
        table_name,
        history_table_spec_from_table_spec(base_table_spec),
        temporary=False,
        if_not_exists=if_not_exists,
    )


TriggerType = Literal["INSERT", "UPDATE", "DELETE"]
ordered_trigger_types: list[TriggerType] = ["INSERT", "UPDATE", "DELETE"]


def history_trigger_name(
    db_name: str, table_name: str, suffix: str, trigger_type: TriggerType
) -> str:
    trigger_name = f"_jsmn_hist_{suffix}_{unescaped(table_name)}_{trigger_type.lower()}"
    assert (
        len(trigger_name) <= 64
    ), f"Cannot create trigger, name would be too long: len('{trigger_name}') > 64"
    return trigger_name


def lock_unlock_tables_statements(
    db_table_names: list[tuple[str, str]]
) -> tuple[str, str]:
    escaped_table_names = ",\n            ".join(
        escaped_db_table(*db_table_name) + " WRITE" for db_table_name in db_table_names
    )
    return (f"LOCK TABLES {escaped_table_names};", "UNLOCK TABLES;")


create_insert_trigger_template = """
CREATE TRIGGER {trigger_name} AFTER INSERT ON {source_table}
FOR EACH ROW
    BEGIN
        INSERT INTO {history_table} (
            {op_type_column},
            {columns_str},
            {event_ts_column}
        )
        VALUES (
            'INSERT',
            {new_columns_str},
            UNIX_TIMESTAMP()
        );
    END
""".strip()

create_update_trigger_template = """
CREATE TRIGGER {trigger_name} AFTER UPDATE ON {source_table}
FOR EACH ROW
    BEGIN
        INSERT INTO {history_table} (
            {op_type_column},
            {columns_str},
            {event_ts_column}
        )
        VALUES (
            'DELETE_UPDATE',
            {old_columns_str},
            UNIX_TIMESTAMP()
        );
        INSERT INTO {history_table} (
            {op_type_column},
            {columns_str},
            {event_ts_column}
        )
        VALUES (
            'INSERT_UPDATE',
            {new_columns_str},
            UNIX_TIMESTAMP()
        );
    END
""".strip()

create_delete_trigger_template = """
CREATE TRIGGER {trigger_name} AFTER DELETE ON {source_table}
FOR EACH ROW
    BEGIN
        INSERT INTO {history_table} (
            {op_type_column},
            {columns_str},
            {event_ts_column}
        )
        VALUES (
            'DELETE',
            {old_columns_str},
            UNIX_TIMESTAMP()
        );
    END
""".strip()

create_trigger_templates: dict[TriggerType, str] = {
    "INSERT": create_insert_trigger_template,
    "UPDATE": create_update_trigger_template,
    "DELETE": create_delete_trigger_template,
}


def create_history_table_trigger_statements(
    table_spec: TableSpec,
    src_db_name: str,
    src_table_name: str,
    trigger_suffix: str,
    dest_table_spec: TableSpec,
    dest_db_name: str,
    dest_table_name: str,
) -> dict[str, str]:

    (event_id_column, op_type_column), event_ts_column = (
        dest_table_spec.column_names[:2],
        dest_table_spec.column_names[-1],
    )

    escaped_column_names = [
        escaped(column_name) for column_name in table_spec.column_names
    ]
    old_column_names = [f"OLD.{column_name}" for column_name in escaped_column_names]
    new_column_names = [f"NEW.{column_name}" for column_name in escaped_column_names]

    sep = ",\n            "
    columns_str = sep.join(escaped_column_names)
    old_columns_str = sep.join(old_column_names)
    new_columns_str = sep.join(new_column_names)

    return {
        trigger_type: create_trigger_template_str.format(
            **{
                "source_table": escaped_db_table(src_db_name, src_table_name),
                "history_table": escaped_db_table(dest_db_name, dest_table_name),
                "trigger_name": escaped(
                    history_trigger_name(
                        src_db_name, src_table_name, trigger_suffix, trigger_type
                    ),
                ),
                "columns_str": columns_str,
                "old_columns_str": old_columns_str,
                "new_columns_str": new_columns_str,
                "event_id_column": event_id_column,
                "op_type_column": op_type_column,
                "event_ts_column": event_ts_column,
            }
        )
        for trigger_type, create_trigger_template_str in create_trigger_templates.items()
    }


def drop_history_table_trigger_statements(
    db_name: str, table_name: str, trigger_suffix: str
) -> dict[str, str]:
    return {
        trigger_type: (
            "DROP TRIGGER IF EXISTS "
            + escaped(
                history_trigger_name(db_name, table_name, trigger_suffix, trigger_type),
            )
            + ";"
        )
        for trigger_type in ordered_trigger_types
    }


def refresh_history_table_triggers_statement(
    src_table_spec: TableSpec,
    src_db_name: str,
    src_table_name: str,
    trigger_suffix: str,
    dest_table_spec: TableSpec,
    dest_db_name: str,
    dest_table_name: str,
) -> str:
    """
    History table refreshing DDL script with appropriate comments.

    This demonstrates how to chain together the above DDL statements to destroy / create
    history tables. Ideally, ETLs will perform these steps sequentially for better error handling and
    rollback.

    >>> from jasmine.sql.table_spec import example_table_spec
    >>> print(refresh_history_table_triggers_statement(
    ...     src_table_spec=example_table_spec,
    ...     src_db_name="main",
    ...     src_table_name='users " ',
    ...     trigger_suffix="table",
    ...     dest_table_spec=history_table_spec_from_table_spec(example_table_spec),
    ...     dest_db_name="main",
    ...     dest_table_name='users " _history',
    ... ))
    /* CDC / history table template autogenerated by jasmine-sql. */
    CREATE TABLE IF NOT EXISTS `main`.`users " _history` (
        `_jsmn_event_id_1` bigint NOT NULL AUTO_INCREMENT,
        `_jsmn_op_type_1` enum("INSERT", "INSERT_UPDATE", "DELETE", "DELETE_UPDATE") NOT NULL,
        `user_id` INTEGER NOT NULL,
    ...
        KEY _jsmn_key_3 (`user_id`, `_jsmn_event_ts_1`)
    );
    <BLANKLINE>
    /* Lock table so triggers don't miss any incoming transactions. */
    LOCK TABLES `main`.`users " ` WRITE;
    <BLANKLINE>
    /* You can't edit or conditionally create triggers. Instead, we drop / create them again. */
    DROP TRIGGER IF EXISTS `_jsmn_hist_table_users " _insert`;
    DROP TRIGGER IF EXISTS `_jsmn_hist_table_users " _update`;
    DROP TRIGGER IF EXISTS `_jsmn_hist_table_users " _delete`;
    <BLANKLINE>
    DELIMITER $$
    CREATE TRIGGER `_jsmn_hist_table_users " _insert` AFTER INSERT ON `main`.`users " `
    FOR EACH ROW
        BEGIN
            INSERT INTO `main`.`users " _history` (
                _jsmn_op_type_1,
                `user_id`,
                `name`,
                `parent_user_id`,
                _jsmn_event_ts_1
            )
            VALUES (
                'INSERT',
                NEW.`user_id`,
                NEW.`name`,
                NEW.`parent_user_id`,
                UNIX_TIMESTAMP()
            );
        END; $$
    DELIMITER ;
    <BLANKLINE>
    DELIMITER $$
    CREATE TRIGGER `_jsmn_hist_table_users " _update` AFTER UPDATE ON `main`.`users " `
    FOR EACH ROW
        BEGIN
            INSERT INTO `main`.`users " _history` (
    ...
            );
            INSERT INTO `main`.`users " _history` (
    ...
            );
        END; $$
    DELIMITER ;
    <BLANKLINE>
    DELIMITER $$
    CREATE TRIGGER `_jsmn_hist_table_users " _delete` AFTER DELETE ON `main`.`users " `
    FOR EACH ROW
        BEGIN
            INSERT INTO `main`.`users " _history` (
    ...
            );
        END; $$
    DELIMITER ;
    <BLANKLINE>
    UNLOCK TABLES;
    """
    idempotent_create_table_sql = create_history_table_statement(
        base_table_spec=src_table_spec,
        db_name=dest_db_name,
        table_name=dest_table_name,
    )

    lock_table_sql, unlock_table_sql = lock_unlock_tables_statements(
        [(src_db_name, src_table_name)]
    )
    drop_triggers_sql = "\n".join(
        drop_history_table_trigger_statements(
            src_db_name, src_table_name, trigger_suffix
        ).values()
    )
    create_triggers_sql = (
        "DELIMITER $$\n"
        + "; $$\nDELIMITER ;\n\nDELIMITER $$\n".join(
            create_history_table_trigger_statements(
                src_table_spec,
                src_db_name,
                src_table_name,
                trigger_suffix,
                dest_table_spec,
                dest_db_name,
                dest_table_name,
            ).values()
        )
        + "; $$\nDELIMITER ;"
    )

    return "\n".join(
        [
            "/* CDC / history table template autogenerated by jasmine-sql. */",
            idempotent_create_table_sql,
            "",
            "/* Lock table so triggers don't miss any incoming transactions. */",
            lock_table_sql,
            "",
            "/* You can't edit or conditionally create triggers. Instead, we drop / create them again. */",
            drop_triggers_sql,
            "",
            create_triggers_sql,
            "",
            unlock_table_sql,
        ]
    )


trim_history_table_template = """
DELETE
  FROM {escaped_db_table}
 WHERE {escaped_event_ts_column} < {oldest_timestamp};
"""[
    1:-1
]


def trim_history_table_statement(
    db_name: str,
    table_name: str,
    oldest_timestamp: int,
    event_ts_column: str = "_jsmn_event_ts_1",
) -> str:
    """
    >>> print(
    ...     trim_history_table_statement("my db ' ", "my $# table", 1642005618, "_jsmn_event_ts_1")
    ... )
    DELETE
      FROM `my db ' `.`my $# table`
     WHERE `_jsmn_event_ts_1` < 1642005618;
    """
    return trim_history_table_template.format(
        escaped_db_table=escaped_db_table(db_name, table_name),
        escaped_event_ts_column=escaped(event_ts_column),
        oldest_timestamp=oldest_timestamp,
    )
