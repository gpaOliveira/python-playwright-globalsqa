#!/bin/bash -xe

# Script that runs tests in Docker

dir="$(dirname -- "$(which -- "$0" 2>/dev/null || realpath -- "./$0")")"
docker compose --ansi never \
  --file "$dir/../docker-compose.yml" \
  up --build