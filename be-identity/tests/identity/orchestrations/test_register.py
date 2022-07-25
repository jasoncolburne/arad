import os
import secrets
import unittest.mock
import uuid

import pytest
import sqlmodel

import common.datatypes.domain

import identity.datatypes.response
import identity.repositories.auth
import identity.orchestrations
import identity.services.auth


@pytest.mark.asyncio
async def test_arad_register__returns_service_results():
    fake_refresh_token = secrets.token_urlsafe()
    fake_user = common.datatypes.domain.User(
        id=uuid.uuid4(),
        email="address@arad.org",
        roles=[common.datatypes.domain.Role.READER],
    )
    fake_passphrase = "terrible passphrase"
    mock_response = identity.datatypes.response.RegisterResponse(
        refresh_token=fake_refresh_token,
        user=fake_user,
    )

    mock_database = sqlmodel.Session()
    mock_auth_service = identity.services.auth.AuthService(database=mock_database)
    mock_auth_service.create_user_with_passphrase = unittest.mock.AsyncMock(
        return_value=fake_user
    )
    mock_auth_service.create_refresh_token = unittest.mock.AsyncMock(
        return_value=fake_refresh_token
    )

    response = await identity.orchestrations.arad_register(
        email=fake_user.email,
        passphrase=fake_passphrase,
        auth_service=mock_auth_service,
        database=None,
    )

    mock_auth_service.create_user_with_passphrase.assert_awaited_once_with(
        email=fake_user.email, passphrase=fake_passphrase
    )
    mock_auth_service.create_refresh_token.assert_awaited_once_with(user=fake_user)

    assert response == mock_response


@pytest.mark.asyncio
async def test_arad_register__creates_admin_user_if_admin_email_provided():
    admin_email = "admin@arad.org"
    user_id = uuid.uuid4()

    fake_refresh_token = secrets.token_urlsafe()
    fake_user = common.datatypes.domain.User(
        id=user_id,
        email=admin_email,
        roles=[common.datatypes.domain.Role.READER, common.datatypes.domain.Role.ADMINISTRATOR],
    )
    fake_passphrase = "terrible passphrase"

    mock_database = sqlmodel.Session()
    mock_auth_service = identity.services.auth.AuthService(database=mock_database)
    mock_auth_service.create_user_with_passphrase = unittest.mock.AsyncMock(
        return_value=fake_user
    )
    mock_auth_service.assign_role_for_user_id = unittest.mock.AsyncMock()
    mock_auth_service.create_refresh_token = unittest.mock.AsyncMock(
        return_value=fake_refresh_token
    )

    os.environ["DEFAULT_ADMIN_EMAIL"] = admin_email

    await identity.orchestrations.arad_register(
        email=fake_user.email,
        passphrase=fake_passphrase,
        auth_service=mock_auth_service,
        database=None,
    )

    del os.environ["DEFAULT_ADMIN_EMAIL"]

    mock_auth_service.assign_role_for_user_id.assert_awaited_once_with(
        user_id=user_id, role=common.datatypes.domain.Role.ADMINISTRATOR
    )
