from ariadne import UnionType

project_models_type_defs = """
type Backend {
    backend_id: ID!
    organization: Organization!
    name: String!
    backend_type: String!
    spec: JSON!
    projects: [Project]!
    backend_events: [BackendEvent]!
}

type BackendEvent {
    backend_event_id: ID!
    title: String!
    description: String
    created_time: DateTime!
    backend: Backend!
    project: Project
    view: View
}

type Project {
    project_id: ID!
    organization: Organization!
    name: String!
    backend: Backend!
    views: [View]!
    backend_events: [BackendEvent]!
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
    backend_events: [BackendEvent]!
}
"""
view_spec_type = UnionType("ViewSpec")


@view_spec_type.type_resolver
def resolve_view_spec_type(view_spec, *_):
    return {
        "query": "QuerySpec",
    }[view_spec["view_type"]]
