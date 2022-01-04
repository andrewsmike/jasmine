"""
Extract and represent table schema, generate CREATE TABLE logic.

Does _not_currently handle auto_increment, as not all backends provide that data.

May simplify/muddle key names due to dialect weirdness, does not currently preserve coalation / charset / etc.
TODO:
- Coalation, charset
- Preserve auto_inc if available
- Rigorously test to identify missing / weak points
- Handle SQLite keys
        # mysql_collate="utf8mb4_0900_ai_ci",
        # mysql_default_charset="utf8mb4",
        # mysql_engine="InnoDB",
"""
from dataclasses import dataclass, replace
from random import choices
from string import ascii_letters, digits
from typing import Any

from dataclasses_json import dataclass_json

from jasmine.sql.transforms.escaping import (
    escaped,
    escaped_column_list,
    escaped_db_table,
    unescaped,
)


def column_type_decl(
    column_info: dict[str, Any],
    ignore_defaults: bool = True,
    ignore_autoinc: bool = True,
) -> str:
    attrs = [str(column_info["type"])]

    if not column_info["nullable"]:
        attrs.append("NOT NULL")

    if not ignore_autoinc and column_info["autoincrement"] == "auto":
        attrs.append("AUTO_INCREMENT")

    if not ignore_defaults and column_info["default"] is not None:
        assert False, "Untested escaping logic."
        attrs.append(f"DEFAULT {column_info['default']}")

    return " ".join(attrs)


@dataclass
class ForeignKey:
    name: str | None
    dest_db_name: str
    dest_table_name: str

    source_columns: list[str]
    dest_columns: list[str]

    @classmethod
    def from_info(cls, foreign_key_info):
        return cls(
            **{
                target_name: foreign_key_info[source_name]
                for target_name, source_name in {
                    "name": "name",
                    "dest_db_name": "referred_schema",
                    "dest_table_name": "referred_table",
                    "source_columns": "constrained_columns",
                    "dest_columns": "referred_columns",
                }.items()
            }
        )

    def constraint_spec_str(self) -> str:
        name_str = f"{escaped(self.name)} " if self.name is not None else ""
        return (
            f"CONSTRAINT {name_str}FOREIGN KEY"
            + f" ({escaped_column_list(self.source_columns)})"
            + f" REFERENCES {escaped(self.dest_db_name)}.{escaped(self.dest_table_name)}"
            + f" ({escaped_column_list(self.dest_columns)})"
        )


