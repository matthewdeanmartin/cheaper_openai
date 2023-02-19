#!/bin/bash
set -euo pipefail
bash --version

pipenv run black .
pipenv run pylint chats
pipenv run pytest test
pipenv run pre-commit install
