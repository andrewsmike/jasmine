from jasmine.etl.backends import backend_conn, view_exists
from jasmine.etl.ddl_tools import (
    ResourceNames,
    assert_names_available,
    assert_names_successfully_taken,
)
from jasmine.etl.materializations.etl_tools import (
    edit_resources,
    set_state_on_exception,
)
from jasmine.sql.analysis import is_readonly_query
from jasmine.sql.transforms.view import create_view_statement, drop_view_statement


def view_resource_names(self):
    """
    Set of table, view, and trigger names used by this materialization.
    Used in verifying CREATE / TERMINATE operations.
    """
    return ResourceNames(
        views={(self.db_name, self.table_name)},
    )


@set_state_on_exception("rejected", (SyntaxError, AssertionError, ValueError))
def verify_view(self, session):

    # Leave asserting to creation.
    # assert_names_available(self.view.project.backend, view_resource_names(self))

    view_sql = self.view.spec["query_text"]
    assert is_readonly_query(view_sql)

    return "accepted"


@set_state_on_exception("could_not_create", (Exception,))
def create_view(self, session):
    backend = self.view.project.backend

    assert_names_available(backend, view_resource_names(self))

    view_path = (self.db_name, self.table_name)
    create_view_sql = create_view_statement(*view_path, self.view.spec["query_text"])

    with backend_conn(backend, readonly=False) as conn:
        with edit_resources(self) as resources:
            conn.execute(create_view_sql)
            resources.views.add(view_path)

    assert_names_successfully_taken(backend, view_resource_names(self))

    return "active"


@set_state_on_exception("could_not_terminate", (Exception,))
def terminate_view(self, session):
    backend = self.view.project.backend

    view_path = (self.db_name, self.table_name)
    dirty_resources = ResourceNames.from_materialization(self)

    # TODO: Verify nobody renamed the views on us.
    drop_view_sql = drop_view_statement(self.db_name, self.table_name)

    with backend_conn(backend, readonly=False) as conn:
        with edit_resources(self) as resources:
            if (view_path in resources.views) and view_exists(backend, *view_path):
                conn.execute(drop_view_sql)
            resources.views.discard(view_path)

            assert resources.empty(), str(resources)

    assert_names_available(backend, dirty_resources)

    return "terminated"


view_event_funcs = {
    "verify": verify_view,
    "create": create_view,
    "terminate": terminate_view,
}
# TODO: event_retries, event_backoff_policy, event_transition_on_failure?
