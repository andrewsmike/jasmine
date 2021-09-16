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

def orm_model(cls):
    """
    Stand-in for @orm_registry.mapped.

    When pytest invokes a file, looking for doctests, it can end up importing it twice.
    (It loads the module's __init__, which loads the file, then loads it again for execution.)
    This is normally fine, but calling registry.mapped() twice throws an exception.

    If table is already defined, don't map the model. This avoids the issue, though
    any tests using local references will find unmapped base classes.
    """
    if cls.__tablename__ in orm_registry.metadata.tables:
        return cls
    else:
        return orm_registry.mapped(cls)
