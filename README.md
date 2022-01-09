Jasmine Web: Putting the 'T' in 'ETL'.
==================================
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

Jasmine Web is a web-app and backend service that automatically translates your SQL queries into optimized ETL patterns with managed lifecycles.
Jasmine uses a variety of ETL strategies, along with a SQL manipulation library, to make your analyses easy, near-realtime, and performant.

Warning: Jasmine has a solid foundation and does things no other library offers, but it is still in pre-alpha and we provide no guarantees of anything. Use at your own risk.
I believe this data engineering strategy will eat the world, but I haven't had the free time to build a _complete_ product around it yet.

Screenshots
===========
![Jasmine Web UI](https://github.com/andrewsmike/jasmine/blob/main/screenshots/main_edit_view.png?raw=true)

How does it work?
=================
Almost all ETL technologies strive to do one thing: Keep the results of a SQL query around as new data arrives.
How they do this varies drammatically depending on the liveliness, correctness, and performance constraints, as well as the underlying database technologies.

Because every use case needs a different solution, data engineers spend their entire careers building scores of variants of each ETL pattern for each new SQL query they want to make available.
This seriously hinders analysis response time (leading to solutions like ELT platforms) and is is a massive burden that can be automated with the right tools.

Jasmine takes these SQL queries and automatically compiles them down into known ETL patterns with explicit latency guarantees that work on a variety of backend platforms.
This means you can use the same query to run a daily batch job, maintain a low-latency streaming join with windows, and as a soft-realtime query with no join windows / historical correctness, all by selecting a few options.

Data is entirely hosted and processed on your database; Jasmine just sends it the commands it needs to keep your analysis fresh and up to date.
ETL pattern lifecycles are safely and fully managed by Jasmine; no more manually CREATE-ing / RENAME-ing / DROP-ing tables; just click a button.
Each ETL pattern is carefully vetted to ensure safety and raise alerts when something looks wrong.


Setting up
==========
- Run `for PROJECT in webserver models sql etl; do pushd jasmine-$PROJECT && pip install -e '.[dev]' && popd`.
- Run `docker-compose up` to start the services (and build them if necessary).
- Copy `config/dev/example_jasmine_webserver.cfg` to `config/dev/jasmine_webserver.cfg`, optionally adding missing credentials.
- Add the database at `mysql://jasmine_web_su:password@127.0.0.1:3305/jasmine_web` to your favorite SQL client.
- Install your distro's redis package and use `redis-cli` to access the docker redis instance for testing.

Navigate to http://localhost:8000/, and the app should be visible and initialized with example data.

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
While we use database dumps (`config/dev/dev_database_dump.sql`) to initialize a new schema, we use [alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html) to handle upgrades.

Upgrading typically looks like this:
```bash
$ cd jasmine-models
jasmine-models/ $ alembic revision --autogenerate -m "Add my fancy new column."
jasmine-models/ $ less migrations/versions/generated_migration_file_name.py  # Review and make any necessary edits.
jasmine-models/ $ alembic upgrade head
```

Please refresh the MySQL dump, along with the derived MySQL testing database dump, using the `./tools/update_sql_dumps.sh` command.
See its documentation for details.
This script assumes jasmine is located in `~/src/jasmine` and requires `mysqldump` to be installed.

You can also populate schema without data in a database by running `$ jasmine_initialize_schema`.


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
- `jasmine-models/jasmine/models/materializations/{etl}.py`: Database model and lifecycle state-machine logical description.

The also need to be registered with the system in the relevant `__init__.py` files:
- `jasmine-etl/jasmine/etl/materializations/__init__.py`: Registration for ETL backend event funcs and resource name func.
- `jasmine-models/jasmine/models/materializations/__init__.py`: Registration for database model and lifecycle state machine logical description.

Between these files, the statefullness and correctness properties, scheduling semantics, available events, backend interactions, SQL analysis, and SQL generation logic are handled for every ETL pattern.
The borders can be a bit fuzzy; the exact setup here may evolve.

To add a materialization, you'll also have to add the materialization type (and any new view types) to the appropriate schemas and add appropriate references to the new objects through the `__init__` hierarchy above as necessary.

There are a variety of helpful utility modules throughout jasmine-sql and jasmine-etl.
I recommend you read over existing ETLs and investigate any used modules to get a sense for what tools are available.
Examples include `jasmine.etl.ddl_tools`, `jasmine.etl.backends`, `jasmine.sql.table_spec`, `jasmine.sql.analysis`, and more.

How do I debug an ETL?
----------------------
There are three good ways to debug an ETL:

- Manually launch celery materialization events through celery, described below.
- Write your lifecycle tests in `test_materializations.py` and debug step-by-step (using `pytest -k test_{materialization}_lifecycle`.)
- Step through materialization states using the `jasmine_step_mat` command.

The `jasmine_step_mat` command describes the materialization's and the backend's state thoroughly before and after every step.
This includes every materialization field, what tables/views/triggers from the materialization exist in the backend, their CREATE statements, and sample data.

This makes it particularly useful for identifying problems quickly, and it operates against the `jasmine_web` database directly, rather than the test database.
This means it doesn't need to reload the database at every step, and can be used on production instances as well.

In your docker container (`docker-compose exec backend /bin/bash`), the command is
```sh
docker-backend $ jasmine_step_mat <view_id> <materialization_type> <action1,action2,...> <config_json>?
```

Use the action 'init' to create new (or terminate, then create new) materializations.
For complicated configurations, save them to a file, then use the following invocation:
```sh
docker-backend $ jasmine_step_mat 51 upsert init,verify,create,update "$(cat /opt/jasmine-etl/jasmine/etl/materializations/tests/upsert_example_conf.json)"
```

You also invoke it from outside docker using exec directly after remapping the config file path:
```sh
$ docker-compose exec backend jasmine_step_mat 51 upsert init,verify,create,update "$(cat jasmine-etl/jasmine/etl/materializations/tests/upsert_example_conf.json)"
```


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

Tools
=====
Additional debugging and project management tools are available in the `tools/` directory.
Some of these are critical and will work by default, others require extra setup.
Consult their header comments (or README.md files) for details.

Debugging:

- `backend_events.sh`: Display all backend events for the last 30m.
- `mysql_trace.py`: Visualize concurrent transactions in MySQL.
- `update_sql_dumps.sh`: Update jasmine\_web database dump and jasmine\_test database dumps.

Project management:

- `cloc.sh`: Summarize jasmine lines of code.
- `jasmine_tracker/update_backlog.py`: Update the jasmine google sheets issue tracker. See `jasmine_tracker/README.md` for details.
