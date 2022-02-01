"""
Assertions and limitations:
- No non-primary-key GROUP BYs, no actual aggregations.
- No subqueries
- No ORDER BY, LIMITs
- No LEFT JOINs
- No SELECT DISTINCT, window functions, aggregating functions
- UNIONs acceptable (TODO: distinct v all? Only distinct, right?)

Config:
- primary_key  [Optional: Parsed from GROUP BY.]
- unique_keys  [Optional: Unnecessary due to primary key.]
- keys  [Optional but encouraged. No default keys.]

- updated_ts_column_name: Updated timestamp column. Gets type from destination table.
    Treats ints and decimals as timestamps.

- start_timestamp  [Optional: defaults to NOW(), or only data going forward.]


Context:
- high_water_mark: Unix timestamp (integer) of last time pulled.
- table_spec: Table spec for the destination table.
    Includes all information about primary/unique/regular keys, types, etc

TODO:
- Think out timestamping issues D:::, timezones
"""
from dataclasses import replace
from datetime import datetime
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
from jasmine.etl.query_type_analysis import inferred_query_table_spec
from jasmine.sql.analysis import is_readonly_query, uses_subqueries
from jasmine.sql.ast_nodes import sql_ast_from_str
from jasmine.sql.table_spec import (
    TableSpec,
    create_table_statement,
    drop_table_statement,
)
from jasmine.sql.transforms.upsert import update_upsert_statement


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

    # No UNION DISTINCT
    # No ORDER BYs, LIMITs _anywhere_
    # No SELECT DISTINCT, SUM(...) OVER (....), non-redundant/non-PK GROUP BY, etc
    # assert not top_level_filters(query_ast), "The UPSERT materialization does not support (possibly changing) WHERE clauses."
    # Can I instead force them to never delete / update those? Nope.

    view_sql = self.view.spec["query_text"]
    assert is_readonly_query(
        view_sql
    ), "Views must contain a single read-only query each."
    assert not uses_subqueries(
        view_sql
    ), "The UPSERT materialization does not support subqueries."

    query_ast = sql_ast_from_str(view_sql)
    backend = self.view.project.backend

    # Infer column names and types by asking the database.
    table_spec = inferred_query_table_spec(backend, query_ast)

    table_spec = replace(
        table_spec,
        primary_key=self.config.get("primary_key", table_spec.primary_key),
        unique_indices=self.config.get("unique_keys", {}),
        indices=self.config.get("indices", {}),
    ).with_auto_id()
    table_spec = table_spec.with_key(
        [self.config["updated_ts_column_name"]], unique=False
    ).with_deduped_indices()

    assert (
        table_spec.primary_key
    ), "UPSERT requires a primary key. Add one to the configuration or add a redundant GROUP BY primary_key, ... clause."
    assert (
        self.config["updated_ts_column_name"] in table_spec.column_names
    ), "Updated TS column doesn't show up in query. Try adding an `... AS updated_ts` SELECT alias."

    start_timestamp = self.config.get("start_timestamp", floor(time()))
    assert isinstance(start_timestamp, int)

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
        table_spec=TableSpec.from_dict(self.context["table_spec"]),
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
        self.db_name, self.table_name, idempotent=True
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

    table_spec = TableSpec.from_dict(self.context["table_spec"])

    auto_id_column_name, *column_names = table_spec.column_names
    assert auto_id_column_name.endswith("auto_id")

    updated_ts_column_name = self.config["updated_ts_column_name"]
    update_upsert_sql = update_upsert_statement(
        self.db_name,
        self.table_name,
        self.view.spec["query_text"],
        updated_ts_column_name,
        column_names=table_spec.column_names[1:],  # Remove the auto_id.
    )

    last_updated_ts = self.context["high_water_mark"] - self.config.get(
        "overlap_seconds", 5 * 60
    )

    timestamp_decl_str = table_spec.column_type_decls[updated_ts_column_name].upper()
    if "INT" in timestamp_decl_str or "DECIMAL" in timestamp_decl_str:
        last_updated_ts_expr = last_updated_ts
    else:
        last_updated_ts_expr = {
            "mysql": f"FROM_UNIXTIME({last_updated_ts})",
            "postgres": f"TO_TIMESTAMP({last_updated_ts})",
        }[self.view.project.backend.backend_type]

    update_upsert_materialization_sql = update_upsert_sql.format(
        last_updated_ts_expr=last_updated_ts_expr,
    )

    end_timestamp = datetime.now().timestamp()
    with backend_conn(backend, readonly=False) as conn:
        conn.execute(update_upsert_materialization_sql)

    self.context["high_water_mark"] = end_timestamp

    return "active"


upsert_event_funcs = {
    "verify": verify_upsert,
    "create": create_upsert,
    "terminate": terminate_upsert,
    "update": update_upsert,
}
# TODO: event_retries, event_backoff_policy, event_transition_on_failure?
