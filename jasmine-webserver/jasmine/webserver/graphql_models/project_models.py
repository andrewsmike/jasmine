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
    history_table
}

type QuerySpec {
    query_text: String!
}

type HistoryTableSpec {
    source_db_name: String!
    source_table_name: String!
    retention_period_seconds: Int!
    trim_frequency_seconds: Int!
}

union ViewSpec = QuerySpec | HistoryTableSpec

type View {
    view_id: ID!
    view_type: ViewType!
    project: Project!
    path: String!
    spec: ViewSpec!
    materializations: [Materialization]!
    backend_events: [BackendEvent]!
}

enum MaterializationType {
    view
    history_table
    upsert
    reload
    incremental
}


type HistoryTableMaterializationSpec {
    source_table: String!
    min_history_seconds: Int!
    trim_frequency_seconds: Int!
}


type UpsertMaterializationSpec {
    column_type_decls: JSON
    updated_ts_column_name: String!
    unique_keys: JSON
    keys: JSON
    start_timestamp: Int
}

type ReloadMaterializationSpec {
    column_type_decls: JSON
    primary_key: [String]
    unique_keys: JSON
    keys: JSON
}

type IncrementalMaterializationSpec {
    column_type_decls: JSON
    primary_key: [String]
    unique_keys: JSON
    keys: JSON
}

union MaterializationSpec = HistoryTableMaterializationSpec | UpsertMaterializationSpec | ReloadMaterializationSpec | IncrementalMaterializationSpec

type Materialization {
    materialization_id: ID!
    materialization_type: MaterializationType!
    state: String!
    view: View!
    config: MaterializationSpec
    backend_events: [BackendEvent]!
}
"""


# Put this first to avoid typing errors in decorator pattern.
def resolve_view_spec_type(view_spec, *_):
    return {
        "query": "QuerySpec",
        "history_table": "HistoryTableSpec",
    }[view_spec["view_type"]]


view_spec_type = UnionType("ViewSpec", resolve_view_spec_type)
