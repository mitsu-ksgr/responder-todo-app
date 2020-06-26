#!/bin/bash
set -eu

docker-compose exec web python ./jig/reset_db.py $@

