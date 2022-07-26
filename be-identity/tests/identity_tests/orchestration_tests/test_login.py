# pylint: disable=duplicate-code

import secrets
import unittest.mock
import uuid

import pytest
import sqlmodel

import common.datatypes.domain
import common.datatypes.exception

import identity.cache
import identity.datatypes.domain
import identity.datatypes.response
import identity.orchestrations
import identity.repositories.auth
import identity.services.auth


@pytest.mark.asyncio
async def test_arad_login__returns_service_results():
    email = "address@arad.org"
    refresh_token = secrets.token_urlsafe(identity.services.auth.REFRESH_TOKEN_BYTES)
    user = identity.datatypes.domain.User(
        id=uuid.uuid4(),
        email=email,
        roles=[common.datatypes.domain.Role.READER],
    )
    passphrase = "terrible passphrase"

    fake_response = identity.datatypes.response.LoginResponse(
        refresh_token=refresh_token,
        user=user,
    )

    mock_database = sqlmodel.Session()
    mock_redis = unittest.mock.Mock()
    mock_token_cache = identity.cache.Cache(redis=mock_redis)
    mock_auth_service = identity.services.auth.AuthService(
        database=mock_database, token_cache=mock_token_cache
    )
    mock_auth_service.authenticate_user_by_email_and_passphrase = (
        unittest.mock.AsyncMock(return_value=user)
    )
    mock_auth_service.create_refresh_token = unittest.mock.AsyncMock(
        return_value=refresh_token
    )

    response = await identity.orchestrations.arad_login(
        email=user.email,
        passphrase=passphrase,
        auth_service=mock_auth_service,
        database=None,
    )

    mock_auth_service.authenticate_user_by_email_and_passphrase.assert_awaited_once_with(
        email=user.email, passphrase=passphrase
    )
    mock_auth_service.create_refresh_token.assert_awaited_once_with(user=user)

    assert response == fake_response


@pytest.mark.asyncio
async def test_arad_login__denies_login_according_to_service_response():
    email = "address@arad.org"
    refresh_token = secrets.token_urlsafe(identity.services.auth.REFRESH_TOKEN_BYTES)
    user = identity.datatypes.domain.User(
        id=uuid.uuid4(),
        email=email,
        roles=[common.datatypes.domain.Role.READER],
    )
    passphrase = "terrible passphrase"

    mock_database = sqlmodel.Session()
    mock_redis = unittest.mock.Mock()
    mock_token_cache = identity.cache.Cache(redis=mock_redis)
    mock_auth_service = identity.services.auth.AuthService(
        database=mock_database, token_cache=mock_token_cache
    )

    # this assumes knowledge of some potentially unintuitive behaviour of the auth service
    mock_auth_service.authenticate_user_by_email_and_passphrase = (
        unittest.mock.AsyncMock(
            side_effect=common.datatypes.exception.UnauthorizedException()
        )
    )
    mock_auth_service.create_refresh_token = unittest.mock.AsyncMock(
        return_value=refresh_token
    )

    with pytest.raises(common.datatypes.exception.UnauthorizedException):
        await identity.orchestrations.arad_login(
            email=user.email,
            passphrase=passphrase,
            auth_service=mock_auth_service,
            database=None,
        )
