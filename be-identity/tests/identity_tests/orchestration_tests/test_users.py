import unittest.mock
import uuid

import pytest
import sqlmodel

import identity.datatypes.domain
import identity.datatypes.response
import identity.orchestrations
import identity.repositories.user
import identity.services.user


@pytest.mark.asyncio
async def test_arad_users__returns_service_results():
    page = 3
    pages = 3
    users = [
        identity.datatypes.domain.User(
            id=uuid.uuid4(),
            email="address@domain.org",
            roles=[],
        )
    ]
    mock_response = identity.datatypes.response.UsersResponse(
        users=users,
        count=len(users),
        page=page,
        pages=pages,
    )

    mock_database = sqlmodel.Session()
    mock_user_service = identity.services.user.UserService(database=mock_database)
    mock_user_service.page = unittest.mock.AsyncMock(return_value=mock_response)

    response = await identity.orchestrations.arad_users(
        email_filter="", page=page, database=None, user_service=mock_user_service
    )

    mock_user_service.page.assert_awaited_once_with(email_filter="", number=page)

    assert response == mock_response
