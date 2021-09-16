from ariadne import ObjectType

user_models_type_defs = """
type Organization {
    organization_id: ID!
    name: String!
    users: [User]!
    teams: [Team]!
    backends: [Backend]!
    projects: [Project]!
}

type User {
    user_id: ID!
    organization: Organization!
    email: String!
    name: String!
    teams: [Team]!
    default_project: Project
}

type Team {
    team_id: ID!
    organization: Organization!
    name: String!
    members: [User]!
}
"""
