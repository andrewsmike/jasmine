from ariadne import make_executable_schema

from jasmine.webserver.graphql_models.mutation import mutation_obj, mutation_type_defs
from jasmine.webserver.graphql_models.project_models import (
    project_models_type_defs,
    view_spec_type,
)
from jasmine.webserver.graphql_models.query import query_obj, query_type_defs
from jasmine.webserver.graphql_models.user_models import user_models_type_defs

type_defs = "\n".join(
    [
        mutation_type_defs,
        project_models_type_defs,
        query_type_defs,
        user_models_type_defs,
    ]
)

union_type_resolvers = [
    view_spec_type,
]

graphql_schema = make_executable_schema(
    type_defs, [query_obj, mutation_obj] + union_type_resolvers
)
