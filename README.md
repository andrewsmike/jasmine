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
$ cd jasmine-models
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


How do I add an ETL / materialization?
======================================

ETL patterns, or materializations, have multiple components:
- `jasmine-sql/jasmine/sql/transforms/{etl}.py`: SQL manipulations and analyses used by the ETL.
- `jasmine-etl/jasmine/etl/materializations/{etl}.py`: ETL backend database interaction logic, event handling, and scheduling.
- `jasmine-models/jasmine/models/materializations/{etl}.py`: Database model and state-machine logical description.

Between these files, the statefullness and correctness properties, scheduling semantics, available events, backend interactions, SQL analysis, and SQL generation logic are handled for every ETL pattern.y
The borders can be a bit fuzzy; the exact setup here may evolve.

To add a materialization, you'll also have to add the materialization (and possibly view) type to the appropriate schemas, and add appropriate references to the new objects through the __init__ hierarchy above as necessary.


How do I run a celery task manually?
====================================
Open up the [celery task monitor](http://localhost:5555/tasks) (at http://localhost:5555/tasks) to see tasks as they are processed.
Find your backend docker container's name using `docker ps` (here jasmnie-backend-1) and use the following syntax to call your function:
```sh
$ docker exec jasmine-backend-1 celery -A jasmine.etl.app call jasmine.etl.worker_tasks.view_result_preview --args '[[28]]' --kwargs '{}'
```
This translates to `view_result_preview([28], **{})`.

The command will return a task ID, such as `dbd04d00-cb0d-4eef-954b-75577f152e74`, which you can use to fetch the status and result:
```sh
$ docker exec jasmine-backend-1 celery -A jasmine.etl.app result dbd04d00-cb0d-4eef-954b-75577f152e74
[{'Organization': 'My Company', 'Project': '[dev]', ...}, ...]
```

You may find these aliases useful:
```sh
function container_name {
    docker ps --format 'table {{.Names}}' | grep "$1"
}

function jasmine_celery_run {
    TASK_ID=$(docker exec $(container_name jasmine-backend) celery -A jasmine.etl.app call jasmine.etl.worker_tasks.$1 --args "$2" --kwargs "$3")
    echo "Running with task ID $TASK_ID."
    docker exec $(container_name jasmine-backend) celery -A jasmine.etl.app result $TASK_ID
}
```
This will call the function and print out the result, and can be ran as `jasmine_celery_run view_result_preview '[[28]]' '{}'`.

After creating, say, a view materialization, you can walk it through its various stages like this:
```sh
$ jasmine_celery_run execute_materialization_event '[[<MATERIALIZATION_ID>], "verify"]' '{}' 
Running with task ID 1595f9a6-7772-44db-94b9-f26ce105b828.

$ jasmine_celery_run execute_materialization_event '[[<MATERIALIZATION_ID>], "create"]' '{}'
Running with task ID a4f7b010-dd84-47ab-bca4-d2a287edf9e2.

$ # Done. Check materializations.
```
