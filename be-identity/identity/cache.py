from datetime import datetime
from uuid import UUID
import os

import aioredis

from common.datatypes.exception import UnauthorizedException


# TODO move all this stuff into a settings file
REFRESH_TOKEN_EXPIRATION_DAYS = 7
SECONDS_IN_ONE_DAY = 86400  # 24 * 60 * 60
REFRESH_TOKEN_EXPIRATION_SECONDS = REFRESH_TOKEN_EXPIRATION_DAYS * SECONDS_IN_ONE_DAY
CACHE_URL = os.environ.get("CACHE_URL")


class Cache:
    def __init__(
        self,
    ):
        self.redis = aioredis.from_url(CACHE_URL, decode_responses=True)

    async def store_refresh_token(
        self, refresh_token: str, user_id: UUID, expiration: datetime
    ):
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

    async def purge_refresh_token(self, refresh_token: str):
        token_key = self._token_key(refresh_token=refresh_token)

        user_id_string = await self.redis.hget(token_key, "user_id")
        if not user_id_string:
            return

        user_id = UUID(user_id_string)

        await self.redis.delete(token_key)

        user_key = self._user_key(user_id)
        await self.redis.hdel(user_key, token_key)

    async def purge_all_refresh_tokens_for_user_id(self, user_id: UUID):
        user_key = self._user_key(user_id=user_id)
        token_keys = await self.redis.hkeys(user_key)

        await self.redis.delete(user_key)
        if not token_keys:
            return

        for token_key in token_keys:
            await self.redis.delete(token_key)

    async def fetch_user_id_from_valid_refresh_token(self, refresh_token: str) -> UUID:
        token_key = self._token_key(refresh_token=refresh_token)
        token_data = await self.redis.hgetall(token_key)

        try:
            expiration_timestamp = int(token_data["expiration"])
        except KeyError:
            raise UnauthorizedException()

        if expiration_timestamp >= int(datetime.utcnow().timestamp()):
            return UUID(token_data["user_id"])
        else:
            raise UnauthorizedException()

    def _token_key(self, refresh_token: str) -> str:
        return f"refresh-token-{refresh_token}"

    def _user_key(self, user_id: UUID) -> str:
        return f"user_tokens-{str(user_id)}"
