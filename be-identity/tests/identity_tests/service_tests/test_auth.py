import secrets
import unittest.mock
import uuid

import passlib.context
import pytest
import sqlmodel

import common.datatypes.domain
import common.datatypes.exception

import identity.cache
import identity.datatypes.domain
import identity.repositories.auth
import identity.services.auth


@pytest.mark.asyncio
async def test_create_user_with_passphrase__calls_repository() -> None:
    email = "address@arad.org"
    passphrase = "passphrase"
    hashed_passphrase = "hashed_passphrase"
    user_id = uuid.uuid4()

    expected_user = identity.datatypes.domain.User(
        id=user_id,
        email=email,
        roles=identity.repositories.auth.DEFAULT_USER_ROLES,
    )

    mock_passphrase_context = passlib.context.CryptContext(
        schemes=["argon2"], deprecated="auto"
    )
    mock_token_cache = identity.cache.Cache()
    mock_database = sqlmodel.Session()
    mock_auth_repository = identity.repositories.auth.AuthRepository(
        _database=mock_database
    )

    mock_passphrase_context.hash = unittest.mock.Mock(return_value=hashed_passphrase)
    mock_auth_repository.create_user = unittest.mock.AsyncMock(
        return_value=expected_user
    )

    auth_service = identity.services.auth.AuthService(
        auth_repository=mock_auth_repository,
        passphrase_context=mock_passphrase_context,
        token_cache=mock_token_cache,
    )

    user = await auth_service.create_user_with_passphrase(
        email=email,
        passphrase=passphrase,
    )

    mock_passphrase_context.hash.assert_called_once_with(passphrase)
    mock_auth_repository.create_user.assert_awaited_once_with(
        email=email, hashed_passphrase=hashed_passphrase
    )
    assert user == expected_user


@pytest.mark.asyncio
async def test_authenticate_user_by_email_and_passphrase__calls_repository() -> None:
    email = "address@arad.org"
    passphrase = "passphrase"
    user_id = uuid.uuid4()

    expected_user = identity.datatypes.domain.User(
        id=user_id,
        email=email,
        roles=identity.repositories.auth.DEFAULT_USER_ROLES,
    )

    mock_passphrase_context = passlib.context.CryptContext(
        schemes=["argon2"], deprecated="auto"
    )
    mock_token_cache = identity.cache.Cache()
    mock_database = sqlmodel.Session()
    mock_auth_repository = identity.repositories.auth.AuthRepository(
        _database=mock_database
    )

    mock_auth_repository.verify_user_email_and_passphrase = unittest.mock.AsyncMock(
        return_value=expected_user
    )

    auth_service = identity.services.auth.AuthService(
        auth_repository=mock_auth_repository,
        passphrase_context=mock_passphrase_context,
        token_cache=mock_token_cache,
    )

    user = await auth_service.authenticate_user_by_email_and_passphrase(
        email=email,
        passphrase=passphrase,
    )

    mock_auth_repository.verify_user_email_and_passphrase.assert_awaited_once_with(
        email=email,
        passphrase=passphrase,
        verify=auth_service._verify_passphrase,  # pylint: disable=protected-access
    )
    assert user == expected_user


@pytest.mark.asyncio
async def test_assign_role_for_user_id__calls_repository() -> None:
    user_id = uuid.uuid4()
    role = common.datatypes.domain.Role.REVIEWER

    mock_passphrase_context = passlib.context.CryptContext(
        schemes=["argon2"], deprecated="auto"
    )
    mock_token_cache = identity.cache.Cache()
    mock_database = sqlmodel.Session()
    mock_auth_repository = identity.repositories.auth.AuthRepository(
        _database=mock_database
    )

    mock_auth_repository.assign_role_for_user_id = unittest.mock.AsyncMock()

    auth_service = identity.services.auth.AuthService(
        auth_repository=mock_auth_repository,
        passphrase_context=mock_passphrase_context,
        token_cache=mock_token_cache,
    )

    await auth_service.assign_role_for_user_id(
        user_id=user_id,
        role=role,
    )

    mock_auth_repository.assign_role_for_user_id.assert_awaited_once_with(
        user_id=user_id, role_name=role.value
    )