# Recursive to_json, from_json methods.
@dataclass_json
@dataclass
class TableSpec:
    """
    Table specification.

    Does _not_ cover:
    - AUTO_INCREMENT
    - Comments
    - Anything you don't see in the below list.

    More tests can be found in in the `jasmine.etl.backends` module.

    Serialization:
    >>> from json import loads
    >>> from pprint import pprint

    >>> pprint(loads(example_table_spec.to_json()))
    {'column_names': ['user_id', 'name', 'parent_user_id'],
     'column_type_decls': {'name': 'VARCHAR(96) NOT NULL',
                           'parent_user_id': 'BIGINT',
                           'user_id': 'INTEGER NOT NULL'},
     'foreign_keys': [{'dest_columns': ['user_id'],
                       'dest_db_name': 'main',
                       'dest_table_name': 'users " ',
                       'name': None,
                       'source_columns': ['parent_user_id']}],
     'indices': {'org_name': ['parent_user_id', 'name']},
     'primary_key': ['user_id'],
     'unique_indices': {'unique_key_0': ['name'],
                        'unique_key_1': ['parent_user_id']}}

    >>> example_table_spec == TableSpec.from_json(example_table_spec.to_json())
    True
    """

    column_names: list[str]
    column_type_decls: dict[str, str]

    primary_key: list[str]
    indices: dict[str, list[str]]
    unique_indices: dict[str, list[str]]

    foreign_keys: list[ForeignKey]

    @classmethod
    def from_sqla_inspector(cls, inspector, db_name: str, table_name: str):
        db_name = unescaped(db_name)
        table_name = unescaped(table_name)

        column_infos = inspector.get_columns(table_name, schema=db_name)
        column_names = [column_info["name"] for column_info in column_infos]
        column_type_decls = {
            column_info["name"]: column_type_decl(column_info)
            for column_info in column_infos
        }

        primary_key = inspector.get_pk_constraint(table_name, schema=db_name)[
            "constrained_columns"
        ]

        index_infos = inspector.get_indexes(table_name, schema=db_name)
        assert not any(index_info["unique"] for index_info in index_infos)
        indices = {
            index_info["name"]: index_info["column_names"] for index_info in index_infos
        }

        unique_index_infos = inspector.get_unique_constraints(
            table_name, schema=db_name
        )
        unique_indices = {
            key_info["name"]
            or f"unique_key_{unique_key_index}": key_info["column_names"]
            for unique_key_index, key_info in enumerate(unique_index_infos)
        }

        foreign_keys = [
            ForeignKey.from_info(fk_info)
            for fk_info in inspector.get_foreign_keys(table_name, schema=db_name)
        ]

        return cls(
            column_names=column_names,
            column_type_decls=column_type_decls,
            primary_key=primary_key,
            indices=indices,
            unique_indices=unique_indices,
            foreign_keys=foreign_keys,
        )

    def with_deduped_indices(self) -> "TableSpec":
        """
        The equivalent table with redundant indices dropped and all indices renamed consistently.

        >>> from jasmine.sql.table_spec import example_table_spec
        >>> from pprint import pprint

        By default, key names are pretty inconsistent, and duplicate keys tend to crop up:
        >>> pprint(example_table_spec.without_constraints())
        TableSpec(...
                  indices={'_jsmn_fk_0': ['parent_user_id'],
                           '_jsmn_uniq_0': ['name'],
                           '_jsmn_uniq_1': ['parent_user_id'],
                           'org_name': ['parent_user_id', 'name']},
                  ...)

        Here we resolve this thoroughly:
        >>> pprint(example_table_spec.without_constraints().with_deduped_indices())
        TableSpec(...
                  indices={'_jsmn_key_0': ['name'],
                           '_jsmn_key_1': ['parent_user_id', 'name']},
                  ...)
        """
        distinct_indices = {
            tuple(unescaped(column) for column in index)
            for index in self.indices.values()
        }
        unique_indices = {
            index
            for index in distinct_indices
            if not any(
                (len(index) < len(bigger_index) and index == bigger_index[: len(index)])
                for bigger_index in distinct_indices
            )
        }
        return replace(
            self,
            indices={
                f"_jsmn_key_{key_index}": list(key_columns)
                for key_index, key_columns in enumerate(sorted(unique_indices))
            },
        )

    def without_constraints(
        self, keep_unique_keys: bool = False, keep_foreign_keys: bool = False
    ) -> "TableSpec":
        """
        The equivalent table spec with no constraints (unique or foreign keys) but the corresponding indices.
        Used in generating derived tables (history tables, temporary tables, etc) for which existing unique or
        foreign keys are not appropriate.

        >>> from jasmine.sql.table_spec import example_table_spec
        >>> from pprint import pprint

        >>> pprint(example_table_spec.without_constraints(keep_foreign_keys=True, keep_unique_keys=True))
        TableSpec(column_names=['user_id', 'name', 'parent_user_id'],
        ...
                  indices={'org_name': ['parent_user_id', 'name']},
                  unique_indices={'unique_key_0': ['name'],
                                  'unique_key_1': ['parent_user_id']},
                  foreign_keys=[ForeignKey(name=None,
                                           dest_db_name='main',
                                           dest_table_name='users " ',
                                           source_columns=['parent_user_id'],
                                           dest_columns=['user_id'])])

        >>> pprint(example_table_spec.without_constraints(keep_unique_keys=True))
        TableSpec(column_names=['user_id', 'name', 'parent_user_id'],
        ...
                  indices={'_jsmn_fk_0': ['parent_user_id'],
                           'org_name': ['parent_user_id', 'name']},
                  unique_indices={'unique_key_0': ['name'],
                                  'unique_key_1': ['parent_user_id']},
                  foreign_keys=[])


        >>> pprint(example_table_spec.without_constraints())
        TableSpec(column_names=['user_id', 'name', 'parent_user_id'],
        ...
                  indices={'_jsmn_fk_0': ['parent_user_id'],
                           '_jsmn_uniq_0': ['name'],
                           '_jsmn_uniq_1': ['parent_user_id'],
                           'org_name': ['parent_user_id', 'name']},
                  unique_indices={},
                  foreign_keys=[])

        >>> pprint(example_table_spec.without_constraints(keep_foreign_keys=True))
        TableSpec(column_names=['user_id', 'name', 'parent_user_id'],
        ...
                  indices={'_jsmn_uniq_0': ['name'],
                           '_jsmn_uniq_1': ['parent_user_id'],
                           'org_name': ['parent_user_id', 'name']},
                  unique_indices={},
                  foreign_keys=[ForeignKey(name=None,
                                           dest_db_name='main',
                                           dest_table_name='users " ',
                                           source_columns=['parent_user_id'],
                                           dest_columns=['user_id'])])
        """
        new_indices = {}
        if keep_foreign_keys:
            foreign_keys = self.foreign_keys
        else:
            foreign_keys = []
            new_indices.update(
                {
                    f"_jsmn_fk_{fk_index}": foreign_key.source_columns
                    for fk_index, foreign_key in enumerate(self.foreign_keys)
                }
            )

        if keep_unique_keys:
            unique_indices = self.unique_indices
        else:
            unique_indices = {}
            new_indices.update(
                {
                    f"_jsmn_uniq_{unique_key_index}": key_parts
                    for unique_key_index, (key_name, key_parts) in enumerate(
                        sorted(self.unique_indices.items())
                    )
                }
            )

        preexisting_keys = set(new_indices.keys()) & set(self.indices.keys())
        assert (
            not preexisting_keys
        ), f"Table already has keys in the _jsmn namespace, cannot inject new keys. Keys: {preexisting_keys}"

        return replace(
            self,
            unique_indices=unique_indices,
            foreign_keys=foreign_keys,
            indices={
                **self.indices,
                **new_indices,
            },
        )


