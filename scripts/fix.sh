#!/bin/bash -xe

# Script that fix files everywhere

poetry run ruff check . --fix
poetry run ruff check .
poetry run black .
poetry run black --check .
poetry run isort .
poetry run isort --check-only .
