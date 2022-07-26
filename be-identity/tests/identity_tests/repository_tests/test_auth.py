import unittest.mock
import uuid

import pytest
import sqlmodel

import common.datatypes.domain
import common.datatypes.exception
import database.models

import identity.datatypes.domain
import identity.repositories.auth


fake_role_id_cache = {
    common.datatypes.domain.Role.READER.value: uuid.uuid4(),
    common.datatypes.domain.Role.REVIEWER.value: uuid.uuid4(),
    common.datatypes.domain.Role.ADMINISTRATOR.value: uuid.uuid4(),
}


@pytest.mark.asyncio
async def test_all_roles__returns_roles_from_cache() -> None:
    expected_roles = [common.datatypes.domain.Role(name) for name in fake_role_id_cache]
    mock_database = sqlmodel.Session()
    auth_repository = identity.repositories.auth.AuthRepository(_database=mock_database)

    identity.repositories.auth.global_role_id_cache = fake_role_id_cache
    result = await auth_repository.all_roles()
    identity.repositories.auth.global_role_id_cache = {}

    assert result == expected_roles


@pytest.mark.asyncio
async def test_create_user__writes_user_and_default_roles_to_database() -> None:
    user_id = uuid.uuid4()
    email = "address@domain.org"
    hashed_passphrase = "hashed_passphrase"
    user_model = database.models.User(
        id=user_id,
        email=email,
        hashed_passphrase=hashed_passphrase,
    )

    mock_database = sqlmodel.Session()
    auth_repository = identity.repositories.auth.AuthRepository(_database=mock_database)

    mock_database.add = unittest.mock.Mock()
    mock_database.commit = unittest.mock.AsyncMock()

    role_ids = [
        fake_role_id_cache[role.value]
        for role in identity.repositories.auth.DEFAULT_USER_ROLES
    ]

    identity.repositories.auth.global_role_id_cache = fake_role_id_cache
    with unittest.mock.patch(
        "identity.repositories.auth.database.models.User"
    ) as user_class:
        user_class.return_value = user_model
        result = await auth_repository.create_user(
            email=email, hashed_passphrase=hashed_passphrase
        )
    identity.repositories.auth.global_role_id_cache = {}

    mock_database.add.assert_has_calls(
        calls=[unittest.mock.call(user_model)]
        + [
            unittest.mock.call(user_role_model)
            for user_role_model in [
                database.models.UserRole(user_id=user_id, role_id=role_id)
                for role_id in role_ids
            ]
        ],
    )

    mock_database.commit.assert_has_awaits(
        calls=[unittest.mock.call()] * (len(role_ids) + 1)
    )

    assert result == identity.datatypes.domain.User(
        id=user_id, email=email, roles=identity.repositories.auth.DEFAULT_USER_ROLES
    )


@pytest.mark.asyncio
async def test_verify_user_email_and_passphrase__returns_user() -> None:
    user_id = uuid.uuid4()
    email = "address@domain.org"
    passphrase = "passphrase"
    hashed_passphrase = "hashed_passphrase"
    roles = [
        common.datatypes.domain.Role(role.name)
        for role in [
            common.datatypes.domain.Role.READER,
            common.datatypes.domain.Role.REVIEWER,
        ]
    ]

    def fake_verify(_passphrase: str, _hashed_passphrase: str):
        return True

    mock_database = sqlmodel.Session()
    auth_repository = identity.repositories.auth.AuthRepository(_database=mock_database)

    mock_result = unittest.mock.Mock()
    mock_scalars = unittest.mock.Mock()
    mock_result.scalars = unittest.mock.Mock(return_value=mock_scalars)
    mock_scalars.one = unittest.mock.Mock(
        return_value=database.models.User(
            id=user_id, email=email, hashed_passphrase=hashed_passphrase
        )
    )
    mock_database.execute = unittest.mock.AsyncMock(return_value=mock_result)
    auth_repository.roles_for_user_id = unittest.mock.AsyncMock(return_value=roles)

    identity.repositories.auth.global_role_id_cache = fake_role_id_cache
    result = await auth_repository.verify_user_email_and_passphrase(
        email=email, passphrase=passphrase, verify=fake_verify
    )
    identity.repositories.auth.global_role_id_cache = {}

    mock_database.execute.assert_awaited_once()
    auth_repository.roles_for_user_id.assert_awaited_once_with(user_id=user_id)

    assert result == identity.datatypes.domain.User(
        id=user_id, email=email, roles=roles
    )


@pytest.mark.asyncio
async def test_verify_user_email_and_passphrase__raises_on_verification_failure() -> None:
    user_id = uuid.uuid4()
    email = "address@domain.org"
    passphrase = "passphrase"
    hashed_passphrase = "hashed_passphrase"
    roles = [
        common.datatypes.domain.Role(role.name)
        for role in [
            common.datatypes.domain.Role.READER,
            common.datatypes.domain.Role.REVIEWER,
        ]
    ]

    def fake_verify(_passphrase: str, _hashed_passphrase: str):
        return False

    mock_database = sqlmodel.Session()
    auth_repository = identity.repositories.auth.AuthRepository(_database=mock_database)

    mock_result = unittest.mock.Mock()
    mock_scalars = unittest.mock.Mock()
    mock_result.scalars = unittest.mock.Mock(return_value=mock_scalars)
    mock_scalars.one = unittest.mock.Mock(
        return_value=database.models.User(
            id=user_id, email=email, hashed_passphrase=hashed_passphrase
        )
    )
    mock_database.execute = unittest.mock.AsyncMock(return_value=mock_result)
    auth_repository.roles_for_user_id = unittest.mock.AsyncMock(return_value=roles)

    identity.repositories.auth.global_role_id_cache = fake_role_id_cache
    with pytest.raises(common.datatypes.exception.UnauthorizedException):
        await auth_repository.verify_user_email_and_passphrase(
            email=email, passphrase=passphrase, verify=fake_verify
        )
    identity.repositories.auth.global_role_id_cache = {}