@pytest.mark.asyncio
async def test_revoke_role_for_user_id__calls_repository() -> None:
    user_id = uuid.uuid4()
    role = common.datatypes.domain.Role.REVIEWER

    mock_passphrase_context = passlib.context.CryptContext(
        schemes=["argon2"], deprecated="auto"
    )
    mock_token_cache = identity.cache.Cache()
    mock_database = sqlmodel.Session()
    mock_auth_repository = identity.repositories.auth.AuthRepository(
        _database=mock_database
    )

    mock_auth_repository.revoke_role_for_user_id = unittest.mock.AsyncMock()

    auth_service = identity.services.auth.AuthService(
        auth_repository=mock_auth_repository,
        passphrase_context=mock_passphrase_context,
        token_cache=mock_token_cache,
    )

    await auth_service.revoke_role_for_user_id(
        user_id=user_id,
        role=role,
    )

    mock_auth_repository.revoke_role_for_user_id.assert_awaited_once_with(
        user_id=user_id, role_name=role.value
    )


@pytest.mark.asyncio
async def test_all_roles__calls_repository() -> None:
    all_roles = [
        common.datatypes.domain.Role.READER,
        common.datatypes.domain.Role.REVIEWER,
        common.datatypes.domain.Role.ADMINISTRATOR,
    ]

    mock_passphrase_context = passlib.context.CryptContext(
        schemes=["argon2"], deprecated="auto"
    )
    mock_token_cache = identity.cache.Cache()
    mock_database = sqlmodel.Session()
    mock_auth_repository = identity.repositories.auth.AuthRepository(
        _database=mock_database
    )

    mock_auth_repository.all_roles = unittest.mock.AsyncMock(return_value=all_roles)

    auth_service = identity.services.auth.AuthService(
        auth_repository=mock_auth_repository,
        passphrase_context=mock_passphrase_context,
        token_cache=mock_token_cache,
    )

    roles = await auth_service.all_roles()

    assert roles == all_roles


@pytest.mark.asyncio
async def test_verify_role_and_create_access_token__creates_token() -> None:
    user_id = uuid.uuid4()
    access_token = "access_token"
    role = common.datatypes.domain.Role.REVIEWER
    roles = [
        common.datatypes.domain.Role.READER,
        common.datatypes.domain.Role.REVIEWER,
    ]

    mock_passphrase_context = passlib.context.CryptContext(
        schemes=["argon2"], deprecated="auto"
    )
    mock_token_cache = identity.cache.Cache()
    mock_database = sqlmodel.Session()
    mock_auth_repository = identity.repositories.auth.AuthRepository(
        _database=mock_database
    )

    mock_auth_repository.roles_for_user_id = unittest.mock.AsyncMock(return_value=roles)

    auth_service = identity.services.auth.AuthService(
        auth_repository=mock_auth_repository,
        passphrase_context=mock_passphrase_context,
        token_cache=mock_token_cache,
    )

    with unittest.mock.patch("identity.services.auth.jwt.encode") as jwt_encode:
        jwt_encode.return_value = access_token
        result = await auth_service.verify_role_and_create_access_token(
            user_id=user_id,
            scope=role,
        )
        jwt_encode.assert_called_once()  # it's difficult to construct the parameters without duplicating the code

    mock_auth_repository.roles_for_user_id.assert_awaited_once_with(user_id=user_id)

    assert result == access_token


@pytest.mark.asyncio
async def test_verify_role_and_create_access_token__raises_when_role_requirement_unmet() -> None:
    user_id = uuid.uuid4()
    role = common.datatypes.domain.Role.ADMINISTRATOR
    roles = [
        common.datatypes.domain.Role.READER,
    ]

    mock_passphrase_context = passlib.context.CryptContext(
        schemes=["argon2"], deprecated="auto"
    )
    mock_token_cache = identity.cache.Cache()
    mock_database = sqlmodel.Session()
    mock_auth_repository = identity.repositories.auth.AuthRepository(
        _database=mock_database
    )

    mock_auth_repository.roles_for_user_id = unittest.mock.AsyncMock(return_value=roles)

    auth_service = identity.services.auth.AuthService(
        auth_repository=mock_auth_repository,
        passphrase_context=mock_passphrase_context,
        token_cache=mock_token_cache,
    )

    with pytest.raises(common.datatypes.exception.UnauthorizedException):
        await auth_service.verify_role_and_create_access_token(
            user_id=user_id,
            scope=role,
        )


