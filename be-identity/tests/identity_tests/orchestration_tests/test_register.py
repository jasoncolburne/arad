import os
import secrets
import unittest.mock
import uuid

import pytest
import sqlmodel

import common.datatypes.domain

import identity.datatypes.domain
import identity.datatypes.response
import identity.orchestrations
import identity.repositories.auth
import identity.services.auth


@pytest.mark.asyncio
async def test_arad_register__returns_service_results():
    refresh_token = secrets.token_urlsafe(identity.services.auth.REFRESH_TOKEN_BYTES)
    user = identity.datatypes.domain.User(
        id=uuid.uuid4(),
        email="address@arad.org",
        roles=[common.datatypes.domain.Role.READER],
    )
    passphrase = "terrible passphrase"

    fake_response = identity.datatypes.response.RegisterResponse(
        refresh_token=refresh_token,
        user=user,
    )

    mock_database = sqlmodel.Session()
    mock_auth_service = identity.services.auth.AuthService(database=mock_database)
    mock_auth_service.create_user_with_passphrase = unittest.mock.AsyncMock(
        return_value=user
    )
    mock_auth_service.create_refresh_token = unittest.mock.AsyncMock(
        return_value=refresh_token
    )

    response = await identity.orchestrations.arad_register(
        email=user.email,
        passphrase=passphrase,
        auth_service=mock_auth_service,
        database=None,
    )

    mock_auth_service.create_user_with_passphrase.assert_awaited_once_with(
        email=user.email, passphrase=passphrase
    )
    mock_auth_service.create_refresh_token.assert_awaited_once_with(user=user)

    assert response == fake_response


@pytest.mark.asyncio
async def test_arad_register__creates_admin_user_if_admin_email_provided():
    admin_email = "admin@arad.org"
    user_id = uuid.uuid4()

    refresh_token = secrets.token_urlsafe(identity.services.auth.REFRESH_TOKEN_BYTES)
    user = identity.datatypes.domain.User(
        id=user_id,
        email=admin_email,
        roles=[
            common.datatypes.domain.Role.READER,
            common.datatypes.domain.Role.ADMINISTRATOR,
        ],
    )
    passphrase = "terrible passphrase"

    mock_database = sqlmodel.Session()
    mock_auth_service = identity.services.auth.AuthService(database=mock_database)
    mock_auth_service.create_user_with_passphrase = unittest.mock.AsyncMock(
        return_value=user
    )
    mock_auth_service.assign_role_for_user_id = unittest.mock.AsyncMock()
    mock_auth_service.create_refresh_token = unittest.mock.AsyncMock(
        return_value=refresh_token
    )

    os.environ["DEFAULT_ADMIN_EMAIL"] = admin_email

    await identity.orchestrations.arad_register(
        email=user.email,
        passphrase=passphrase,
        auth_service=mock_auth_service,
        database=None,
    )

    del os.environ["DEFAULT_ADMIN_EMAIL"]

    mock_auth_service.assign_role_for_user_id.assert_awaited_once_with(
        user_id=user_id, role=common.datatypes.domain.Role.ADMINISTRATOR
    )