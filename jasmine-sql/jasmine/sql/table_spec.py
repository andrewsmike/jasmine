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
- Handle prefix-only indexing of TEXT blobs (IE, `KEY (my_text_column(255), ...)`)
"""
from dataclasses import dataclass, field, replace
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
    sqla_type = column_info["type"]
    if str(sqla_type) == "ENUM":
        attrs = [repr(sqla_type)]
    else:
        attrs = [str(sqla_type)]

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

    def __post_init__(self):
        assert len(self.source_columns) == len(
            self.dest_columns
        ), "Foreign keys must have the same number of source and target columns."

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


def key_redundant(
    keys: dict[str, list[str]], key: list[str], unique: bool = False
) -> bool:
    if unique:
        # Unique key is redundant; a __less__ precise key already exists. Add as regular index.
        return any(
            (len(key) >= len(existing_key) and key[: len(existing_key)] == existing_key)
            for existing_key in keys.values()
        )
    else:
        # Key is redundant; a __more__ precise key already exists. Don't add.
        return any(
            (len(key) <= len(existing_key) and existing_key[: len(key)] == key)
            for existing_key in keys.values()
        )


def next_indexed_name(names: set[str], base: str, index: int = 0):
    """
    >>> next_indexed_name({"key_1", "key_2", "key_3", "key_6"}, "key")
    'key_4'
    """
    for i in range(1_000_000):
        name = f"{base}_{i+1}"
        if name not in names:
            index -= 1
        if index < 0:
            return name
    else:
        raise RuntimeError(f"Couldn't find a unique name. Tried 1mil. Base: {base}.")


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

    column_names: list[str] = field(default_factory=list)
    column_type_decls: dict[str, str] = field(default_factory=dict)

    primary_key: list[str] = field(default_factory=list)
    indices: dict[str, list[str]] = field(default_factory=dict)
    unique_indices: dict[str, list[str]] = field(default_factory=dict)

    foreign_keys: list[ForeignKey] = field(default_factory=list)

    def __post_init__(self):
        """
        Validate everything.

        Note: Does not validate everything, IE name length > accepted by database.

        >>> from pprint import pprint

        Example correct usage:
        >>> pprint(TableSpec(column_names=["a", "b"], column_type_decls={"a": "int", "b": "int"}, primary_key=["a"]))
        TableSpec(column_names=['a', 'b'],
                  column_type_decls={'a': 'int', 'b': 'int'},
                  primary_key=['a'],
                  indices={},
                  unique_indices={},
                  foreign_keys=[])

        Various errors:
        >>> TableSpec(column_names=[])
        Traceback (most recent call last):
          ...
        AssertionError: Table spec must have at least one column...

        You must remember to type your columns:
        >>> TableSpec(column_names=["a"])
        Traceback (most recent call last):
          ...
        AssertionError: Column(s) not provided with a type declaration: {'a'}...


        >>> TableSpec(column_names=["a"], column_type_decls={"a": "int"}, primary_key=["b"])
        Traceback (most recent call last):
          ...
        AssertionError: Key ['b'] asking for unknown column(s) {'b'}...

        >>> TableSpec(column_names=["a"], column_type_decls={"a": "int"}, unique_indices={"blah": ["a", "b"]})
        Traceback (most recent call last):
          ...
        AssertionError: Key ['a', 'b'] asking for unknown column(s) {'b'}...
        """
        assert len(self.column_names) >= 1, "Table spec must have at least one column."

        assert not any(
            ("{" in column_name) or ("}" in column_name)
            for column_name in self.column_names
        ), (
            "Curly brackets in column names not supported. Columns: {self.column_names}\n"
            + "(Hint: Add an alias using 'AS column_name'.)"
        )

        untyped_columns = set(self.column_names) - set(self.column_type_decls.keys())
        assert (
            not untyped_columns
        ), f"Column(s) not provided with a type declaration: {untyped_columns}"

        assert not (
            set(self.unique_indices.keys()) & set(self.indices.keys())
        ), "Key and unique key have identical name."

        keys = (
            [self.primary_key]
            + list(self.unique_indices.values())
            + list(self.indices.values())
            + list(foreign_key.source_columns for foreign_key in self.foreign_keys)
        )
        for key in keys:
            unknown_columns = set(key) - set(self.column_names)
            assert (
                not unknown_columns
            ), f"Key {key} asking for unknown column(s) {unknown_columns}"

    @classmethod
    def from_sqla_inspector(cls, inspector, db_name: str | None, table_name: str):
        db_name = unescaped(db_name) if db_name is not None else None
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
        index_names = {
            index_info["name"] for index_info in index_infos if index_info["name"]
        }
        indices = {
            index_info["name"]
            or next_indexed_name(index_names, "key", index_index): index_info[
                "column_names"
            ]
            for index_index, index_info in enumerate(index_infos)
            if not index_info["unique"]
        }

        unique_index_infos = inspector.get_unique_constraints(
            table_name, schema=db_name
        )
        unique_index_names = {
            unique_index_info["name"]
            for unique_index_info in unique_index_infos
            if unique_index_info["name"]
        }
        unique_indices = {
            unique_index_info["name"]
            or next_indexed_name(
                unique_index_names, "unique_key", unique_index_index
            ): unique_index_info["column_names"]
            for unique_index_index, unique_index_info in enumerate(unique_index_infos)
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

    @property
    def all_unique_indices(self) -> dict[str, list[str]]:
        if self.primary_key:
            return {
                next_indexed_name(
                    set(self.unique_indices.keys()), "primary_key"
                ): self.primary_key,
                **self.unique_indices,
            }
        else:
            return self.unique_indices

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
            tuple(unescaped(column) for column in index)
            for index in self.all_unique_indices.values()
        }

        minimal_indices = {
            index
            for index in distinct_indices
            if not any(
                (len(index) < len(bigger_index) and index == bigger_index[: len(index)])
                for bigger_index in distinct_indices
            )
            if not any(
                (
                    len(index) <= len(encapsulating_unique_index)
                    and index == encapsulating_unique_index[: len(index)]
                )
                for encapsulating_unique_index in unique_indices
            )
        }
        return replace(
            self,
            indices={
                f"_jsmn_key_{key_index}": list(key_columns)
                for key_index, key_columns in enumerate(sorted(minimal_indices))
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

    def with_key(
        self, key: list[str], key_name: str | None = None, unique: bool = False
    ):
        """
        Add a new key while avoiding collisions.
        If key is a strict prefix to an existing key

        >>> from jasmine.sql.table_spec import example_table_spec
        >>> from pprint import pprint

        >>> pprint(example_table_spec.with_key(["name"]))
        TableSpec(column_names=['user_id', 'name', 'parent_user_id'],
                  ...
                  indices={'key_1': ['name'], 'org_name': ['parent_user_id', 'name']},
                  ...)

        Don't add unnecessary keys:
        >>> pprint(example_table_spec.with_key(["user_id"], unique=True))
        TableSpec(...
                  unique_indices={'unique_key_0': ['name'],
                                  'unique_key_1': ['parent_user_id']},
                  ...)
        """
        if unique and key_redundant(self.all_unique_indices, key, unique=True):
            return self.with_key(key, key_name=key_name, unique=False)

        if (not unique) and key_redundant(self.indices, key, unique=False):
            return self

        if key_name is None:
            if unique:
                key_name = next_indexed_name(
                    set(self.unique_indices.keys()), base="unique_key"
                )
            else:
                key_name = next_indexed_name(set(self.indices.keys()), base="key")

        assert key_name is not None  # For MyPy.

        if unique:

            return replace(
                self,
                unique_indices={key_name: key, **self.unique_indices},
            )
        else:

            return replace(
                self,
                indices={key_name: key, **self.indices},
            )

    def with_auto_id(
        self, prefix: str | None = None, bigint: bool = True
    ) -> "TableSpec":
        """
        Replace the current primary key with an auto_id PK and a unique key.

        >>> from jasmine.sql.table_spec import example_table_spec
        >>> from pprint import pprint

        >>> pprint(example_table_spec.with_auto_id(prefix="jsmn", bigint=True))
        TableSpec(column_names=['jsmn_auto_id', 'user_id', 'name', 'parent_user_id'],
                  column_type_decls={'jsmn_auto_id': 'BIGINT NOT NULL AUTO_INCREMENT',
                                     'name': 'VARCHAR(96) NOT NULL',
                                     'parent_user_id': 'BIGINT',
                                     'user_id': 'INTEGER NOT NULL'},
                  primary_key=['jsmn_auto_id'],
                  indices={'org_name': ['parent_user_id', 'name']},
                  unique_indices={'jsmn_prev_primary_key': ['user_id'],
                                  ...)
        """
        if prefix is not None:
            auto_id_column_name = f"{prefix}_auto_id"
        else:
            auto_id_column_name = "auto_id"

        if bigint:
            int_type_str = "BIGINT"
        else:
            int_type_str = "INT"

        assert "jsmn_prev_primary_key" not in self.unique_indices
        assert (
            auto_id_column_name not in self.column_names
        ), f"Table already has an identically named auto_id: {auto_id_column_name}."

        primary_key_index = (
            {"jsmn_prev_primary_key": self.primary_key} if self.primary_key else {}
        )

        return replace(
            self,
            column_names=[auto_id_column_name] + self.column_names,
            column_type_decls={
                auto_id_column_name: f"{int_type_str} NOT NULL AUTO_INCREMENT",
                **self.column_type_decls,
            },
            primary_key=[auto_id_column_name],
            unique_indices={**primary_key_index, **self.unique_indices},
        )

    def pk_table(self) -> "TableSpec":
        """
        >>> from jasmine.sql.table_spec import example_table_spec
        >>> from pprint import pprint

        >>> pprint(example_table_spec.pk_table())
        TableSpec(column_names=['user_id'],
                  column_type_decls={'user_id': 'INTEGER NOT NULL'},
                  primary_key=['user_id'],
                  indices={},
                  unique_indices={},
                  foreign_keys=[])
        """
        return TableSpec(
            column_names=self.primary_key,
            column_type_decls={
                column_name: column_type_decl
                for column_name, column_type_decl in self.column_type_decls.items()
                if column_name in self.primary_key
            },
            primary_key=self.primary_key,
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
    base_table_name: str | None,
    base_table_spec: TableSpec,
    suffix: str | None = None,
    real_table: bool = False,
) -> tuple[str, str]:
    """
    Create an appropriate staging table:
    - Drop foreign keys, as their semantic guarantees aren't required and they can junk up the
        ETL patterns.
    - Replace foreign keys with alternatives, so all reverse-lookups stay performant.
    - Allow suffix for easy debugging, but randomize random table name.
        TODO: Cache randomly generated table names during session to avoid collisions.
    - Drop any defaults / generated columns / whatnot.

    Note: The kwarg `real_table=True` can force this method to create a real table.
        This is sometimes necessary, as MySQL doesn't allow temp tables to be reused within a
        query, and this can be _incredibly_ problematic. Be aware that may flush your commit, and you
        must drop it using drop_table_statement(..., temporary=False).

    TODO: Preserve coalation and charset.

    Example:
    >>> from jasmine.sql.table_spec import example_table_spec
    >>> from random import seed

    >>> seed(1337)
    >>> temp_table_name, create_temp_table = create_staging_table_statement("main", 'users " ', example_table_spec, suffix="new")
    >>> temp_table_name
    '_users " _new_MHwKkZ'
    >>> print(create_temp_table)
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
        suffix = ""
    else:
        suffix = f"_{suffix}"

    assert suffix is not None  # For MyPy.

    if base_table_name is None:
        base_table_name = "unnamed_table"

    assert base_table_name is not None  # For MyPy.

    random_suffix = "".join(choices(ascii_letters + digits, k=6))
    if real_table:
        randomized_name = f"_jsmn_tmp_{base_table_name}{suffix}_{random_suffix}"
    else:
        randomized_name = f"_{base_table_name}{suffix}_{random_suffix}"

    return randomized_name, create_table_statement(
        base_db_name,
        randomized_name,
        base_table_spec.without_constraints(keep_unique_keys=True),
        temporary=not real_table,
    )


def drop_table_statement(
    db_name: str | None,
    table_name: str,
    idempotent: bool = True,
    temporary: bool = False,
) -> str:
    """
    >>> print(drop_table_statement("main", 'users " '))
    DROP TABLE IF EXISTS `main`.`users " `;

    >>> print(drop_table_statement(None, 'users " '))
    DROP TABLE IF EXISTS `users " `;

    >>> print(drop_table_statement("main", 'users " ', idempotent=False))
    DROP TABLE `main`.`users " `;

    >>> print(drop_table_statement("main", 'users " ', idempotent=False))
    DROP TABLE `main`.`users " `;

    >>> print(drop_table_statement("main", 'users " ', idempotent=True, temporary=True))
    DROP TEMPORARY TABLE IF EXISTS `main`.`users " `;
    """
    idempotent_str = "IF EXISTS " if idempotent else ""
    temp_str = "TEMPORARY " if temporary else ""
    return (
        f"DROP {temp_str}TABLE {idempotent_str}{escaped_db_table(db_name, table_name)};"
    )
