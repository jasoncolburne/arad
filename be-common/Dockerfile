# syntax=docker/dockerfile:1

########################################
# ARAD Dockerfile
# * edit the source file in `be-common`
########################################

FROM python:slim-bullseye

ARG DEPLOYMENT_ENVIRONMENT
ENV DEPLOYMENT_ENVIRONMENT ${DEPLOYMENT_ENVIRONMENT}

ENV PYTHONDONTWRITEBYTECODE=1
ENV POETRY_HOME=/opt/poetry
ENV PATH="${POETRY_HOME}/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

RUN apt-get update
RUN apt-get -y install --no-install-recommends \
  gcc \
  libc-dev \
  curl \
  ca-certificates

# TODO download this script and run it from our sources
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | \
  python - --preview

RUN poetry config virtualenvs.options.system-site-packages true

WORKDIR /app
COPY pyproject.toml .
COPY poetry.lock .

RUN poetry check
RUN poetry lock --check
RUN \
  if [ "${DEPLOYMENT_ENVIRONMENT}" == "development" ]; then \
    poetry install --no-root --with test; \
  else \
    poetry install --no-root --without test; \
  fi

RUN apt-get -y remove gcc libc-dev ca-certificates
RUN apt-get -y autoremove

COPY . .

CMD ["poetry", "run", "start"]
