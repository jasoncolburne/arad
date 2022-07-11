# syntax=docker/dockerfile:1

########################################
# ARAD Dockerfile
# * edit the source file in `node-common`
########################################

FROM python:slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV POETRY_HOME=/opt/poetry
ENV PATH="${POETRY_HOME}/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

RUN apt-get update
RUN apt-get -y install --no-install-recommends \
  gcc \
  libc-dev \
  curl \
  ca-certificates

WORKDIR /app
COPY . .

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | \
  python - --preview

RUN poetry config virtualenvs.options.system-site-packages true
RUN poetry check
RUN poetry lock --check
RUN poetry install --no-root

RUN apt-get -y remove gcc libc-dev ca-certificates
RUN apt-get -y autoremove

CMD ["poetry", "run", "start"]
