"""
Initialize flask, config, database connections, auth, graphql, etc.
"""
from configparser import ConfigParser
from functools import cache
from os import getenv
from os.path import expanduser
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker


@cache
def app_config() -> ConfigParser:
    possible_config_file_paths = [
        getenv("JASMINE_WEBSERVER_CONFIG", None),
        "jasmine_webserver.cfg",
        "~/.jasmine_webserver.cfg",
    ]
    config_file_paths: list[str] = [
        expanduser(path) for path in possible_config_file_paths if path
    ]

    config_parser = ConfigParser()
    config_parser.read(config_file_paths)

    return config_parser


def sqla_uri_from_config_section(config_section) -> str:
    """
    >>> from jasmine.webserver.app_base import sqla_uri_from_config_section
    >>> sqla_uri_from_config_section({
    ...     "uri": "mysq://blah:blah@blah/{username}={user}, {password}={pass}, {database}={db}",
    ...     "username": "username",
    ...     "password": "password",
    ...     "host": "localhost",
    ...     "database": "db",
    ... })
    'mysq://blah:blah@blah/username=username, password=password, db=db'
    >>> sqla_uri_from_config_section({
    ...     "username": "my_app_prod_ro",
    ...     "password": "my_ap_prod_ro_pass",
    ...     "host": "db_endpoint",
    ...     "database": "database",
    ... })
    'mysql+pymysql://my_app_prod_ro:my_ap_prod_ro_pass@db_endpoint:3306/database'
    """
    uri = config_section.get(
        "uri", "mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
    )
    username = config_section.get("username", "")
    password = config_section.get("password", "")
    host = config_section.get("host", "")
    port = config_section.get("port", "3306")
    database = config_section.get("database", "")

    return uri.format(
        **{
            "username": username,
            "user": username,
            "password": password,
            "pass": password,
            "host": host,
            "port": port,
            "database": database,
            "db": database,
        }
    )


@cache
def app_db_engine_session_maker(orm_registry) -> tuple[Engine, Any]:
    config = app_config()
    assert "database" in config, "No backend [database] configured. Add to config file."
    sqla_uri = sqla_uri_from_config_section(config["database"])

    engine = create_engine(sqla_uri, echo=False)

    orm_registry.metadata.bind = engine

    return (
        engine,
        scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=engine,
            )
        ),
    )


def app_db_engine_session(orm_registry) -> tuple[Engine, Session]:
    engine, session_maker = app_db_engine_session_maker(orm_registry)
    return (engine, session_maker())
