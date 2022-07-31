# syntax=docker/dockerfile:1

FROM node:slim

ARG DEPLOYMENT_ENVIRONMENT
ENV DEPLOYMENT_ENVIRONMENT ${DEPLOYMENT_ENVIRONMENT}

RUN \
    if [ "${DEPLOYMENT_ENVIRONMENT}" = "development" ]; then \
        apt-get update; \
        apt-get install -y \
            xvfb \
            librust-gobject-sys-dev \
            libnss3 \
            libatk-bridge2.0-0 \
            libcups2 \
            libgdk-pixbuf2.0-0 \
            libgtk-3-0 \
            libgbm1 \
            libasound2 \
            --no-install-recommends; \
    fi

WORKDIR /app
COPY package.json .
COPY yarn.lock .

RUN \
    if [ "${DEPLOYMENT_ENVIRONMENT}" = "production" ]; then \
        yarn install --production=true; \
    else \
        yarn install --production=false; \
    fi

COPY . .

RUN \
    if [ "${DEPLOYMENT_ENVIRONMENT}" = "production" ]; then \
        yarn build; \
    fi


CMD ["yarn", "start"]
