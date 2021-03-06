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
from datetime import datetime, timedelta
from os.path import dirname, join
from subprocess import run

from pytest import MonkeyPatch
from sqlalchemy import text

import jasmine.etl.app_base
from jasmine.etl.app_base import app_db_session
from jasmine.etl.backends import table_exists, view_exists
from jasmine.models import View, orm_registry
from jasmine.models.materializations import new_materialization
from jasmine.sql.transforms.escaping import escaped_column_list

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
    # Import late so mocking captures config.
    # TODO: Make this nicer with decent config setup.
    from jasmine.etl.worker_tasks import execute_materialization_event

    view = session.query(View).get(view_id)
    backend = view.project.backend
    mats = [mat for mat in view.materializations if mat.materialization_type == "view"]
    mat = mats[0] if mats else None

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
            schedule_next_event=False,
        )

    if mat is not None and not mat.terminal():
        do("terminate")

    # Verify happy-path / basic flow.
    mat = refresh_mat(preexisting_mat=mat)
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


def test_upsert_lifecycle():
    with prepopulated_worker_test_backend():

        # Hardcoded in test dump.
        with app_db_session(orm_registry) as session:
            walk_upsert_lifecycle(session, 51)


def walk_upsert_lifecycle(session, view_id: int):
    # Import late so mocking captures config.
    # TODO: Make this nicer with decent config setup.
    from jasmine.etl.worker_tasks import execute_materialization_event

    view = session.query(View).get(view_id)
    backend = view.project.backend
    mats = [
        mat for mat in view.materializations if mat.materialization_type == "upsert"
    ]
    mat = mats[0] if mats else None

    column_type_decls = {
        "event_id": "BIGINT NOT NULL",
        "path": "VARCHAR(256)",
        "method": "VARCHAR(64)",
        "state": "VARCHAR(64)",
        "config": "TEXT",
        "context": "TEXT",
        "title": "VARCHAR(255)",
        "description": "VARCHAR(255)",
        "updated_ts": "DATETIME",
    }
    column_names = list(
        column_type_decls.keys()
    )  # Deterministic order guaranteed in python 3.7 and above.
    unique_keys = {"event_id": ["event_id"]}
    keys = {
        "event_id": ["event_id"],
        "path": ["path"],
        "description": ["description"],
        "title": ["title"],
        "title2": ["title", "description"],
    }
    updated_ts_column_name = "updated_ts"
    start_timestamp = int(datetime(2021, 1, 1).timestamp())

    def refresh_mat(preexisting_mat=None):
        config = {
            "column_type_decls": column_type_decls,
            "unique_keys": unique_keys,
            "updated_ts_column_name": updated_ts_column_name,
            "keys": keys,
            "start_timestamp": start_timestamp,
        }
        mat = new_materialization(
            view=view,
            mat_type_name="upsert",
            config=config,
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
            schedule_next_event=False,
        )

    if mat is not None and not mat.terminal():
        do("terminate")

    # Verify happy-path / basic flow.
    mat = refresh_mat(preexisting_mat=mat)
    assert mat.state == "proposed"

    do("verify")
    assert mat.state == "accepted"

    do("create")
    assert mat.state == "active"
    assert table_exists(backend, "jasmine_test", "incremental_demo_upsert")
    assert (
        mat.context["high_water_mark"]
        < (datetime.now() - timedelta(minutes=10)).timestamp()
    )

    direct_results = set(session.execute(text(view.spec["query_text"])).fetchall())

    # Adds rows to backend_events and changes state so do this a step later.
    do("update")
    assert mat.state == "active"
    assert (
        mat.context["high_water_mark"]
        >= (datetime.now() - timedelta(seconds=10)).timestamp()
    )

    upsert_results = set(
        session.execute(
            text(
                f"SELECT {escaped_column_list(column_names)} FROM `jasmine_test`.`incremental_demo_upsert`"
            )
        ).fetchall()
    )
    assert direct_results == upsert_results

    do("terminate")
    assert mat.state == "terminated"
    assert not table_exists(backend, "jasmine_test", "incremental_demo_upsert")

    # Verify early-termination.
    mat = refresh_mat(mat)
    do("verify")
    do("terminate")
    assert mat.state == "terminated"
    assert not table_exists(backend, "jasmine_test", "incremental_demo_upsert")

    # Verify view collion handling.
    session.execute(
        text("CREATE VIEW `jasmine_test`.`incremental_demo_upsert` AS SELECT 1;")
    )
    mat = refresh_mat(mat)
    do("verify")
    do("create")
    assert mat.state == "could_not_create"
    assert view_exists(backend, "jasmine_test", "incremental_demo_upsert")

    do("terminate")
    assert mat.state == "terminated"
    assert view_exists(backend, "jasmine_test", "incremental_demo_upsert")
    session.execute(text("DROP VIEW `jasmine_test`.`incremental_demo_upsert`;"))

    # Verify table name collion handling.
    session.execute(
        text("CREATE TABLE `jasmine_test`.`incremental_demo_upsert` (pk INT);")
    )
    mat = refresh_mat(mat)
    do("verify")
    do("create")
    assert mat.state == "could_not_create"
    assert table_exists(backend, "jasmine_test", "incremental_demo_upsert")

    do("terminate")
    assert mat.state == "terminated"
    assert table_exists(backend, "jasmine_test", "incremental_demo_upsert")
    session.execute(text("DROP TABLE `jasmine_test`.`incremental_demo_upsert`;"))

    # Verify manual delete handling.
    mat = refresh_mat(mat)
    do("verify")
    do("create")
    session.execute(text("DROP TABLE `jasmine_test`.`incremental_demo_upsert`;"))
    do("terminate")
    assert mat.state == "terminated"


