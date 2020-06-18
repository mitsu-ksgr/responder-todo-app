#!/bin/bash
set -eu

if [ "${1+$1}" = "-i" ]; then
    # install dependencies
    docker-compose exec web pipenv install --system --dev
fi

echo "----- Lint with flake8 -----"
docker-compose exec web pipenv run flake8 --exit-zero app/*.py app/*/*.py

echo "----- Format with black -----"
docker-compose exec web pipenv run black app/*.py app/*/*.py

