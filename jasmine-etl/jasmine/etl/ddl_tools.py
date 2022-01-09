"""
ETLs create a series of tables, views, and triggers in a database.
This module has tools to:
- Verify there aren't any preexisting tables/triggers/views that'll interfere with creating the ETL.
- Verify an ETL was correctly instantiated in a database.
"""
from dataclasses import dataclass, field
from pprint import pformat

from sqlalchemy import text

from jasmine.etl.backends import (
    Backend,
    backend_engine,
    backend_table_spec,
    create_view_statement,
    table_exists,
    table_view_exists,
    trigger_exists_with_pattern,
    view_exists,
)
from jasmine.sql.table_spec import create_table_statement
from jasmine.sql.transforms.escaping import escaped_db_table


@dataclass
class ResourceNames:
    tables: set[tuple[str, str]] = field(default_factory=set)
    views: set[tuple[str, str]] = field(default_factory=set)
    triggers: set[tuple[str, str]] = field(default_factory=set)

    def to_dict(self):
        return {
            "tables": [list(table_name) for table_name in self.tables],
            "views": [list(view_name) for view_name in self.views],
            "triggers": [list(trigger_name) for trigger_name in self.triggers],
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            tables={tuple(table_name) for table_name in data.get("tables", [])},
            views={tuple(view_name) for view_name in data.get("views", [])},
            triggers={tuple(trigger_name) for trigger_name in data.get("triggers", [])},
        )

    @classmethod
    def from_materialization(cls, mat):
        return cls.from_dict(mat.context.get("claimed_resources", {}))

    def empty(self):
        return (len(self.tables) + len(self.views) + len(self.triggers)) == 0


def assert_names_available(backend: Backend, resource_names: ResourceNames) -> None:
    for db_name, table_name in resource_names.tables:
        pretty_name = escaped_db_table(db_name, table_name)
        assert (
            not len(db_name) > 64
        ), "Database name too long: {pretty_name} (max 64 characters.)"
        assert (
            not len(table_name) > 64
        ), "Table name too long: {pretty_name} (max 64 characters.)"

        assert not table_view_exists(
            backend, db_name, table_name
        ), f"Table/view already exists: {pretty_name}"

    for db_name, view_name in resource_names.views:
        pretty_name = escaped_db_table(db_name, view_name)
        assert (
            not len(db_name) > 64
        ), "Database name too long: {pretty_name} (max 64 characters.)"
        assert (
            not len(view_name) > 64
        ), "View name too long: {pretty_name} (max 64 characters.)"

        assert not table_view_exists(
            backend, db_name, view_name
        ), f"Table/view already exists: {escaped_db_table(db_name, view_name)}"

    for db_name, trigger_name in resource_names.triggers:
        pretty_name = escaped_db_table(db_name, trigger_name)
        assert (
            not len(db_name) > 64
        ), "Database name too long: {pretty_name} (max 64 characters.)"
        assert (
            not len(trigger_name) > 64
        ), "Trigger name too long: {pretty_name} (max 64 characters.)"

        assert not trigger_exists_with_pattern(
            backend, db_name, trigger_name
        ), f"Trigger already exists: {escaped_db_table(db_name, trigger_name)}"


def names_available(backend: Backend, resource_names: ResourceNames) -> bool:
    try:
        assert_names_available(backend, resource_names)
    except AssertionError:
        return False
    return True


def assert_names_successfully_taken(
    backend: Backend, resource_names: ResourceNames
) -> None:
    for db_name, table_name in resource_names.tables:
        assert table_exists(
            backend, db_name, table_name
        ), f"Failed to create table: {escaped_db_table(db_name, table_name)}"

    for db_name, view_name in resource_names.views:
        assert view_exists(
            backend, db_name, view_name
        ), f"Failed to create view: {escaped_db_table(db_name, view_name)}"

    for db_name, trigger_name in resource_names.triggers:
        assert trigger_exists_with_pattern(
            backend, db_name, trigger_name
        ), f"Failed to create trigger: {escaped_db_table(db_name, trigger_name)}"


def names_successfully_taken(backend: Backend, resource_names: ResourceNames) -> bool:
    try:
        assert_names_successfully_taken(backend, resource_names)
    except AssertionError:
        return False
    return True


