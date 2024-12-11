#!/bin/bash

set -eu

poetry run alembic upgrade head
poetry run prefect server start --host 0.0.0.0