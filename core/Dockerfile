# syntax=docker/dockerfile:1

########################################
# ARAD Dockerfile
# * edit the source file in `common`
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
  ca-certificates \
  nginx

RUN rm -f /etc/nginx/sites-enabled/default
RUN mkdir -p /etc/nginx/conf.d/streams
RUN ln -sf /local/upstreams.conf /etc/nginx/conf.d/streams/upstreams.conf
COPY nginx.conf /etc/nginx

WORKDIR /app

COPY install-poetry.py .
RUN python ./install-poetry.py --version 1.2.0b3
RUN poetry config virtualenvs.options.system-site-packages true

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry check
RUN poetry lock --check
RUN \
  if [ "${DEPLOYMENT_ENVIRONMENT}" = "production" ]; then \
    poetry install --no-root --without test; \
  else \
    poetry install --no-root --with test; \
  fi

RUN apt-get -y remove gcc libc-dev ca-certificates
RUN apt-get -y autoremove

COPY . .
RUN rm nginx.conf

CMD ["bash", "-c", "./entrypoint.sh"]
