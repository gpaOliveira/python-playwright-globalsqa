#!/bin/bash -xe

# Script that cleanup everything from Docker

docker compose --ansi never \
  --file "$dir/../docker-compose.yml" \
  kill
if [ "$(docker ps -a -q)" ]; then
  docker rm -f $(docker ps -a -q)
fi
if [ "$(docker volume ls -q)" ]; then
  docker volume rm $(docker volume ls -q)
fi
