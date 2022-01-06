"""
ETLs create a series of tables, views, and triggers in a database.
This module has tools to:
- Verify there aren't any preexisting tables/triggers/views that'll interfere with creating the ETL.
- Verify an ETL was correctly instantiated in a database.
"""
from dataclasses import dataclass, field

from jasmine.etl.backends import (
    Backend,
    table_exists,
    table_view_exists,
    trigger_exists_with_pattern,
    view_exists,
)
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
