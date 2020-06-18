#!/bin/bash
set -eu

docker-compose build
docker-compose up -d

# wait for mysql to be ready...
echo "Waiting for mysql to be ready..."
sleep 5s # tabun 5 byo mo areba ju-bun!

# migration
docker-compose exec web pipenv run alembic upgrade head

echo -e "\n\n"
echo "* Container status"
echo "run: docker-compose ps"
echo ""
echo "* Exit"
echo "run: docker-compose down"
echo ""
echo "* Views"
echo "see: http://localhost:8080/"

