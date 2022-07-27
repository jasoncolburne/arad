import datetime
import secrets
import os
import typing
import uuid

import ecdsa
import passlib.context
import sqlmodel
from jose import jwt

import common.datatypes.exception
import common.datatypes.domain

import identity.cache
import identity.datatypes.domain
import identity.repositories.auth


ACCESS_TOKEN_EXPIRATION_MINUTES = 10
ACCESS_TOKEN_ALGORITHM = "ES256"
ACCESS_TOKEN_PRIVATE_KEY_PEM = os.environ[
    "ACCESS_TOKEN_PRIVATE_KEY_PEM"
]  # we actually do want to throw if unset
ACCESS_TOKEN_PRIVATE_KEY = ecdsa.SigningKey.from_pem(ACCESS_TOKEN_PRIVATE_KEY_PEM)

REFRESH_TOKEN_BYTES = 48


# never remove any used schemes, or existing users won't be able to log in
global_passphrase_context = passlib.context.CryptContext(
    schemes=["argon2"], deprecated="auto"
)


class AuthService:
    def __init__(
        self,
        database: sqlmodel.Session | None = None,
        auth_repository: identity.repositories.auth.AuthRepository | None = None,
        passphrase_context: passlib.context.CryptContext = global_passphrase_context,
        token_cache: identity.cache.Cache | None = None,
    ):
        self.passphrase_context = passphrase_context

        if token_cache is not None:
            self.token_cache = token_cache
        else:
            self.token_cache = identity.cache.global_cache_manager.get_cache()

        if auth_repository is not None:
            self.auth_repository = auth_repository
        elif database is not None:
            self.auth_repository = identity.repositories.auth.AuthRepository(
                _database=database
            )
        else:
            raise Exception()

    async def create_user_with_passphrase(
        self, email: str, passphrase: str
    ) -> identity.datatypes.domain.User:
        hashed_passphrase = self._hash_passphrase(passphrase=passphrase)
        return await self.auth_repository.create_user(
            email=email, hashed_passphrase=hashed_passphrase
        )

    async def authenticate_user_by_email_and_passphrase(
        self, email: str, passphrase: str
    ) -> identity.datatypes.domain.User:
        return await self.auth_repository.verify_user_email_and_passphrase(
            email=email,
            passphrase=passphrase,
            verify=self._verify_passphrase,
        )

    async def assign_role_for_user_id(
        self, user_id: uuid.UUID, role: common.datatypes.domain.Role
    ) -> None:
        await self.auth_repository.assign_role_for_user_id(
            user_id=user_id, role_name=role.value
        )

    async def revoke_role_for_user_id(
        self,
        user_id: uuid.UUID,
        role: common.datatypes.domain.Role,
    ) -> None:
        await self.auth_repository.revoke_role_for_user_id(
            user_id=user_id, role_name=role.value
        )

    async def all_roles(self) -> list[common.datatypes.domain.Role]:
        return await self.auth_repository.all_roles()

    async def verify_role_and_create_access_token(
        self, user_id: uuid.UUID, scope: common.datatypes.domain.Role
    ) -> str:
        valid_roles = await self.auth_repository.roles_for_user_id(user_id=user_id)
        if scope.value not in [role.name for role in valid_roles]:
            raise common.datatypes.exception.UnauthorizedException()

        token: dict[str, typing.Any] = {"sub": str(user_id), "scope": scope.value}
        expires = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=ACCESS_TOKEN_EXPIRATION_MINUTES
        )
        token.update({"exp": expires.timestamp()})
        json_web_token = jwt.encode(
            token, ACCESS_TOKEN_PRIVATE_KEY, algorithm=ACCESS_TOKEN_ALGORITHM
        )

        return json_web_token

    async def create_refresh_token(self, user_id: uuid.UUID) -> str:
        refresh_token = secrets.token_urlsafe(REFRESH_TOKEN_BYTES)

        await self.token_cache.store_refresh_token(
            refresh_token=refresh_token,
            user_id=user_id,
            expiration=(
                datetime.datetime.utcnow()
                + datetime.timedelta(days=identity.cache.REFRESH_TOKEN_EXPIRATION_DAYS)
            ),
        )

        return refresh_token

    async def destroy_refresh_token(self, refresh_token: str) -> None:
        await self.token_cache.purge_refresh_token(refresh_token=refresh_token)

    async def destroy_all_refresh_tokens_for_user_id(self, user_id: uuid.UUID) -> None:
        await self.token_cache.purge_all_refresh_tokens_for_user_id(user_id=user_id)

    async def verify_and_extract_user_id_from_refresh_token(
        self, refresh_token: str
    ) -> uuid.UUID:
        return await self.token_cache.fetch_user_id_from_valid_refresh_token(
            refresh_token=refresh_token
        )

    def _hash_passphrase(self, passphrase: str) -> str:
        return self.passphrase_context.hash(passphrase)

    def _verify_passphrase(self, passphrase: str, hashed_passphrase: str) -> bool:
        return self.passphrase_context.verify(passphrase, hashed_passphrase)