def test_reload_lifecycle():
    with prepopulated_worker_test_backend():

        # Hardcoded in test dump.
        with app_db_session(orm_registry) as session:
            walk_reload_lifecycle(session, 51)


def walk_reload_lifecycle(session, view_id: int):
    # Import late so mocking captures config.
    # TODO: Make this nicer with decent config setup.
    from jasmine.etl.worker_tasks import execute_materialization_event

    view = session.query(View).get(view_id)
    backend = view.project.backend
    mats = [
        mat for mat in view.materializations if mat.materialization_type == "reload"
    ]
    mat = mats[0] if mats else None

    column_type_decls = {
        "event_id": "BIGINT NOT NULL",
        "path": "VARCHAR(256)",
        "method": "VARCHAR(64)",
        "state": "VARCHAR(64)",
        "config": "TEXT",
        "context": "TEXT",
        "title": "VARCHAR(255)",
        "description": "VARCHAR(255)",
        "updated_ts": "DATETIME",
    }
    column_names = list(
        column_type_decls.keys()
    )  # Deterministic order guaranteed in python 3.7 and above.
    primary_key = ["event_id"]
    unique_keys: dict[str, list[str]] = {}
    keys = {
        "event_id": ["event_id"],
        "path": ["path"],
        "description": ["description"],
        "title": ["title"],
        "title2": ["title", "description"],
    }
    updated_ts_column_name = "updated_ts"
    start_timestamp = int(datetime(2021, 1, 1).timestamp())

    def refresh_mat(preexisting_mat=None):
        config = {
            "column_type_decls": column_type_decls,
            "primary_key": primary_key,
            "unique_keys": unique_keys,
            "updated_ts_column_name": updated_ts_column_name,
            "keys": keys,
            "start_timestamp": start_timestamp,
        }
        mat = new_materialization(
            view=view,
            mat_type_name="reload",
            config=config,
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
            schedule_next_event=False,
        )

    if mat is not None and not mat.terminal():
        do("terminate")

    # Verify happy-path / basic flow.
    mat = refresh_mat(preexisting_mat=mat)
    assert mat.state == "proposed"

    do("verify")
    assert mat.state == "accepted"

    do("create")
    assert mat.state == "active"
    assert table_exists(backend, "jasmine_test", "incremental_demo_reload")
    assert mat.context["last_updated"] is None

    direct_results = set(session.execute(text(view.spec["query_text"])).fetchall())

    # Adds rows to backend_events and changes state so do this a step later.
    do("update")
    assert mat.state == "active"
    assert mat.context["last_updated"] is not None
    assert (
        mat.context["last_updated"]
        >= (datetime.now() - timedelta(seconds=10)).timestamp()
    )

    reload_results = set(
        session.execute(
            text(
                f"SELECT {escaped_column_list(column_names)} FROM `jasmine_test`.`incremental_demo_reload`"
            )
        ).fetchall()
    )
    assert direct_results == reload_results

    second_direct_results = set(
        session.execute(text(view.spec["query_text"])).fetchall()
    )
    do("update")
    second_reload_results = set(
        session.execute(
            text(
                f"SELECT {escaped_column_list(column_names)} FROM `jasmine_test`.`incremental_demo_reload`"
            )
        ).fetchall()
    )
    assert second_direct_results == second_reload_results

    # Specific to backend_events.
    assert len(reload_results) + 1 == len(second_reload_results)

    do("terminate")
    assert mat.state == "terminated"
    assert not table_exists(backend, "jasmine_test", "incremental_demo_reload")

    # Verify early-termination.
    mat = refresh_mat(mat)
    do("verify")
    do("terminate")
    assert mat.state == "terminated"
    assert not table_exists(backend, "jasmine_test", "incremental_demo_reload")

    # Verify view collion handling.
    session.execute(
        text("CREATE VIEW `jasmine_test`.`incremental_demo_reload` AS SELECT 1;")
    )
    mat = refresh_mat(mat)
    do("verify")
    do("create")
    assert mat.state == "could_not_create"
    assert view_exists(backend, "jasmine_test", "incremental_demo_reload")

    do("terminate")
    assert mat.state == "terminated"
    assert view_exists(backend, "jasmine_test", "incremental_demo_reload")
    session.execute(text("DROP VIEW `jasmine_test`.`incremental_demo_reload`;"))

    # Verify table name collion handling.
    session.execute(
        text("CREATE TABLE `jasmine_test`.`incremental_demo_reload` (pk INT);")
    )
    mat = refresh_mat(mat)
    do("verify")
    do("create")
    assert mat.state == "could_not_create"
    assert table_exists(backend, "jasmine_test", "incremental_demo_reload")

    do("terminate")
    assert mat.state == "terminated"
    assert table_exists(backend, "jasmine_test", "incremental_demo_reload")
    session.execute(text("DROP TABLE `jasmine_test`.`incremental_demo_reload`;"))

    # Verify manual delete handling.
    mat = refresh_mat(mat)
    do("verify")
    do("create")
    session.execute(text("DROP TABLE `jasmine_test`.`incremental_demo_reload`;"))
    do("terminate")
    assert mat.state == "terminated"


