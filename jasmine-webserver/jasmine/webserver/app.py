"""
Instantiate a global GraphQL server.
Invoke with `uvicorn jasmine.webserver.app:app`.
"""
from ariadne.asgi import GraphQL

from jasmine.models import orm_registry
from jasmine.webserver.app_base import app_db_engine_session
from jasmine.webserver.graphql_models import graphql_schema

__all__ = [
    "app",
    "initialize_schema",
]

app = GraphQL(graphql_schema, debug=True)


def initialize_schema():
    engine, session = app_db_engine_session(orm_registry)
    orm_registry.metadata.create_all(engine)
