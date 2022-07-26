import datetime
import secrets
import unittest.mock
import uuid

import aioredis
import pytest

import common.datatypes.exception

import identity.cache
import identity.services.auth


def token_key(refresh_token: str) -> str:
    return f"refresh-token-{refresh_token}"


def user_key(user_id: uuid.UUID) -> str:
    return f"user_tokens-{str(user_id)}"


@pytest.mark.asyncio
async def test_store_refresh_token__calls_redis() -> None:
    user_id = uuid.uuid4()
    refresh_token = secrets.token_urlsafe(identity.services.auth.REFRESH_TOKEN_BYTES)
    expiration = datetime.datetime.utcnow()

    mock_redis = aioredis.Redis()
    mock_redis.hset = unittest.mock.AsyncMock()
    mock_redis.expire = unittest.mock.AsyncMock()

    cache = identity.cache.Cache(redis=mock_redis)

    await cache.store_refresh_token(
        refresh_token=refresh_token, user_id=user_id, expiration=expiration
    )

    mock_redis.hset.assert_has_awaits(
        calls=[
            unittest.mock.call(
                token_key(refresh_token=refresh_token),
                mapping={
                    "user_id": str(user_id),
                    "expiration": str(int(expiration.timestamp())),
                },
            ),
            unittest.mock.call(
                user_key(user_id=user_id),
                token_key(refresh_token=refresh_token),
                str(int(expiration.timestamp())),
            ),
        ]
    )

    mock_redis.expire.assert_has_awaits(
        calls=[
            unittest.mock.call(
                token_key(refresh_token=refresh_token),
                identity.cache.REFRESH_TOKEN_EXPIRATION_SECONDS,
            ),
            unittest.mock.call(
                user_key(user_id=user_id),
                identity.cache.REFRESH_TOKEN_EXPIRATION_SECONDS,
            ),
        ]
    )


@pytest.mark.asyncio
async def test_purge_refresh_token__calls_redis() -> None:
    user_id = uuid.uuid4()
    refresh_token = secrets.token_urlsafe(identity.services.auth.REFRESH_TOKEN_BYTES)

    mock_redis = aioredis.Redis()
    mock_redis.hget = unittest.mock.AsyncMock(return_value=str(user_id))
    mock_redis.delete = unittest.mock.AsyncMock()
    mock_redis.hdel = unittest.mock.AsyncMock()

    cache = identity.cache.Cache(redis=mock_redis)

    await cache.purge_refresh_token(refresh_token=refresh_token)

    mock_redis.hget.assert_awaited_once_with(
        token_key(refresh_token=refresh_token),
        "user_id",
    )
    mock_redis.delete.assert_awaited_once_with(token_key(refresh_token=refresh_token))
    mock_redis.hdel.assert_awaited_once_with(
        user_key(user_id=user_id),
        token_key(refresh_token=refresh_token),
    )


@pytest.mark.asyncio
async def test_purge_refresh_token__returns_early_when_token_missing() -> None:
    refresh_token = secrets.token_urlsafe(identity.services.auth.REFRESH_TOKEN_BYTES)

    mock_redis = aioredis.Redis()
    mock_redis.hget = unittest.mock.AsyncMock(return_value=None)
    mock_redis.delete = unittest.mock.AsyncMock()
    mock_redis.hdel = unittest.mock.AsyncMock()

    cache = identity.cache.Cache(redis=mock_redis)

    await cache.purge_refresh_token(refresh_token=refresh_token)

    mock_redis.hget.assert_awaited_once_with(
        token_key(refresh_token=refresh_token),
        "user_id",
    )
    mock_redis.delete.assert_not_awaited()
    mock_redis.hdel.assert_not_awaited()


@pytest.mark.asyncio
async def test_purge_all_refresh_tokens_for_user_id__calls_redis() -> None:
    user_id = uuid.uuid4()
    token_one = secrets.token_urlsafe(identity.services.auth.REFRESH_TOKEN_BYTES)
    token_two = secrets.token_urlsafe(identity.services.auth.REFRESH_TOKEN_BYTES)

    token_keys = [
        token_key(refresh_token=token_one),
        token_key(refresh_token=token_two),
    ]

    mock_redis = aioredis.Redis()
    mock_redis.hkeys = unittest.mock.AsyncMock(return_value=token_keys)
    mock_redis.delete = unittest.mock.AsyncMock()

    cache = identity.cache.Cache(redis=mock_redis)

    await cache.purge_all_refresh_tokens_for_user_id(user_id=user_id)

    mock_redis.hkeys.assert_awaited_once_with(user_key(user_id=user_id))
    mock_redis.delete.assert_has_awaits(
        calls=[unittest.mock.call(token_key) for token_key in token_keys]
        + [unittest.mock.call(user_key(user_id=user_id))]
    )


@pytest.mark.asyncio
async def test_fetch_user_id_from_valid_refresh_token__fetches_user_id_from_redis() -> None:
    user_id = uuid.uuid4()
    refresh_token = secrets.token_urlsafe(identity.services.auth.REFRESH_TOKEN_BYTES)
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

    mock_redis = aioredis.Redis()
    mock_redis.hgetall = unittest.mock.AsyncMock(
        return_value={
            "user_id": str(user_id),
            "expiration": str(int(expiration.timestamp())),
        }
    )

    cache = identity.cache.Cache(redis=mock_redis)

    result = await cache.fetch_user_id_from_valid_refresh_token(
        refresh_token=refresh_token
    )

    mock_redis.hgetall.assert_awaited_once_with(token_key(refresh_token))
    assert result == user_id


@pytest.mark.asyncio
async def test_fetch_user_id_from_valid_refresh_token__raises_for_missing_expiration() -> None:
    user_id = uuid.uuid4()
    refresh_token = secrets.token_urlsafe(identity.services.auth.REFRESH_TOKEN_BYTES)

    mock_redis = aioredis.Redis()
    mock_redis.hgetall = unittest.mock.AsyncMock(
        return_value={
            "user_id": str(user_id),
        }
    )

    cache = identity.cache.Cache(redis=mock_redis)

    with pytest.raises(common.datatypes.exception.UnauthorizedException):
        await cache.fetch_user_id_from_valid_refresh_token(refresh_token=refresh_token)


@pytest.mark.asyncio
async def test_fetch_user_id_from_valid_refresh_token__raises_for_expired_token() -> None:
    user_id = uuid.uuid4()
    refresh_token = secrets.token_urlsafe(identity.services.auth.REFRESH_TOKEN_BYTES)
    expiration = datetime.datetime.utcnow() - datetime.timedelta(hours=1)

    mock_redis = aioredis.Redis()
    mock_redis.hgetall = unittest.mock.AsyncMock(
        return_value={
            "user_id": str(user_id),
            "expiration": str(int(expiration.timestamp())),
        }
    )

    cache = identity.cache.Cache(redis=mock_redis)

    with pytest.raises(common.datatypes.exception.UnauthorizedException):
        await cache.fetch_user_id_from_valid_refresh_token(refresh_token=refresh_token)
