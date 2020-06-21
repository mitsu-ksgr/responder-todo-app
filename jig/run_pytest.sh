#!/bin/bash
set -eu

TARGET="tests"

if [ -n "${1+$1}" ]; then
    TARGET="$1"
fi

docker-compose run -e APP_ENV=test --rm web\
    pipenv run pytest $TARGET

