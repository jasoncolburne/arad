# syntax=docker/dockerfile:1

FROM redis
RUN mkdir /var/run/redis
RUN chown redis:redis /var/run/redis
COPY redis.conf /etc/redis/redis.conf
CMD [ "redis-server", "/etc/redis/redis.conf" ]