example_table_spec = TableSpec(
    column_names=["user_id", "name", "parent_user_id"],
    column_type_decls={
        "name": "VARCHAR(96) NOT NULL",
        "parent_user_id": "BIGINT",
        "user_id": "INTEGER NOT NULL",
    },
    primary_key=["user_id"],
    indices={"org_name": ["parent_user_id", "name"]},
    unique_indices={
        "unique_key_0": ["name"],
        "unique_key_1": ["parent_user_id"],
    },
    foreign_keys=[
        ForeignKey(
            name=None,
            dest_db_name="main",
            dest_table_name='users " ',
            source_columns=["parent_user_id"],
            dest_columns=["user_id"],
        ),
    ],
)


def create_table_statement(
    db_name: str,
    table_name: str,
    table_spec: TableSpec,
    temporary: bool = False,
    if_not_exists: bool = False,
) -> str:
    """
    from jasmine.sql.table_spec import example_table_spec

    >>> print(create_table_statement("main", 'users " ', example_table_spec, temporary=True, if_not_exists=True))
    CREATE TEMPORARY TABLE IF NOT EXISTS `main`.`users " ` (
        `user_id` INTEGER NOT NULL,
        `name` VARCHAR(96) NOT NULL,
        `parent_user_id` BIGINT,
        PRIMARY KEY (`user_id`),
        UNIQUE unique_key_0 (`name`),
        UNIQUE unique_key_1 (`parent_user_id`),
        KEY org_name (`parent_user_id`, `name`),
        CONSTRAINT FOREIGN KEY (`parent_user_id`) REFERENCES `main`.`users " ` (`user_id`)
    );
    """
    table_type_str = "TEMPORARY TABLE" if temporary else "TABLE"
    temporary_str = "TEMPORARY " if temporary else ""
    if_not_exists_str = "IF NOT EXISTS " if if_not_exists else ""
    header_str = f"CREATE {table_type_str} {if_not_exists_str}{escaped(db_name)}.{escaped(table_name)} ("

    column_type_specs = [
        f"{escaped(column_name)} {table_spec.column_type_decls[column_name]}"
        for column_name in table_spec.column_names
    ]

    primary_key_spec = []
    if table_spec.primary_key:
        primary_key_spec = [
            f"PRIMARY KEY ({escaped_column_list(table_spec.primary_key)})"
        ]

    # SQLite doesn't allow "UNIQUE KEY", only "UNIQUE". MySQL supports this, so :shrug:
    unique_key_specs = [
        f"UNIQUE {unique_key_name} ({escaped_column_list(unique_key_columns)})"
        for unique_key_name, unique_key_columns in table_spec.unique_indices.items()
    ]

    # TODO: SQLite requires these to be separate
    index_specs = [
        f"KEY {key_name} ({escaped_column_list(key_columns)})"
        for key_name, key_columns in table_spec.indices.items()
    ]

    fk_specs = [
        foreign_key.constraint_spec_str() for foreign_key in table_spec.foreign_keys
    ]

    body_parts = (
        column_type_specs + primary_key_spec + unique_key_specs + index_specs + fk_specs
    )
    body_str = ",\n    ".join(body_parts)
    footer_str = ");"

    return "\n".join([header_str, "    " + body_str, footer_str])


