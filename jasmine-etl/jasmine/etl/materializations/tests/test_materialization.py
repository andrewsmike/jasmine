"""
- Test ETL logic against:
    - Spec errors
    - Weird transitions
    - Database errors (injected / other)
    - Unusual data
    - Materialization end state

... Hmmm...
- End to end SQL tests (SQL, materialization calls / outcome, SQL, SQL output)

Ephemeral database? ... Yeah, test config.
"""
from contextlib import contextmanager
from os.path import dirname, join
from subprocess import run

from pytest import MonkeyPatch
from sqlalchemy import text

import jasmine.etl.app_base
from jasmine.etl.app_base import app_db_session
from jasmine.etl.backends import table_exists, view_exists
from jasmine.models import View, orm_registry
from jasmine.models.materializations import new_materialization

test_config = {
    "redis": {"url": "redis://redis:6379/1"},
    "database": {
        "username": "jasmine_web_su",
        "password": "password",
        "host": "127.0.0.1",
        "port": "3305",
        "database": "jasmine_test",
    },
    "celery": {
        "broker_url": "pyamqp://username:password@127.0.0.1:5672/",
        "backend_url": "redis://redis:6379/1",
    },
}

test_database_dump_path = join(dirname(__file__), "test_database_dump.sql")


@contextmanager
def prepopulated_worker_test_backend():
    with open(test_database_dump_path, "r") as dump_sql:
        command_parts = [
            "mysql",
            "--user={username}",
            "--password={password}",
            "--host={host}",
            "--port={port}",
            "--database=jasmine_web",
        ]

        run(
            [part.format(**test_config["database"]) for part in command_parts],
            stdin=dump_sql,
            check=True,
        )

        with MonkeyPatch.context() as context:
            context.setattr(jasmine.etl.app_base, "app_config", lambda: test_config)
            yield


def test_view_lifecycle():
    with prepopulated_worker_test_backend():

        # Hardcoded in test dump.
        with app_db_session(orm_registry) as session:
            walk_view_lifecycle(session, 28)


def walk_view_lifecycle(session, view_id: int):
    """
    "proposed": "Received request, need to verify.",
    "rejected": "Materialization specification is invalid for some reason; aborted. See logs for details.",
    "accepted": "Materialization verified; need to create.",
    "could_not_create": "Failed to create materialization; aborted. See logs for details.",
    "active": "Successfully created materialization; active.",
    "could_not_terminate": "Failed to clean up materialization; retrying. See logs for details.",
    "terminated": "Materialization terminated by user.",

    "proposed": {"verify", "terminate"},
    "accepted": {"create", "terminate"},
    "could_not_create": {"terminate"},
    "active": {"terminate"},
    "could_not_terminate": {"terminate"},
    """
    # Import late so mocking captures config.
    # TODO: Make this nicer with decent config setup.
    from jasmine.etl.worker_tasks import execute_materialization_event

    view = session.query(View).get(view_id)
    backend = view.project.backend

    def refresh_mat(preexisting_mat=None):
        mat = new_materialization(
            view=view,
            mat_type_name="view",
            config={},
            preexisting_mat=preexisting_mat,
        )
        session.add(mat)
        session.commit()
        return mat

    def do(event):
        # Flush any dependencies to avoid locking issues.
        session.commit()
        execute_materialization_event(
            mat.materialization_id,
            event,
        )

    # Verify happy-path / basic flow.
    mat = refresh_mat()
    assert mat.state == "proposed"

    do("verify")
    assert mat.state == "accepted"

    do("create")
    assert mat.state == "active"
    assert view_exists(backend, "jasmine_test", "analytics/user_view_facts_view")

    direct_results = session.execute(
        text("SELECT * FROM `jasmine_test`.`analytics/user_view_facts_view`")
    ).fetchall()
    view_results = session.execute(text(view.spec["query_text"])).fetchall()
    assert direct_results == view_results

    do("terminate")
    assert mat.state == "terminated"
    assert not view_exists(backend, "jasmine_test", "analytics/user_view_facts_view")

    # Verify early-termination.
    mat = refresh_mat(mat)
    do("verify")
    do("terminate")
    assert mat.state == "terminated"
    assert not view_exists(backend, "jasmine_test", "analytics/user_view_facts_view")

    # Verify view name collion handling.
    session.execute(
        text("CREATE VIEW `jasmine_test`.`analytics/user_view_facts_view` AS SELECT 1;")
    )
    mat = refresh_mat(mat)
    do("verify")
    do("create")
    assert mat.state == "could_not_create"
    assert view_exists(backend, "jasmine_test", "analytics/user_view_facts_view")

    do("terminate")
    assert mat.state == "terminated"
    assert view_exists(backend, "jasmine_test", "analytics/user_view_facts_view")
    session.execute(text("DROP VIEW `jasmine_test`.`analytics/user_view_facts_view`;"))

    # Verify table name collion handling.
    session.execute(
        text("CREATE TABLE `jasmine_test`.`analytics/user_view_facts_view` (pk INT);")
    )
    mat = refresh_mat(mat)
    do("verify")
    do("create")
    assert mat.state == "could_not_create"
    assert table_exists(backend, "jasmine_test", "analytics/user_view_facts_view")

    do("terminate")
    assert mat.state == "terminated"
    assert table_exists(backend, "jasmine_test", "analytics/user_view_facts_view")
    session.execute(text("DROP TABLE `jasmine_test`.`analytics/user_view_facts_view`;"))

    # Verify manual delete handling.
    mat = refresh_mat(mat)
    do("verify")
    do("create")
    session.execute(text("DROP VIEW `jasmine_test`.`analytics/user_view_facts_view`;"))
    do("terminate")
    assert mat.state == "terminated"
