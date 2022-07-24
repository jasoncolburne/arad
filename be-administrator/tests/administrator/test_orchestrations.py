import unittest.mock
import uuid

import pytest
import sqlmodel

import common.services.user
import common.datatypes.response

import administrator.orchestrations
import administrator.datatypes.response


@pytest.mark.asyncio
async def test_arad_users_returns_service_results():
    mock_result = administrator.datatypes.response.UsersResponse(
        users=[
            common.datatypes.response.User(
                id=uuid.uuid4(),
                email="address@arad.org",
                roles=[],
            )
        ],
        count=1,
        page=1,
        pages=1,
    )

    mock_database = sqlmodel.Session()
    mock_user_service = common.services.user.UserService(database=mock_database)
    mock_user_service.page = unittest.mock.AsyncMock(return_value=mock_result)

    result = await administrator.orchestrations.arad_users(
        email_filter="", page=1, database=None, user_service=mock_user_service
    )

    assert result == mock_result