@pytest.mark.asyncio
async def test_create_refresh_token__creates_and_stores_token() -> None:
    user_id = uuid.uuid4()
    email = "address@arad.org"
    user = identity.datatypes.domain.User(
        id=user_id,
        email=email,
        roles=[],
    )
    refresh_token = secrets.token_urlsafe(identity.services.auth.REFRESH_TOKEN_BYTES)

    mock_passphrase_context = passlib.context.CryptContext(
        schemes=["argon2"], deprecated="auto"
    )
    mock_token_cache = identity.cache.Cache()
    mock_database = sqlmodel.Session()
    mock_auth_repository = identity.repositories.auth.AuthRepository(
        _database=mock_database
    )

    mock_token_cache.store_refresh_token = unittest.mock.AsyncMock()

    auth_service = identity.services.auth.AuthService(
        auth_repository=mock_auth_repository,
        passphrase_context=mock_passphrase_context,
        token_cache=mock_token_cache,
    )

    with unittest.mock.patch(
        "identity.services.auth.secrets.token_urlsafe"
    ) as token_generator:
        token_generator.return_value = refresh_token
        result = await auth_service.create_refresh_token(user=user)
        token_generator.assert_called_once_with(
            identity.services.auth.REFRESH_TOKEN_BYTES
        )

    mock_token_cache.store_refresh_token.assert_awaited_once()

    assert result == refresh_token


@pytest.mark.asyncio
async def test_destroy_refresh_token__purges_cache() -> None:
    refresh_token = secrets.token_urlsafe(identity.services.auth.REFRESH_TOKEN_BYTES)

    mock_passphrase_context = passlib.context.CryptContext(
        schemes=["argon2"], deprecated="auto"
    )
    mock_token_cache = identity.cache.Cache()
    mock_database = sqlmodel.Session()
    mock_auth_repository = identity.repositories.auth.AuthRepository(
        _database=mock_database
    )

    mock_token_cache.purge_refresh_token = unittest.mock.AsyncMock()

    auth_service = identity.services.auth.AuthService(
        auth_repository=mock_auth_repository,
        passphrase_context=mock_passphrase_context,
        token_cache=mock_token_cache,
    )

    await auth_service.destroy_refresh_token(refresh_token=refresh_token)

    mock_token_cache.purge_refresh_token.assert_awaited_once_with(
        refresh_token=refresh_token
    )


@pytest.mark.asyncio
async def test_destroy_all_refresh_tokens_for_user_id__purges_cache() -> None:
    user_id = uuid.uuid4()

    mock_passphrase_context = passlib.context.CryptContext(
        schemes=["argon2"], deprecated="auto"
    )
    mock_token_cache = identity.cache.Cache()
    mock_database = sqlmodel.Session()
    mock_auth_repository = identity.repositories.auth.AuthRepository(
        _database=mock_database
    )

    mock_token_cache.purge_all_refresh_tokens_for_user_id = unittest.mock.AsyncMock()

    auth_service = identity.services.auth.AuthService(
        auth_repository=mock_auth_repository,
        passphrase_context=mock_passphrase_context,
        token_cache=mock_token_cache,
    )

    await auth_service.destroy_all_refresh_tokens_for_user_id(user_id=user_id)

    mock_token_cache.purge_all_refresh_tokens_for_user_id.assert_awaited_once_with(
        user_id=user_id
    )


@pytest.mark.asyncio
async def test_verify_and_extract_user_id_from_refresh_token__extracts_user_id() -> None:
    user_id = uuid.uuid4()
    refresh_token = secrets.token_urlsafe(identity.services.auth.REFRESH_TOKEN_BYTES)

    mock_passphrase_context = passlib.context.CryptContext(
        schemes=["argon2"], deprecated="auto"
    )
    mock_token_cache = identity.cache.Cache()
    mock_database = sqlmodel.Session()
    mock_auth_repository = identity.repositories.auth.AuthRepository(
        _database=mock_database
    )

    mock_token_cache.fetch_user_id_from_valid_refresh_token = unittest.mock.AsyncMock(
        return_value=user_id
    )

    auth_service = identity.services.auth.AuthService(
        auth_repository=mock_auth_repository,
        passphrase_context=mock_passphrase_context,
        token_cache=mock_token_cache,
    )

    result = await auth_service.verify_and_extract_user_id_from_refresh_token(
        refresh_token=refresh_token
    )

    mock_token_cache.fetch_user_id_from_valid_refresh_token.assert_awaited_once_with(
        refresh_token=refresh_token
    )

    assert result == user_id
