#!/bin/bash
set -eu

TARGET="tests"

if [ -n "${1+$1}" ]; then
    TARGET="$1"
fi

docker-compose exec web pipenv run pytest $TARGET

