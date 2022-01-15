"""
Use CDC/history tables to determine what chunks of the table need to be rewritten, then regenerate and insert them.
Keep high-water marks for all source tables; possibly dynamically scope input rows during processing.

This is a relatively complex process.

Method:
- [OPT] Generate temporary tables for the previous, next data from the CDC table.
- Generate complicated queries that determine the set of affected chunks.
    - For previous and next data for the source tables
        - For every source table, generate the set of chunk IDs that were affected by the previous/next
            rows, accounting for propagating through all JOINs.
        - JOIN order may be determined through nontrivial heuristic process, possibly EXPLAIN data.
- Once set of chunks is identified, rerun query against source data, constrained to particular chunk(s).
    - Use rewriter invert aggregating datetime function constraints for efficient indexing.
- Diff the result into the destination table.
- Update the CDC table high-water marks


So this relies on a few things:
- Dynamical backoff process [DELAY]
- Temp table generation (previous/next, PKs, target_data)
- Pre-existing CDC tables [PROTOTYPE-WORTHY]
- A specific location for high-water marks  [Jasmine schema or their schema?]
- Consistency semantics that support this nonsense (specifically re:source table operations during work.)
    - Idea: Read top of source tables, CDC tables, will this effectively lock the table?
    - Idea: Just use CDC, add extra checks to avoid inconsistencies / only use current table for rows that aren't in prev/next and aren't updated after current process
- Complicated SQL query rewriting
- Nontrivial JOIN-path representation with solid heuristics, possible integrations with EXPLAIN data.


Incrementally reload chunks of the table as their inputs change, at a regular interval.

Config:
- primary_key  [Optional: Parsed from GROUP BY.]
- chunk_key [Optional: Assumed to be primary_key.]
- unique_keys  [Optional: Unnecessary due to primary key.]
- keys  [Optional but encouraged. No default keys.]

Context:
- last_updated: Unix timestamp (integer) of last time pulled.
- table_spec: Table spec for the destination table.
    Includes all information about primary/unique/regular keys, types, etc
"""
from dataclasses import replace
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
from jasmine.etl.query_type_analysis import inferred_query_table_spec
from jasmine.etl.table_diff import patch_target_table_region
from jasmine.sql.analysis import is_readonly_query
from jasmine.sql.ast_nodes import sql_ast_from_str
from jasmine.sql.table_spec import (
    TableSpec,
    create_staging_table_statement,
    create_table_statement,
    drop_table_statement,
)
from jasmine.sql.transforms.basic_statements import insert_into_statement


def incremental_resource_names(self):
    """
    Set of table, view, and trigger names used by this materialization.
    Used in verifying CREATE / TERMINATE operations.
    """
    return ResourceNames(
        tables={(self.db_name, self.table_name)},
    )


@set_state_on_exception("rejected", (SyntaxError, AssertionError, ValueError))
def verify_incremental(self, session):

    # Leave asserting to creation.
    # assert_names_available(self.view.project.backend, incremental_resource_names(self))

    view_sql = self.view.spec["query_text"]
    assert is_readonly_query(
        view_sql
    ), "Views must contain a single read-only query each."

    query_ast = sql_ast_from_str(view_sql)

    backend = self.view.project.backend
    table_spec = inferred_query_table_spec(backend, query_ast, require_primary_key=True)

    table_spec = replace(
        table_spec,
        primary_key=self.config.get("primary_key", table_spec.primary_key),
        unique_indices=self.config.get("unique_keys", {}),
        indices=self.config.get("indices", {}),
    )
    table_spec = table_spec.with_deduped_indices()
    assert (
        table_spec.primary_key
    ), "Incremental materializations require a primary key. Try adding a no-op GROUP BY clause."

    self.context = {
        "table_spec": table_spec,
        "last_updated": None,
    }

    return "accepted"


@set_state_on_exception("could_not_create", (Exception,))
def create_incremental(self, session):
    backend = self.view.project.backend

    assert_names_available(backend, incremental_resource_names(self))

    create_incremental_sql = create_table_statement(
        db_name=self.db_name,
        table_name=self.table_name,
        table_spec=TableSpec.from_dict(self.context["table_spec"]),
        temporary=False,
        if_not_exists=False,
    )

    with backend_conn(backend, readonly=False) as conn:
        with edit_resources(self) as resources:
            conn.execute(create_incremental_sql)
            resources.tables.add((self.db_name, self.table_name))

    assert_names_successfully_taken(backend, incremental_resource_names(self))

    return "active"


@set_state_on_exception("could_not_terminate", (Exception,))
def terminate_incremental(self, session):
    backend = self.view.project.backend

    incremental_path = (self.db_name, self.table_name)
    dirty_resources = ResourceNames.from_materialization(self)

    # TODO: Verify nobody renamed the incremental on us.
    drop_incremental_sql = drop_table_statement(
        self.db_name, self.table_name, idempotent=True
    )

    with backend_conn(backend, readonly=False) as conn:
        with edit_resources(self) as resources:
            if (incremental_path in resources.tables) and table_exists(
                backend, *incremental_path
            ):
                conn.execute(drop_incremental_sql)
            resources.tables.discard(incremental_path)

            assert resources.empty(), str(resources)

    assert_names_available(backend, dirty_resources)

    return "terminated"


def update_incremental(self, session):

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
        title="Materilaization fully incrementaled",
        description=f"Row stats:\n{pformat(stats)}",
        materialization=self,
    )

    return "active"


incremental_event_funcs = {
    "verify": verify_incremental,
    "create": create_incremental,
    "terminate": terminate_incremental,
    "update": update_incremental,
}
# TODO: event_retries, event_backoff_policy, event_transition_on_failure?
