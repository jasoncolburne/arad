#!/usr/bin/env bash

cd /app
. $(./echo_activate_path)
alembic upgrade head
