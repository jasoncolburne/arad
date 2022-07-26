import unittest.mock
import uuid

import pytest
import sqlmodel

import common.datatypes.domain

import identity.cache
import identity.datatypes.request
import identity.datatypes.response
import identity.orchestrations
import identity.repositories.auth
import identity.services.auth


@pytest.mark.asyncio
async def test_arad_modify_role_assignment__assigns_role_and_logs_user_out():
    user_id = uuid.uuid4()
    role = common.datatypes.domain.Role.REVIEWER
    action = identity.datatypes.request.RoleAction.ASSIGN

    mock_database = sqlmodel.Session()
    mock_auth_repository = identity.repositories.auth.AuthRepository(
        _database=mock_database
    )
    mock_redis = unittest.mock.Mock()
    mock_token_cache = identity.cache.Cache(redis=mock_redis)
    mock_auth_service = identity.services.auth.AuthService(
        auth_repository=mock_auth_repository,
        token_cache=mock_token_cache,
    )
    mock_auth_service.assign_role_for_user_id = unittest.mock.AsyncMock()
    mock_auth_service.destroy_all_refresh_tokens_for_user_id = unittest.mock.AsyncMock()

    expected_response = identity.datatypes.response.RoleResponse(role=role)

    response = await identity.orchestrations.arad_modify_role_assignment(
        user_id=user_id,
        role=role,
        action=action,
        auth_service=mock_auth_service,
        database=None,
    )

    mock_auth_service.assign_role_for_user_id.assert_awaited_once_with(
        user_id=user_id,
        role=role,
    )

    assert response == expected_response


@pytest.mark.asyncio
async def test_arad_modify_role_assignment__revokes_role_and_logs_user_out():
    user_id = uuid.uuid4()
    role = common.datatypes.domain.Role.REVIEWER
    action = identity.datatypes.request.RoleAction.REVOKE

    mock_database = sqlmodel.Session()
    mock_auth_repository = identity.repositories.auth.AuthRepository(
        _database=mock_database
    )
    mock_redis = unittest.mock.Mock()
    mock_token_cache = identity.cache.Cache(redis=mock_redis)
    mock_auth_service = identity.services.auth.AuthService(
        auth_repository=mock_auth_repository,
        token_cache=mock_token_cache,
    )
    mock_auth_service.revoke_role_for_user_id = unittest.mock.AsyncMock()
    mock_auth_service.destroy_all_refresh_tokens_for_user_id = unittest.mock.AsyncMock()

    expected_response = identity.datatypes.response.RoleResponse(role=role)

    response = await identity.orchestrations.arad_modify_role_assignment(
        user_id=user_id,
        role=role,
        action=action,
        auth_service=mock_auth_service,
        database=None,
    )

    mock_auth_service.revoke_role_for_user_id.assert_awaited_once_with(
        user_id=user_id,
        role=role,
    )

    assert response == expected_response
