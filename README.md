Jasmine Web: Putting the 'T' in 'ETL'.
==================================
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

Jasmine Web is a web-app and backend service that automatically translates your SQL queries into optimized ETL patterns.
Jasmine is uses a variety of ETL strategies, along with a SQL manipulation library, to make your analyses easy, near-realtime, and performant.

Setting up
==========
- Run `for PROJECT in webserver models sql etl; do pushd jasmine-$PROJECT && pip install -e '.[dev]' && popd`.
- Run `docker-compose up` to start the services (and build them if necessary).
- Run `jasmine_initialize_schema` to initialize your database.
- Copy `config/dev/example_jasmine_webserver.cfg` to `config/dev/jasmine_webserver.cfg`, optionally adding missing credentials.
- Add the database at `mysql://jasmine_web_su:password@127.0.0.1:3305/jasmine_web` to your favorite SQL client.
- Install your distro's redis package and use `redis-cli` to access the docker redis instance for testing.
- Dump `config/dev/dev_database_dump.sql` for default company/user/backend/views/etc dev testing data, or set up manually.

Navigate to http://localhost:8000/, and the app should be visible.

Useful links
------------
- `http://localhost:8000/console`: The webapp.
- `http://localhost:8000/api/graphql`: Directly interact with the webserver's GraphQL API. Extremely useful for development.
- `mysql://127.0.0.1:3305`: The webapp's database server.
- `http://localhost:8001`: Direct access to the npm development webserver.
- `http://localhost:8002`: Direct access to the GraphQL webserver.
- `http://localhost:5555/`: Task manager (celery) monitoring app ("flowey"). You can see task arguments, status, and results here.
- `http://localhost:15672`: Worker router (RabbitMQ) monitoring app. (Username/pass: 'username'/'password').


Maintenance
===========
Database Migrations
-------------------
While we use `$ jasmine_initialize_schema` or `config/dev/dev_database_dump.sql` to initialize a new schema, we use [alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html) to handle upgrades.

Upgrading typically looks like this:
```bash
$ cd jasmine-webserver
jasmine-models/ $ alembic revision --autogenerate -m "Add my fancy new column."
jasmine-models/ $ less migrations/versions/generated_migration_file_name.py  # Review and make any necessary edits.
jasmine-models/ $ alembic upgrade head
```

Please refresh the MySQL dump when you upgrade the schema.


Architecture
============
Jasmine is split into a few components:
- Nginx: Reverse proxies requests between the jasmine-webui's npm static resource server and jasmine-webserver's python/uvicorn GraphQL API server.
- Webapp: The React and Material-UI based frontend. Uses typescript, the Apollo GraphQL client, and a variety of other packages.
    Served using `npm start` from the `jasmine-webui` directory and is responsible for most static resources.
    Config in `config/dev/nginx.config`.
- GraphQL API: The Ariadne GraphQL based python webserver. Services API calls, as well as the GraphQL API debugging webapp.
    Served using uvicorn, located in the `jasmine-webserver/` directory, and connects to the database.
- Database: MySQL backend database.
- Jasmine-ETL: RabbitMQ-based celery worker pool for running ETL and management jobs. Includes celery beat cron-like scheduler.
- jasmine-models: Shared package holding the ORM models.
- jasmine-sql: Utility package for SQL manipulation.
