ETL testing against MySQL database.
===================================
To thoroughly test ETLs and materialization logic, these tests verify correct
behavior when actually running ETLs against a test database.

Database harness
----------------
Tests are run on the host machine which is mocked to point at the docker redis/MySQL instances.
A test database (jasmine_test) is destroyed and prepopulated for each test group to simplify implementation.


Maintaining test database dump
------------------------------
The database dump can be derived from the dev database dump in config/dev.
This is currently automated by `tools/update_sql_dumps.sh`.

As of 2021-12-15, the process for generating the test dump from the main dump is:
- Replace all references to jasmine_web with jasmine_test, but do not change any jasmine_web_su references.
- Replace the single backend rows' spec's connection_args' host/port with 127.0.0.1 and 3305.


