import secrets
import unittest.mock

import pytest
import sqlmodel

import identity.cache
import identity.datatypes.response
import identity.orchestrations
import identity.repositories.auth
import identity.services.auth


@pytest.mark.asyncio
async def test_arad_logout__invokes_service_to_destroy_token():
    fake_refresh_token = secrets.token_urlsafe(
        identity.services.auth.REFRESH_TOKEN_BYTES
    )

    mock_database = sqlmodel.Session()
    mock_redis = unittest.mock.Mock()
    mock_token_cache = identity.cache.Cache(redis=mock_redis)
    mock_auth_service = identity.services.auth.AuthService(
        database=mock_database, token_cache=mock_token_cache
    )
    mock_auth_service.destroy_refresh_token = unittest.mock.AsyncMock()

    response = await identity.orchestrations.arad_logout(
        refresh_token=fake_refresh_token,
        auth_service=mock_auth_service,
        database=None,
    )

    mock_auth_service.destroy_refresh_token.assert_awaited_once_with(
        refresh_token=fake_refresh_token
    )

    assert response == identity.datatypes.response.LogoutResponse(status="ok")
