"""
Initialize celery, config, database connections, auth, redis, etc.
"""
from configparser import ConfigParser
from contextlib import contextmanager
from functools import cache
from os import getenv
from os.path import expanduser
from typing import Any, Optional

from celery import Celery
from pottery import Redlock
from pottery.exceptions import ReleaseUnlockedLock
from redis import Redis
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker


@cache
def app_config() -> ConfigParser:
    possible_config_file_paths = [
        getenv("JASMINE_WORKER_CONFIG", None),
        "~/.jasmine_worker.cfg",
        "jasmine_worker.cfg",
    ]
    config_file_paths: list[str] = [
        expanduser(path) for path in possible_config_file_paths if path
    ]

    config_parser = ConfigParser()
    config_parser.read(config_file_paths)

    return config_parser


@cache
def celery_handle():
    return Celery(
        "jasmine_etl",
        broker=app_config()["celery"]["broker_url"],
        backend=app_config()["celery"].get("backend_url", None),
        include=["jasmine.etl.worker_tasks"],
    )


def sqla_uri_from_config_section(config_section) -> str:
    """
    >>> from jasmine.etl.app_base import sqla_uri_from_config_section
    >>> sqla_uri_from_config_section({
    ...     "uri": "mysq://blah:blah@blah/{username}={user}, {password}={pass}, {database}={db}",
    ...     "username": "username",
    ...     "password": "password",
    ...     "host": "localhost",
    ...     "database": "database",
    ... })
    'mysq://blah:blah@blah/username=username, password=password, database=database'
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


@cache
def redis_handle():
    return Redis.from_url(app_config()["redis"]["url"])


DEFAULT_ACQUIRE_TIMEOUT = 1.0  # Seconds.


@cache
def redislock(
    key: str,
    task_timeout: int,
    acquire_timeout: Optional[float] = None,
):
    acquire_timeout = acquire_timeout or DEFAULT_ACQUIRE_TIMEOUT
    assert acquire_timeout is not None  # For MyPy.

    return Redlock(
        key=key,
        masters={redis_handle()},
        raise_on_redis_errors=True,
        auto_release_time=task_timeout,
        context_manager_blocking=True,
        context_manager_timeout=acquire_timeout,
    )


@contextmanager
def timed_lock(
    key_parts_strs: list[str],
    task_timeout: int,
    acquire_timeout: Optional[float] = None,
):
    key_str = ":".join(key_parts_strs)
    lock = redislock(key_str, task_timeout, acquire_timeout=acquire_timeout)

    try:
        with lock:
            yield lock
    except ReleaseUnlockedLock as e:
        raise RuntimeError(f"Error while trying to lock/unlock redis to run task: {e}")


def lock_free(
    *key_parts_strs: str,
    task_timeout: int,
    acquire_timeout: Optional[float] = None,
):
    key_str = ":".join(key_parts_strs)
    lock = redislock(key_str, task_timeout, acquire_timeout)

    return lock.locked()
