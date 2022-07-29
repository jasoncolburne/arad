# pylint: disable=duplicate-code

import unittest.mock
import uuid

import pytest

import sqlmodel

import common.datatypes.domain

import identity.datatypes.domain
import identity.repositories.user
import identity.services.user


@pytest.mark.asyncio
async def test_page__calls_repository() -> None:
    email_filter = "email_filter"
    page_number = 9
    user_id = uuid.uuid4()
    email = "email_filter_superset@domain.org"
    roles = [common.datatypes.domain.Role.READER]
    user = identity.datatypes.domain.User(id=user_id, email=email, roles=roles)
    user_page = identity.datatypes.domain.UserPage(
        users=[user],
        count=1,
        page=page_number,
        pages=page_number,
    )

    mock_database = sqlmodel.Session()
    mock_user_repository = identity.repositories.user.UserRepository(
        _database=mock_database
    )
    user_service = identity.services.user.UserService(
        user_repository=mock_user_repository
    )

    mock_user_repository.page = unittest.mock.AsyncMock(return_value=user_page)

    result = await user_service.page(email_filter=email_filter, number=page_number)

    assert result == user_page
