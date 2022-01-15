"""
Record all changes to the rows in a table using triggers.

Config:
- trim_frequency_seconds: How often should excess rows be DELETEd?
    0 for "never delete".
    Smaller numbers means less excess data, but more DELETE statements running against the table.
    Defaults to 1 hour.

- retention_period_seconds: How long should data be kept?
    0 for "never delete".
    Defaults to 4 days.


Context:
- base_table_spec: Base table's spec when the materialization was created.
- table_spec: Derived history table spec.
- last_trimmed: Last timestamp when the table was trimmed. Used to identify next trimming time.
"""
from datetime import datetime

from jasmine.etl.backends import backend_conn, backend_table_spec, table_exists
from jasmine.etl.ddl_tools import (
    ResourceNames,
    assert_names_available,
    assert_names_successfully_taken,
)
from jasmine.etl.materializations.etl_tools import (
    attempt_log_backend_event,
    edit_resources,
    set_state_on_exception,
)
from jasmine.sql.table_spec import (
    TableSpec,
    create_table_statement,
    drop_table_statement,
)
from jasmine.sql.transforms.history_table import (
    TriggerType,
    create_history_table_trigger_statements,
    drop_history_table_trigger_statements,
    history_table_spec_from_table_spec,
    history_trigger_name,
    lock_unlock_tables_statements,
    ordered_trigger_types,
    trim_history_table_statement,
)

history_table_trigger_suffix = "table"


def history_table_resource_names(self):
    """
    Set of table, view, and trigger names used by this materialization.
    Used in verifying CREATE / TERMINATE operations.
    """
    return ResourceNames(
        tables={(self.db_name, self.table_name)},
        views=set(),
        triggers={
            (
                self.db_name,
                history_trigger_name(
                    self.view.spec["source_db_name"],
                    self.view.spec["source_table_name"],
                    suffix=history_table_trigger_suffix,
                    trigger_type=trigger_type,
                ),
            )
            for trigger_type in ordered_trigger_types
        },
    )


SECONDS = 1
MINUTES = 60 * SECONDS
HOURS = 60 * MINUTES
DAYS = 24 * HOURS
YEARS = 265 * DAYS


@set_state_on_exception("bad_spec", (AssertionError,))
def verify_history_table(self, session):

    backend = self.view.project.backend

    source_db_name, source_table_name = (
        self.view.spec["source_db_name"],
        self.view.spec["source_table_name"],
    )

    freq = self.config.setdefault("trim_frequency_seconds", 1 * HOURS)
    assert isinstance(freq, int) and (0 <= freq < 10 * YEARS)

    retention = self.config.setdefault("retention_period_seconds", 4 * DAYS)
    assert isinstance(retention, int) and (0 <= retention < 100 * YEARS)

    assert table_exists(
        backend,
        source_db_name,
        source_table_name,
    ), "Source table doesn't exist."

    base_table_spec = backend_table_spec(backend, source_db_name, source_table_name)
    self.context = {
        "base_table_spec": base_table_spec,
        "table_spec": history_table_spec_from_table_spec(base_table_spec),
        "last_trimmed": datetime.now().timestamp(),
    }

    return "accepted"


def trigger_resource(
    resources: ResourceNames, trigger_type: TriggerType
) -> tuple[str, str]:
    # Hacky way to get the trigger name without regenerating it from the resource_names.
    for db_name, trigger_name in resources.triggers:
        if trigger_name.endswith(trigger_type.lower()):
            return (db_name, trigger_name)
    else:
        raise RuntimeError("Could not find corresponding trigger.")


