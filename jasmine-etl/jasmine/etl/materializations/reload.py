"""
Completely reload the table at a regular interval.

Config:
- column_type_decls
    - Future feature: autodetect type decls from simple source columns

- primary_key
- unique_keys
- keys

Context:
- last_updated: Unix timestamp (integer) of last time pulled.
- table_spec: Table spec for the destination table.
    Includes all information about primary/unique/regular keys, types, etc
"""
from datetime import datetime
from pprint import pformat

from jasmine.etl.backends import backend_conn, table_exists
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
from jasmine.etl.table_diff import patch_target_table_region
from jasmine.sql.analysis import is_readonly_query, query_column_names
from jasmine.sql.ast_nodes import sql_ast_from_str
from jasmine.sql.table_spec import (
    TableSpec,
    create_staging_table_statement,
    create_table_statement,
    drop_table_statement,
)
from jasmine.sql.transforms.basic_statements import insert_into_statement


def reload_resource_names(self):
    """
    Set of table, view, and trigger names used by this materialization.
    Used in verifying CREATE / TERMINATE operations.
    """
    return ResourceNames(
        tables={(self.db_name, self.table_name)},
    )


@set_state_on_exception("rejected", (SyntaxError, AssertionError, ValueError))
def verify_reload(self, session):

    # Leave asserting to creation.
    # assert_names_available(self.view.project.backend, reload_resource_names(self))

    view_sql = self.view.spec["query_text"]
    assert is_readonly_query(
        view_sql
    ), "Views must contain a single read-only query each."

    column_names = query_column_names(sql_ast_from_str(view_sql))

    table_spec = TableSpec(
        column_names=column_names,
        column_type_decls=self.config["column_type_decls"],
        primary_key=self.config.get("primary_key", column_names),
        unique_indices=self.config.get("unique_keys", {}),
        indices=self.config.get("keys", {}),
    ).with_deduped_indices()

    self.context = {
        "table_spec": table_spec,
        "last_updated": None,
    }

    return "accepted"


@set_state_on_exception("could_not_create", (Exception,))
def create_reload(self, session):
    backend = self.view.project.backend

    assert_names_available(backend, reload_resource_names(self))

    create_reload_sql = create_table_statement(
        db_name=self.db_name,
        table_name=self.table_name,
        table_spec=TableSpec.from_dict(self.context["table_spec"]),
        temporary=False,
        if_not_exists=False,
    )

    with backend_conn(backend, readonly=False) as conn:
        with edit_resources(self) as resources:
            conn.execute(create_reload_sql)
            resources.tables.add((self.db_name, self.table_name))

    assert_names_successfully_taken(backend, reload_resource_names(self))

    return "active"


@set_state_on_exception("could_not_terminate", (Exception,))
def terminate_reload(self, session):
    backend = self.view.project.backend

    reload_path = (self.db_name, self.table_name)
    dirty_resources = ResourceNames.from_materialization(self)

    # TODO: Verify nobody renamed the reload on us.
    drop_reload_sql = drop_table_statement(
        self.db_name, self.table_name, idempotent=True
    )

    with backend_conn(backend, readonly=False) as conn:
        with edit_resources(self) as resources:
            if (reload_path in resources.tables) and table_exists(
                backend, *reload_path
            ):
                conn.execute(drop_reload_sql)
            resources.tables.discard(reload_path)

            assert resources.empty(), str(resources)

    assert_names_available(backend, dirty_resources)

    return "terminated"


def update_reload(self, session):

    backend = self.view.project.backend

    table_spec = TableSpec.from_dict(self.context["table_spec"])

    temp_table_spec = table_spec.without_constraints().with_deduped_indices()

    results_temp_table, create_results_temp_table_sql = create_staging_table_statement(
        self.db_name, self.table_name, temp_table_spec, suffix="next"
    )

    with backend_conn(backend, readonly=False) as conn:
        conn.execute(create_results_temp_table_sql)
        conn.execute(
            insert_into_statement(
                self.db_name,
                results_temp_table,
                self.view.spec["query_text"],
                column_names=temp_table_spec.column_names,
            )
        )
        # Update the entire table simultaneously.
        stats = patch_target_table_region(
            conn,
            self.db_name,
            self.table_name,
            next_temp_table=results_temp_table,
            temp_table_spec=temp_table_spec,
            region=None,
        )

    self.context["last_updated"] = datetime.now().timestamp()

    attempt_log_backend_event(
        title="Materilaization fully reloaded",
        description=f"Row stats:\n{pformat(stats)}",
        materialization=self,
    )

    return "active"


reload_event_funcs = {
    "verify": verify_reload,
    "create": create_reload,
    "terminate": terminate_reload,
    "update": update_reload,
}
# TODO: event_retries, event_backoff_policy, event_transition_on_failure?
