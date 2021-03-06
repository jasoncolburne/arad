import datetime
import os
import uuid

import aioredis

import common.datatypes.exception


# TODO move all this stuff into a settings file
REFRESH_TOKEN_EXPIRATION_DAYS = 7
SECONDS_IN_ONE_DAY = 86400  # 24 * 60 * 60
REFRESH_TOKEN_EXPIRATION_SECONDS = REFRESH_TOKEN_EXPIRATION_DAYS * SECONDS_IN_ONE_DAY
CACHE_URL = os.environ.get("CACHE_URL")


class Cache:
    def __init__(
        self,
    ) -> None:
        self.redis = aioredis.from_url(CACHE_URL, decode_responses=True)

    async def store_refresh_token(
        self, refresh_token: str, user_id: uuid.UUID, expiration: datetime.datetime
    ) -> None:
        token_key = self._token_key(refresh_token=refresh_token)
        token_data = {
            "user_id": str(user_id),
            "expiration": str(int(expiration.timestamp())),
        }

        await self.redis.hset(token_key, mapping=token_data)
        await self.redis.expire(token_key, REFRESH_TOKEN_EXPIRATION_SECONDS)

        user_key = self._user_key(user_id=user_id)
        await self.redis.hset(user_key, token_key, str(int(expiration.timestamp())))
        await self.redis.expire(user_key, REFRESH_TOKEN_EXPIRATION_SECONDS)

    async def purge_refresh_token(self, refresh_token: str) -> None:
        token_key = self._token_key(refresh_token=refresh_token)

        user_id_string = await self.redis.hget(token_key, "user_id")
        if not user_id_string:
            return

        user_id = uuid.UUID(user_id_string)

        await self.redis.delete(token_key)

        user_key = self._user_key(user_id)
        await self.redis.hdel(user_key, token_key)

    async def purge_all_refresh_tokens_for_user_id(self, user_id: uuid.UUID) -> None:
        user_key = self._user_key(user_id=user_id)
        token_keys = await self.redis.hkeys(user_key)

        await self.redis.delete(user_key)
        if not token_keys:
            return

        for token_key in token_keys:
            await self.redis.delete(token_key)

    async def fetch_user_id_from_valid_refresh_token(
        self, refresh_token: str
    ) -> uuid.UUID:
        token_key = self._token_key(refresh_token=refresh_token)
        token_data = await self.redis.hgetall(token_key)

        try:
            expiration_timestamp = int(token_data["expiration"])
        except KeyError as exc:
            raise common.datatypes.exception.UnauthorizedException() from exc

        if expiration_timestamp < int(datetime.datetime.utcnow().timestamp()):
            raise common.datatypes.exception.UnauthorizedException()

        return uuid.UUID(token_data["user_id"])

    def _token_key(self, refresh_token: str) -> str:
        return f"refresh-token-{refresh_token}"

    def _user_key(self, user_id: uuid.UUID) -> str:
        return f"user_tokens-{str(user_id)}"
