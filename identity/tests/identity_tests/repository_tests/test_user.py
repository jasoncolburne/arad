# pylint: disable=duplicate-code

import unittest.mock
import uuid

import pytest

import sqlmodel

import common.datatypes.domain
import database.models

import identity.datatypes.domain
import identity.repositories.user


@pytest.mark.asyncio
async def test_page__fetches_from_database() -> None:
    email_filter = "email_filter"
    page_number = 9
    user_id = uuid.uuid4()
    email = "email_filter_superset@domain.org"
    roles = [common.datatypes.domain.Role.READER]
    user_model = database.models.User(
        id=user_id, email=email, hashed_passphrase="hashed_passphrase"
    )
    user_models = [user_model]

    user = identity.datatypes.domain.User(id=user_id, email=email, roles=roles)
    user_page = identity.datatypes.domain.UserPage(
        users=[user],
        count=1,
        page=page_number,
        pages=page_number,
    )

    mock_database = sqlmodel.Session()

    mock_result = unittest.mock.Mock()
    mock_scalars = unittest.mock.Mock()
    mock_result.scalars = unittest.mock.Mock(return_value=mock_scalars)
    mock_scalars.all = unittest.mock.Mock(return_value=user_models)

    mock_database.execute = unittest.mock.AsyncMock(return_value=mock_result)
    mock_database.scalar = unittest.mock.AsyncMock(
        return_value=identity.repositories.user.PAGE_SIZE_USER * (page_number - 1) + 1
    )

    user_repository = identity.repositories.user.UserRepository(_database=mock_database)

    with unittest.mock.patch(
        "identity.repositories.user.UserRepository.roles_for_user_id"
    ) as roles_for_id:
        roles_for_id.return_value = roles
        result = await user_repository.page(
            email_filter=email_filter, number=page_number
        )
        roles_for_id.assert_awaited_once_with(user_id=user_id)

    assert result == user_page
