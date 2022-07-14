# syntax=docker/dockerfile:1

FROM node:slim

WORKDIR /app
COPY . .

RUN yarn install

CMD ["yarn", "start"]
