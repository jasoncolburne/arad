# syntax=docker/dockerfile:1

FROM nginx:latest

COPY ./etc/nginx/conf.d/default.conf /etc/nginx/conf.d/

EXPOSE 80
STOPSIGNAL SIGQUIT
CMD ["nginx", "-g", "daemon off;"]