#!/usr/bin/env bash

set -eo pipefail

service nginx start || echo "nginx failed to start"
poetry run start
