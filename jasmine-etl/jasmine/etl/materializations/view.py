from jasmine.etl.backends import new_backend_conn
from jasmine.sql.analysis import is_readonly_query
from jasmine.sql.transforms.view import create_view_statement, drop_view_statement


def verify_view(self, session):
    view_sql = self.view.spec["query_text"]

    try:
        assert is_readonly_query(view_sql)
    except (SyntaxError, AssertionError, ValueError):
        return "bad_spec"

    return "accepted"


def create_view(self, session):
    create_view_sql = create_view_statement(
        self.db_name, self.table_name, self.view.spec["query_text"]
    )

    try:
        with new_backend_conn(self.view.project.backend, readonly=False) as conn:
            conn.execute(create_view_sql)
    except Exception as e:
        print(e)
        return "could_not_create"

    return "active"


def terminate_view(self, session):
    # TODO: Verify nobody renamed the views on us.
    drop_view_sql = drop_view_statement(self.db_name, self.table_name)

    with new_backend_conn(self.view.project.backend, readonly=False) as conn:
        conn.execute(drop_view_sql)

    return "terminated"


view_event_funcs = {
    "verify": verify_view,
    "create": create_view,
    "terminate": terminate_view,
}
# TODO: event_retries, event_backoff_policy, event_transition_on_failure?
