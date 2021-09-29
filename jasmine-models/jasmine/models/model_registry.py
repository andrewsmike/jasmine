"""
Backend: An ETL and data provider backend
Project: A top-level path directory bound to a backend.
Query: A persistent editable query spec. Bound to user dev project by default.
Materialization: A view acceleration.

Organization: Unit that "owns" all resources. (Account?)
Teams: Groups of users.
Users: Members of an organization.

TODO:
- Billing mechanism / schema
- Backends
- ETL service connections / materialization events
- Permissions (org, team, queries)

- Directory-style permissions for projects / directories.

- All users have a default [dev] project.
- Other projects may be write-protected, or write-disabled.
- Queries in write-disabled projects cannot be directly edited. They must be copied and hot-swapped.

"""
from sqlalchemy.orm import registry

orm_registry = registry()
