#!/bin/bash
set -eu

docker-compose exec web pipenv run alembic $@

