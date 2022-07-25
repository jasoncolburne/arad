import secrets
import unittest.mock
import uuid

import pytest
import sqlmodel

import common.datatypes.domain
import common.datatypes.exception

import identity.datatypes.response
import identity.repositories.auth
import identity.orchestrations
import identity.services.auth


@pytest.mark.asyncio
async def test_arad_login__returns_service_results():
    fake_email = "address@arad.org"
    fake_refresh_token = secrets.token_urlsafe()
    fake_user = common.datatypes.domain.User(
        id=uuid.uuid4(),
        email=fake_email,
        roles=[common.datatypes.domain.Role.READER],
    )
    fake_passphrase = "terrible passphrase"
    mock_response = identity.datatypes.response.LoginResponse(
        refresh_token=fake_refresh_token,
        user=fake_user,
    )

    mock_database = sqlmodel.Session()
    mock_auth_service = identity.services.auth.AuthService(database=mock_database)
    mock_auth_service.authenticate_user_by_email_and_passphrase = unittest.mock.AsyncMock(
        return_value=fake_user
    )
    mock_auth_service.create_refresh_token = unittest.mock.AsyncMock(
        return_value=fake_refresh_token
    )

    response = await identity.orchestrations.arad_login(
        email=fake_user.email,
        passphrase=fake_passphrase,
        auth_service=mock_auth_service,
        database=None,
    )

    mock_auth_service.authenticate_user_by_email_and_passphrase.assert_awaited_once_with(
        email=fake_user.email, passphrase=fake_passphrase
    )
    mock_auth_service.create_refresh_token.assert_awaited_once_with(user=fake_user)

    assert response == mock_response


@pytest.mark.asyncio
async def test_arad_login__denies_login_according_to_service_response():
    fake_email = "address@arad.org"
    fake_refresh_token = secrets.token_urlsafe()
    fake_user = common.datatypes.domain.User(
        id=uuid.uuid4(),
        email=fake_email,
        roles=[common.datatypes.domain.Role.READER],
    )
    fake_passphrase = "terrible passphrase"

    mock_database = sqlmodel.Session()
    mock_auth_service = identity.services.auth.AuthService(database=mock_database)

    # this assumes knowledge of some potentially unintuitive behaviour of the auth service
    mock_auth_service.authenticate_user_by_email_and_passphrase = unittest.mock.AsyncMock(
        side_effect=common.datatypes.exception.UnauthorizedException()
    )
    mock_auth_service.create_refresh_token = unittest.mock.AsyncMock(
        return_value=fake_refresh_token
    )

    with pytest.raises(common.datatypes.exception.UnauthorizedException):
        await identity.orchestrations.arad_login(
            email=fake_user.email,
            passphrase=fake_passphrase,
            auth_service=mock_auth_service,
            database=None,
        )
