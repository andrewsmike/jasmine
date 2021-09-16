from ariadne import ObjectType

project_models_type_defs = """
type Backend {
    backend_id: ID!
    organization: Organization!
    name: String!
    projects: [Project]!
}

type Project {
    project_id: ID!
    organization: Organization!
    name: String!
    backend: Backend!
    queries: [SqlQuery]!
}

type SqlQuery {
    query_id: ID!
    project: Project!
    path: String!
    query_text: String!
}
"""
