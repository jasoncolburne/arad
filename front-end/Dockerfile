# syntax=docker/dockerfile:1

FROM node:slim

ARG DEPLOYMENT_ENVIRONMENT
ENV DEPLOYMENT_ENVIRONMENT ${DEPLOYMENT_ENVIRONMENT}
ENV PORT 80

RUN \
    if [ "${DEPLOYMENT_ENVIRONMENT}" = "production" ]; then \
        echo "skipping package installation for production build"; \
    else \
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
            curl \
            --no-install-recommends; \
    fi

WORKDIR /app
COPY package.json .
COPY yarn.lock .

RUN \
    if [ "${DEPLOYMENT_ENVIRONMENT}" = "production" ]; then \
        yarn install --production=true --frozen-lockfile; \
    else \
        yarn install --production=false --frozen-lockfile; \
    fi

COPY . .

RUN \
    if [ "${DEPLOYMENT_ENVIRONMENT}" = "production" ]; then \
        yarn build; \
    fi


CMD ["yarn", "start"]