def create_staging_table_statement(
    base_db_name: str,
    base_table_name: str,
    base_table_spec: TableSpec,
    suffix: str | None = None,
) -> str:
    """
    Create an appropriate staging table:
    - Drop foreign keys, as their semantic guarantees aren't required and they can junk up the ETL patterns.
    - Replace foreign keys with alternatives, so all reverse-lookups stay performant.
    - Allow suffix for easy debugging, but randomize random table name.
        TODO: Cache randomly generated table names during session to avoid collisions.
    - Drop any defaults / generated columns / whatnot.

    TODO: Preserve coalation and charset.

    Example:
    >>> from jasmine.sql.table_spec import example_table_spec
    >>> from random import seed

    >>> seed(1337)
    >>> print(create_staging_table_statement("main", 'users " ', example_table_spec, suffix="new"))
    CREATE TEMPORARY TABLE `main`.`_users " _new_MHwKkZ` (
        `user_id` INTEGER NOT NULL,
        `name` VARCHAR(96) NOT NULL,
        `parent_user_id` BIGINT,
        PRIMARY KEY (`user_id`),
        UNIQUE unique_key_0 (`name`),
        UNIQUE unique_key_1 (`parent_user_id`),
        KEY org_name (`parent_user_id`, `name`),
        KEY _jsmn_fk_0 (`parent_user_id`)
    );
    """
    if suffix is None:
        suffix = "tmp"

    random_suffix = "".join(choices(ascii_letters + digits, k=6))
    randomized_name = f"_{base_table_name}_{suffix}_{random_suffix}"

    return create_table_statement(
        base_db_name,
        randomized_name,
        base_table_spec.without_constraints(keep_unique_keys=True),
        temporary=True,
    )


def drop_table_statement(
    db_name: str,
    table_name: str,
    idempotent: bool = True,
) -> str:
    """
    >>> print(drop_table_statement("main", 'users " '))
    DROP TABLE IF EXISTS `main`.`users " `;

    >>> print(drop_table_statement("main", 'users " ', idempotent=False))
    DROP TABLE `main`.`users " `;
    """
    idempotent_str = "IF EXISTS " if idempotent else ""
    return f"DROP TABLE {idempotent_str}{escaped_db_table(db_name, table_name)};"
