#!/bin/bash
set -eu

#echo "$@"

docker-compose exec web pipenv run alembic "$@"

