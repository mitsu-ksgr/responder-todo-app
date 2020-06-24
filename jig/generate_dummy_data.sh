#!/bin/bash
set -eu

docker-compose exec web python ./jig/generate_dummy_data.py $@

