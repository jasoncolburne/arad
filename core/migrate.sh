#!/usr/bin/env bash

set -eo pipefail

cd /app
. $(./echo_activate_path)
alembic upgrade head