@set_state_on_exception("could_not_create", (Exception,))
def create_history_table(self, session):
    """
    Create a history table and associated triggers.
    - Assert the table and triggers don't already exist.
    - Create the history table.
    - Write-lock the upstream table, attempt to create the triggers, unlock.

    Each of these steps may fail. Unrolling is necessary to ensure we leave the database in a clean state.
    TODO: If the database connection fails and we cannot reset anything, prehaps we should have "dirty"
    state and an automatic attempt-cleanup process.
    """
    backend = self.view.project.backend

    resource_names = history_table_resource_names(self)
    assert_names_available(backend, resource_names)

    source_db_name, source_table_name = (
        self.view.spec["source_db_name"],
        self.view.spec["source_table_name"],
    )

    assert table_exists(
        backend, source_db_name, source_table_name
    ), "History table's source table doesn't exist!"

    source_table_spec = TableSpec.from_dict(self.context["base_table_spec"])
    table_spec = TableSpec.from_dict(self.context["table_spec"])

    assert source_table_spec == backend_table_spec(
        backend, source_db_name, source_table_name
    ), "Source table was ALTERed or replaced."
    create_history_table_sql = create_table_statement(
        self.db_name,
        self.table_name,
        table_spec,
        if_not_exists=False,
    )

    lock_source_table_sql, unlock_tables_sql = lock_unlock_tables_statements(
        [(source_db_name, source_table_name)],
    )

    create_trigger_sql_statements = create_history_table_trigger_statements(
        source_table_spec,
        source_db_name,
        source_table_name,
        trigger_suffix=history_table_trigger_suffix,
        dest_table_spec=table_spec,
        dest_db_name=self.db_name,
        dest_table_name=self.table_name,
    )

    with backend_conn(backend, readonly=False) as conn:
        with edit_resources(self) as resources:
            conn.execute(create_history_table_sql)
            resources.tables.add((self.db_name, self.table_name))

        conn.execute(lock_source_table_sql)
        try:
            for (
                trigger_type,
                create_trigger_sql,
            ) in create_trigger_sql_statements.items():
                with edit_resources(self) as resources:
                    conn.execute(create_trigger_sql)
                    resources.triggers.add(
                        trigger_resource(resource_names, trigger_type)
                    )
        finally:
            # TODO: Test this actually works and / or is necessary.
            conn.execute(unlock_tables_sql)

    assert_names_successfully_taken(backend, resource_names)

    self.context["last_trimmed"] = datetime.now().timestamp()

    return "active"


@set_state_on_exception("could_not_terminate", Exception)
def terminate_history_table(self, session):
    """
    Terminate a trigger-generated history table.

    - Write lock the source table.
    - Drop the triggers individually. Once the first one succeeds, we can't back out and retry:
        ETL will end up in "dirty" (on any failure) or "terminated" (on all successes.)
    - Unlock the source table.
    - Drop the history table.
    """
    backend = self.view.project.backend

    source_db_name, source_table_name = (
        self.view.spec["source_db_name"],
        self.view.spec["source_table_name"],
    )

    history_table = (self.db_name, self.table_name)

    lock_source_table_sql, unlock_tables_sql = lock_unlock_tables_statements(
        [(source_db_name, source_table_name)],
    )

    drop_trigger_sql_statements = drop_history_table_trigger_statements(
        source_db_name,
        source_table_name,
        trigger_suffix=history_table_trigger_suffix,
    )

    drop_history_table_sql = drop_table_statement(*history_table, idempotent=True)

    resource_names = history_table_resource_names(self)

    with backend_conn(backend, readonly=False) as conn:

        use_locking = table_exists(backend, source_db_name, source_table_name)
        if use_locking:
            conn.execute(lock_source_table_sql)

        try:
            for trigger_type, drop_trigger_sql in drop_trigger_sql_statements.items():
                with edit_resources(self) as dirty_resources:
                    trigger = trigger_resource(resource_names, trigger_type)
                    if trigger in dirty_resources.triggers:
                        conn.execute(drop_trigger_sql)
                        dirty_resources.triggers.discard(trigger)

        finally:
            # TODO: Test this actually works and / or is necessary.
            # When there's an exception, the connection may be invalidated.
            if use_locking:
                conn.execute(unlock_tables_sql)

        # No locking involved.
        with edit_resources(self) as resources:
            if history_table in resources.tables and table_exists(
                backend, *history_table
            ):
                conn.execute(drop_history_table_sql)
            resources.tables.discard(history_table)

    assert_names_available(backend, resource_names)

    return "terminated"


def trim_history_table(self, session):

    table_spec = TableSpec.from_dict(self.context["table_spec"])
    event_ts_column = table_spec.column_names[-1]

    trim_freq = self.config["trim_frequency_seconds"]
    retention_period = self.config["retention_period_seconds"]

    if trim_freq == 0 or retention_period == 0:
        return "active"

    backend = self.view.project.backend

    now_ts = datetime.now().timestamp()
    next_trim_ts = trim_freq + self.context["last_trimmed"]

    trim_history_table_sql = trim_history_table_statement(
        self.db_name,
        self.table_name,
        oldest_timestamp=now_ts - retention_period,
        event_ts_column=event_ts_column,
    )

    if next_trim_ts <= now_ts:
        with backend_conn(backend, readonly=False) as conn:
            deleted_count = conn.execute(trim_history_table_sql)

        self.context["last_trimmed"] = now_ts

        attempt_log_backend_event(
            title="Successfully trimmed history table.",
            description=f"{deleted_count} rows were deleted.",
            materialization=self,
        )

    return "active"


history_table_event_funcs = {
    "verify": verify_history_table,
    "create": create_history_table,
    "terminate": terminate_history_table,
    "trim": trim_history_table,
}
# TODO: event_retries, event_backoff_policy, interactions with set-state-on-failure.