def test_incremental_lifecycle():
    with prepopulated_worker_test_backend():

        # Hardcoded in test dump.
        with app_db_session(orm_registry) as session:
            walk_incremental_lifecycle(session, 51)


def walk_incremental_lifecycle(session, view_id: int):
    # Import late so mocking captures config.
    # TODO: Make this nicer with decent config setup.
    from jasmine.etl.worker_tasks import execute_materialization_event

    view = session.query(View).get(view_id)
    backend = view.project.backend
    mats = [
        mat
        for mat in view.materializations
        if mat.materialization_type == "incremental"
    ]
    mat = mats[0] if mats else None

    keys = {
        "event_id": ["event_id"],
        "path": ["path"],
        "description": ["description"],
        "title": ["title"],
        "title2": ["title", "description"],
    }
    column_names = [
        "event_id",
        "path",
        "method",
        "state",
        "config",
        "context",
        "title",
        "description",
        "updated_ts",
    ]

    def refresh_mat(preexisting_mat=None):
        config = {
            "keys": keys,
        }
        mat = new_materialization(
            view=view,
            mat_type_name="incremental",
            config=config,
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
            schedule_next_event=False,
        )

    if mat is not None and not mat.terminal():
        do("terminate")

    # Verify happy-path / basic flow.
    mat = refresh_mat(preexisting_mat=mat)
    assert mat.state == "proposed"

    do("verify")
    assert mat.state == "accepted"

    do("create")
    assert mat.state == "active"
    assert table_exists(backend, "jasmine_test", "incremental_demo_incremental")
    assert mat.context["last_updated"] is None

    direct_results = set(session.execute(text(view.spec["query_text"])).fetchall())

    # Adds rows to backend_events and changes state so do this a step later.
    do("update")
    assert mat.state == "active"
    assert mat.context["last_updated"] is not None
    assert (
        mat.context["last_updated"]
        >= (datetime.now() - timedelta(seconds=10)).timestamp()
    )

    incremental_results = set(
        session.execute(
            text(
                f"SELECT {escaped_column_list(column_names)} FROM `jasmine_test`.`incremental_demo_incremental`"
            )
        ).fetchall()
    )
    assert direct_results == incremental_results

    second_direct_results = set(
        session.execute(text(view.spec["query_text"])).fetchall()
    )
    do("update")
    second_incremental_results = set(
        session.execute(
            text(
                f"SELECT {escaped_column_list(column_names)} FROM `jasmine_test`.`incremental_demo_incremental`"
            )
        ).fetchall()
    )
    assert second_direct_results == second_incremental_results

    # Specific to backend_events.
    assert len(incremental_results) + 1 == len(second_incremental_results)

    do("terminate")
    assert mat.state == "terminated"
    assert not table_exists(backend, "jasmine_test", "incremental_demo_incremental")

    # Verify early-termination.
    mat = refresh_mat(mat)
    do("verify")
    do("terminate")
    assert mat.state == "terminated"
    assert not table_exists(backend, "jasmine_test", "incremental_demo_incremental")

    # Verify view collion handling.
    session.execute(
        text("CREATE VIEW `jasmine_test`.`incremental_demo_incremental` AS SELECT 1;")
    )
    mat = refresh_mat(mat)
    do("verify")
    do("create")
    assert mat.state == "could_not_create"
    assert view_exists(backend, "jasmine_test", "incremental_demo_incremental")

    do("terminate")
    assert mat.state == "terminated"
    assert view_exists(backend, "jasmine_test", "incremental_demo_incremental")
    session.execute(text("DROP VIEW `jasmine_test`.`incremental_demo_incremental`;"))

    # Verify table name collion handling.
    session.execute(
        text("CREATE TABLE `jasmine_test`.`incremental_demo_incremental` (pk INT);")
    )
    mat = refresh_mat(mat)
    do("verify")
    do("create")
    assert mat.state == "could_not_create"
    assert table_exists(backend, "jasmine_test", "incremental_demo_incremental")

    do("terminate")
    assert mat.state == "terminated"
    assert table_exists(backend, "jasmine_test", "incremental_demo_incremental")
    session.execute(text("DROP TABLE `jasmine_test`.`incremental_demo_incremental`;"))

    # Verify manual delete handling.
    mat = refresh_mat(mat)
    do("verify")
    do("create")
    session.execute(text("DROP TABLE `jasmine_test`.`incremental_demo_incremental`;"))
    do("terminate")
    assert mat.state == "terminated"
