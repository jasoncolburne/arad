# syntax=docker/dockerfile:1

FROM node:slim

WORKDIR /app
COPY ./package.json ./package.json
COPY ./package-lock.json ./package-lock.json

RUN npm install

COPY . .

CMD ["npm", "start"]
