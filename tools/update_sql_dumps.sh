#!/bin/bash

# Update the initializing database dump, as well as the test-database initializing dump,
# from the current state of jasmine_web.
# Assumes a set location for the jasmine monorepo.

pushd ~/src/jasmine

mysqldump \
    --user=root \
    --password=root \
    --host=127.0.0.1 \
    --port=3305 \
    --databases jasmine_web \
    > config/dev/dev_database_dump.sql

# Process can be found in jasmine-etl/jasmine/etl/materializations/tests/README.md
cat config/dev/dev_database_dump.sql \
    | sed 's/CREATE DATABASE/DROP DATABASE IF EXISTS jasmine_test;\nCREATE DATABASE /g' \
    | sed 's/jasmine_web_su/jasmine_su_web/g' \
    | sed 's/jasmine_web/jasmine_test/g' \
    | sed 's/jasmine_su_web/jasmine_web_su/g' \
    | sed 's/\\"host\\": \\"database\\",/\\"host\\": \\"127.0.0.1\\",/g' \
    | sed 's/\\"port\\": 3306,/\\"port\\": 3305,/g' \
    > jasmine-etl/jasmine/etl/materializations/tests/test_database_dump.sql

popd
