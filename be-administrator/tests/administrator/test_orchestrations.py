import unittest.mock
import uuid

import pytest
import sqlmodel

import common.datatypes.domain

import administrator.datatypes.response
import administrator.orchestrations
import administrator.repositories.user
import administrator.services.user


@pytest.mark.asyncio
async def test_arad_users_returns_service_results():
    page = 3
    pages = 3
    users = [
        common.datatypes.domain.User(
            id=uuid.uuid4(),
            email="address@arad.org",
            roles=[],
        )
    ]
    mock_result = administrator.datatypes.response.UsersResponse(
        users=users,
        count=len(users),
        page=page,
        pages=pages,
    )

    mock_database = sqlmodel.Session()
    mock_user_service = administrator.services.user.UserService(database=mock_database)
    mock_user_service.page = unittest.mock.AsyncMock(return_value=mock_result)

    result = await administrator.orchestrations.arad_users(
        email_filter="", page=page, database=None, user_service=mock_user_service
    )

    assert result == mock_result
