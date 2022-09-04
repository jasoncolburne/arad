# syntax=docker/dockerfile:1

FROM nginx:latest

COPY ./etc/nginx/conf.d/default.conf /etc/nginx/conf.d/
COPY ./etc/nginx/nginx.conf /etc/nginx/

WORKDIR /app
COPY ./build .

EXPOSE 80
STOPSIGNAL SIGQUIT
CMD ["nginx"]
