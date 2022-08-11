# syntax=docker/dockerfile:1

FROM nginx:latest

WORKDIR /secrets
RUN openssl req \
        -nodes \
        -x509 \
        -newkey rsa:4096 \
        -keyout nginx-private-key.pem \
        -out nginx-certificate.pem \
        -sha256 \
        -days 21 \
        -subj "/CN=api"

COPY ./etc/nginx/conf.d/default.conf /etc/nginx/conf.d/
COPY ./etc/nginx/nginx.conf /etc/nginx/

RUN mkdir /local
RUN touch /local/administrator.conf
RUN touch /local/reviewer.conf
RUN touch /local/reader.conf
RUN touch /local/identity.conf

RUN mkdir -p /etc/nginx/conf.d/upstreams
RUN ln -sf /local/administrator.conf /etc/nginx/conf.d/upstreams/administrator.conf
RUN ln -sf /local/reviewer.conf /etc/nginx/conf.d/upstreams/reviewer.conf
RUN ln -sf /local/reader.conf /etc/nginx/conf.d/upstreams/reader.conf
RUN ln -sf /local/identity.conf /etc/nginx/conf.d/upstreams/identity.conf

RUN mkdir -p /etc/nginx/ssl
RUN ln -sf /secrets/nginx-private-key.pem /etc/nginx/ssl/key.pem
RUN ln -sf /secrets/nginx-certificate.pem /etc/nginx/ssl/cert.pem

WORKDIR /

EXPOSE 443
STOPSIGNAL SIGQUIT
CMD ["nginx"]
