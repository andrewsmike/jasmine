"""
User config:

Assertions:
- No GROUP BYs (aggregations are incompat with this pattern)
- No subqueries



Config:
- column_type_decls
    - Future feature: autodetect type decls from simple source columns

- unique_keys
- updated_ts_column_name: Updated timestamp column. Gets type from destination table.
    Treats ints and decimals as timestamps.

- keys

- start_timestamp: Optional start timestamp. Defaults to NOW().


Context:
- high_water_mark: Unix timestamp (integer) of last time pulled.
- table_spec: Table spec for the destination table.
    Includes all information about primary/unique/regular keys, types, etc

TODO:
- Think out timestamping issues D:::, timezones
- How are ORDER BYs retained?
- Alllll the JOIN issues
"""
from math import floor
from time import time

from jasmine.etl.backends import backend_conn, table_exists
from jasmine.etl.ddl_tools import (
    ResourceNames,
    assert_names_available,
    assert_names_successfully_taken,
)
from jasmine.etl.materializations.etl_tools import (
    edit_resources,
    set_state_on_exception,
)
from jasmine.sql.analysis import is_readonly_query, query_column_names
from jasmine.sql.table_spec import TableSpec, create_table_statement, drop_table_statement
from jasmine.sql.transforms.upsert import (
    update_upsert_statement,
)


def upsert_resource_names(self):
    """
    Set of table, view, and trigger names used by this materialization.
    Used in verifying CREATE / TERMINATE operations.
    """
    return ResourceNames(
        tables={(self.db_name, self.table_name)},
    )


@set_state_on_exception("rejected", (SyntaxError, AssertionError, ValueError))
def verify_upsert(self, session):

    # Leave asserting to creation.
    # assert_names_available(self.view.project.backend, upsert_resource_names(self))

    view_sql = self.view.spec["query_text"]
    assert is_readonly_query(view_sql)

    column_names = query_column_names(view_sql)

    assert updated_ts_column_name in column_names

    if start_timestamp is None:
        start_timestamp = floor(time())
    assert isinstance(start_timestamp, int)

    table_spec = TableSpec(
        column_names=["auto_id"] + column_names,
        column_type_decls={
            **{"auto_id": "BIGINT NOT NULL AUTO_INCREMENT"},
            **self.config["column_type_decls"]
        },
        primary_key="auto_id",
        unique_indices=self.config["unique_keys"],
        keys=self.config["keys"],
    )

    self.context = {
        "high_water_mark": start_timestamp,
        "table_spec": table_spec,
    }

    return "accepted"


@set_state_on_exception("could_not_create", (Exception,))
def create_upsert(self, session):
    backend = self.view.project.backend

    assert_names_available(backend, upsert_resource_names(self))

    create_upsert_sql = create_table_statement(
        db_name=self.db_name,
        table_name=self.table_name,
        table_spec=TableSpec.from_json(self.context["table_spec"]),
        temporary=False,
        if_not_exists=False,
    )

    with backend_conn(backend, readonly=False) as conn:
        with edit_resources(self) as resources:
            conn.execute(create_upsert_sql)
            resources.tables.add((self.db_name, self.table_name))

    assert_names_successfully_taken(backend, upsert_resource_names(self))

    return "active"


@set_state_on_exception("could_not_terminate", (Exception,))
def terminate_upsert(self, session):
    backend = self.view.project.backend

    upsert_path = (self.db_name, self.table_name)
    dirty_resources = ResourceNames.from_materialization(self)

    # TODO: Verify nobody renamed the upsert on us.
    drop_upsert_sql = drop_table_statement(
        self.db_name, self.table_name, idempotent=False
    )

    with backend_conn(backend, readonly=False) as conn:
        with edit_resources(self) as resources:
            if (upsert_path in resources.tables) and table_exists(
                backend, *upsert_path
            ):
                conn.execute(drop_upsert_sql)
            resources.tables.discard(upsert_path)

            assert resources.empty(), str(resources)

    assert_names_available(backend, dirty_resources)

    return "terminated"


def update_upsert(self, session):
    backend = self.view.project.backend

    upsert_path = (self.db_name, self.table_name)

    updated_ts_column_name = self.config["updated_ts_column_name"]
    update_upsert_sql = update_upsert_statement(
        self.db_name, self.table_name, self.view.spec["query_text"], updated_ts_column_name,
    )

    last_updated_ts = self.config["high_water_mark"]

    table_spec = TableSpec.from_json(self.context["table_spec"])

    timestamp_decl_str = table_spec["column_type_decls"][last_updated_ts_column_name].upper()
    if "INT" in timestamp_decl_str or "DECIMAL" in timestamp_decl_str:
        last_updated_ts_expr = last_updated_ts
    else:
        last_updated_ts_expr = {
            "mysql": f"FROM_UNIXTIME({last_updated_ts})",
            "postgres": f"TO_TIMESTAMP({last_updated_ts})",
        }[self.view.project.backend.backend_type]

    with backend_conn(backend, readonly=False) as conn:
        conn.execute(update_upsert_sql.format(
            last_updated_ts_expr=last_updated_ts_expr,
        ))

    return "active"


view_event_funcs = {
    "verify": verify_upsert,
    "create": create_upsert,
    "terminate": terminate_upsert,
    "update": update_upsert,
}
# TODO: event_retries, event_backoff_policy, event_transition_on_failure?
