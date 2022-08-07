# syntax=docker/dockerfile:1

FROM nginx:latest

COPY ./etc/nginx/conf.d/default.conf /etc/nginx/conf.d/
RUN mkdir -p /etc/nginx/conf.d/upstreams
RUN ln -sf /local/administrator.conf /etc/nginx/conf.d/upstreams/administrator.conf
RUN ln -sf /local/reviewer.conf /etc/nginx/conf.d/upstreams/reviewer.conf
RUN ln -sf /local/reader.conf /etc/nginx/conf.d/upstreams/reader.conf
RUN ln -sf /local/identity.conf /etc/nginx/conf.d/upstreams/identity.conf

EXPOSE 80
STOPSIGNAL SIGQUIT
CMD ["nginx", "-g", "daemon off;"]