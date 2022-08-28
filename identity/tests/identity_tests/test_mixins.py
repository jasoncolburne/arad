import unittest.mock
import uuid

import pytest
import sqlmodel

import common.datatypes.domain
import database.models

import identity.mixins


class ExercisingClass(identity.mixins.RolesForUserID):
    def __init__(self, _database: sqlmodel.Session):
        self.database = _database


@pytest.mark.asyncio
async def test_roles_for_user_id__fetches_from_database() -> None:
    user_id = uuid.uuid4()

    role_id = uuid.uuid4()
    role_ids = [role_id]

    role = common.datatypes.domain.Role.READER
    roles = [role]
    role_model = database.models.Role(id=role_id, name=role.value)
    role_models = [role_model]

    mock_result = unittest.mock.Mock()
    mock_result.scalars = unittest.mock.Mock(
        side_effect=[
            role_ids,
            role_models,
        ]
    )

    mock_database = sqlmodel.Session()
    mock_database.execute = unittest.mock.AsyncMock(return_value=mock_result)

    exercising_instance = ExercisingClass(_database=mock_database)

    result = await exercising_instance.roles_for_user_id(user_id=user_id)

    assert result == roles
