# syntax=docker/dockerfile:1

FROM node:slim

RUN apt-get update
RUN apt-get install -y \
    xvfb \
    librust-gobject-sys-dev \
    libnss3 \
    libatk-bridge2.0-0 \
    libcups2 \
    libgdk-pixbuf2.0-0 \
    libgtk-3-0 \
    libgbm1 \
    libasound2 \
    --no-install-recommends

WORKDIR /app
COPY package.json .
COPY yarn.lock .

RUN yarn install

COPY . .

CMD ["yarn", "start"]
