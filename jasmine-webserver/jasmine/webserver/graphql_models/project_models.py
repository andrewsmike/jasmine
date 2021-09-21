from ariadne import UnionType

project_models_type_defs = """
type Backend {
    backend_id: ID!
    organization: Organization!
    name: String!
    backend_type: String!
    spec: JSON!
    projects: [Project]!
}

type Project {
    project_id: ID!
    organization: Organization!
    name: String!
    backend: Backend!
    views: [View]!
}

enum ViewType {
    query
}

type QuerySpec {
    query_text: String!
}

union ViewSpec = QuerySpec

type View {
    view_id: ID!
    view_type: ViewType!
    project: Project!
    path: String!
    spec: ViewSpec!
}
"""
view_spec_type = UnionType("ViewSpec")


@view_spec_type.type_resolver
def resolve_view_spec_type(view_spec, *_):
    return {
        "query": "QuerySpec",
    }[view_spec["view_type"]]
