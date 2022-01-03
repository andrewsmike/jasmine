#!/bin/bash
export EXCLUDE_DIRS="--exclude-dir=node_modules --exclude-dir=__pycache__ --exclude-dir=.mypy_cache --exclude-dir=\.pytest_cache --exclude-dir=build"

grep $EXCLUDE_DIRS -rie $@
