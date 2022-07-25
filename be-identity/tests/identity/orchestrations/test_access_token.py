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
async def test_arad_arad_access_token__creates_access_token():
    refresh_token = secrets.token_urlsafe(identity.services.auth.REFRESH_TOKEN_BYTES)
    user_id = uuid.uuid4()
    scope = common.datatypes.domain.Role.ADMINISTRATOR
    access_token = "xxx.xxx"


    mock_database = sqlmodel.Session()
    mock_auth_service = identity.services.auth.AuthService(database=mock_database)
    mock_auth_service.verify_and_extract_user_id_from_refresh_token = unittest.mock.AsyncMock(
        return_value=user_id
    )
    mock_auth_service.verify_role_and_create_access_token = unittest.mock.AsyncMock(
        return_value=access_token
    )

    response = await identity.orchestrations.arad_access_token(
        refresh_token=refresh_token,
        scope=scope,
        auth_service=mock_auth_service,
        database=None,
    )

    mock_auth_service.verify_and_extract_user_id_from_refresh_token.assert_awaited_once_with(
        refresh_token=refresh_token
    )
    mock_auth_service.verify_role_and_create_access_token.assert_awaited_once_with(
        user_id=user_id,
        scope=scope,
    )

    assert response == identity.datatypes.response.TokenResponse(access_token=access_token)
