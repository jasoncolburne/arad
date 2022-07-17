# syntax=docker/dockerfile:1

FROM node:slim

WORKDIR /app
COPY package.json .
COPY yarn.lock .

RUN yarn install

COPY . .

CMD ["yarn", "start"]
