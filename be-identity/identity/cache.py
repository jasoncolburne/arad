from datetime import datetime
from uuid import UUID
import os

import aioredis

from common.types.exception import UnauthorizedException


CACHE_URL = os.environ.get("CACHE_URL")

class Cache:
    def __init__(
        self,
    ):
        self.redis = aioredis.from_url(CACHE_URL, decode_responses=True)

    async def store_refresh_token(self, refresh_token: str, user_id: UUID, expiration: datetime):
        key = self._key(refresh_token=refresh_token)
        value = {
            "user_id": str(user_id),
            "expiration": str(int(expiration.timestamp()))
        }
        await self.redis.hset(key, mapping=value)

    async def fetch_user_id_from_valid_refresh_token(self, refresh_token: str) -> UUID:
        key = self._key(refresh_token=refresh_token)
        value = await self.redis.hgetall(key)

        expiration_timestamp = int(value["expiration"])
        if expiration_timestamp >= int(datetime.utcnow().timestamp()):
            return UUID(value["user_id"])
        else:
            raise UnauthorizedException()

    def _key(self, refresh_token: str) -> str:
        return f"refresh-token-{refresh_token}"
