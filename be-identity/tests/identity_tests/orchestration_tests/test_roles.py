import unittest.mock

import pytest
import sqlmodel

import common.datatypes.domain

import identity.datatypes.response
import identity.orchestrations
import identity.repositories.auth
import identity.services.auth


@pytest.mark.asyncio
async def test_arad_roles__returns_all_roles():
    all_roles = [
        common.datatypes.domain.Role.READER,
        common.datatypes.domain.Role.REVIEWER,
        common.datatypes.domain.Role.ADMINISTRATOR,
    ]

    mock_database = sqlmodel.Session()
    mock_auth_service = identity.services.auth.AuthService(database=mock_database)
    mock_auth_service.all_roles = unittest.mock.AsyncMock(return_value=all_roles)

    expected_response = identity.datatypes.response.RolesResponse(roles=all_roles)

    response = await identity.orchestrations.arad_roles(
        auth_service=mock_auth_service,
        database=None,
    )

    assert response == expected_response
