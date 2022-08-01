# syntax=docker/dockerfile:1

FROM nginx:latest

RUN openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
COPY mkcert /usr/local/bin

WORKDIR /etc/nginx/ssl

RUN mkcert --install
RUN mkcert -ecdsa arad-api

WORKDIR /

COPY ./etc/nginx/conf.d/default.conf /etc/nginx/conf.d/

EXPOSE 443
STOPSIGNAL SIGQUIT
CMD ["nginx", "-g", "daemon off;"]