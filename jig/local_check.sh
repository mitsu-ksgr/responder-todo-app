#!/bin/bash
set -eu

echo "----- Lint with flake8 -----"
docker-compose exec web pipenv run \
    flake8 --count --exit-zero app/*.py app/*/*.py

echo "----- Format with black -----"
docker-compose exec web pipenv run black app/*.py app/*/*.py