def view_status_str(backend: Backend, db_name: str, view_name: str) -> str:
    if table_exists(backend, db_name, view_name):
        return (
            f"Table {escaped_db_table(db_name, view_name)} exists; was expecting a view.\n"
            + table_status_str(backend, db_name, view_name)
        )

    if not view_exists(backend, db_name, view_name):
        return f"View {escaped_db_table(db_name, view_name)} does not exist."

    view_statement = create_view_statement(backend, db_name, view_name)
    try:
        with backend_engine(backend).connect() as conn:
            sample_rows = conn.execute(
                text(f"SELECT * FROM {escaped_db_table(db_name, view_name)} LIMIT 5;")
            ).fetchall()
    except Exception as e:
        sample_rows = None

    return "\n".join(
        [
            view_statement,
            "Sample rows:",
            pformat(sample_rows),
        ]
    )


def table_status_str(backend: Backend, db_name: str, table_name: str) -> str:
    if view_exists(backend, db_name, table_name):
        return (
            f"View {escaped_db_table(db_name, table_name)} exists; was expecting a table.\n"
            + view_status_str(backend, db_name, table_name)
        )

    if not table_exists(backend, db_name, table_name):
        return f"Table {escaped_db_table(db_name, table_name)} does not exist."

    table_spec = backend_table_spec(backend, db_name, table_name)
    table_statement = create_table_statement(db_name, table_name, table_spec)
    try:
        with backend_engine(backend).connect() as conn:
            sample_rows = conn.execute(
                text(f"SELECT * FROM {escaped_db_table(db_name, table_name)} LIMIT 5;")
            ).fetchall()
    except Exception as e:
        sample_rows = None

    return "\n".join(
        [
            table_statement,
            "Sample rows:",
            pformat(sample_rows),
        ]
    )


def trigger_status_str(backend: Backend, db_name: str, trigger_name: str) -> str:
    if not trigger_exists_with_pattern(backend, db_name, trigger_name):
        return f"Trigger {escaped_db_table(db_name, trigger_name)} does not exist."

    with backend_engine(backend).connect() as conn:
        (create_trigger_statement,) = conn.execute(
            text(f"SHOW CREATE TRIGGER {escaped_db_table(db_name, trigger_name)};")
        ).fetchone()
        return create_trigger_statement


def names_status_str(backend: Backend, resource_names: ResourceNames) -> str:
    """
    Summarize the status of a group of resource names.
    Useful for debugging materialization / ETLs across multiple steps.

    This shows whether each exist, prints out the CREATE TABLE / CREATE VIEW statements, and
    shows sample data if available.

    >>> from jasmine.etl.ddl_tools import ResourceNames, names_status_str
    >>> from jasmine.etl.backends import example_create_sqlite_schema_statements, tmp_mock_sqla_backend
    >>> from pprint import pprint

    >>> resource_names = ResourceNames(
    ...     tables=[("main", 'bleh " ')],
    ...     views=[("main", 'users " ')],
    ...     triggers=[],  # sqlite doesn't currently support triggers.
    ... )
    >>> create_view_statement = 'CREATE VIEW `bleh " ` AS SELECT 1;'
    >>> with tmp_mock_sqla_backend(example_create_sqlite_schema_statements + [create_view_statement]) as backend:
    ...     print(names_status_str(backend, resource_names))
    Table `main`.`users " ` exists; was expecting a view.
    CREATE TABLE `main`.`users " ` (
        `user_id` INTEGER NOT NULL,
        `name` VARCHAR(96) NOT NULL,
        `parent_user_id` BIGINT,
        PRIMARY KEY (`user_id`),
        UNIQUE unique_key_0 (`name`),
        UNIQUE unique_key_1 (`parent_user_id`),
        KEY org_name (`parent_user_id`, `name`),
        CONSTRAINT FOREIGN KEY (`parent_user_id`) REFERENCES `main`.`users \\" ` (`user_id`)
    );
    <BLANKLINE>
    View `main`.`bleh " ` exists; was expecting a table.
    CREATE VIEW `bleh " ` AS SELECT 1
    """
    status_parts = []

    for db_name, view_name in resource_names.views:
        status_parts.append(view_status_str(backend, db_name, view_name))

    for db_name, table_name in resource_names.tables:
        status_parts.append(table_status_str(backend, db_name, table_name))

    for db_name, trigger_name in resource_names.triggers:
        status_parts.append(trigger_status_str(backend, db_name, trigger_name))

    return "\n\n".join(status_parts)
