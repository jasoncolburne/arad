# syntax=docker/dockerfile:1

########################################
# ARAD Dockerfile
# * edit the source file in `node-common`
########################################

FROM debian:bullseye-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV POETRY_HOME=/opt/poetry
ENV PATH="${POETRY_HOME}/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

RUN apt-get update
RUN apt-get -y install --no-install-recommends \
  python-is-python3 \
  python3-venv \
  curl \
  ca-certificates

WORKDIR /app
COPY . .

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | \
  python - --preview

RUN poetry config virtualenvs.options.system-site-packages true
RUN poetry lock --check
RUN poetry install --no-root

CMD ["poetry", "run", "start"]
