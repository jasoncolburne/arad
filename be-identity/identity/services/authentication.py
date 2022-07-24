from datetime import datetime, timedelta
from secrets import token_urlsafe
from typing import Any
from uuid import UUID
import os

from ecdsa import SigningKey
from jose import jwt
from passlib.context import CryptContext
from sqlmodel import Session

from common.repositories.role import RoleRepository
from common.repositories.user import UserRepository
from common.datatypes.exception import UnauthorizedException
from common.datatypes.response import User as UserType, Role

from identity.cache import Cache, REFRESH_TOKEN_EXPIRATION_DAYS


ACCESS_TOKEN_EXPIRATION_MINUTES = 10
ACCESS_TOKEN_ALGORITHM = "ES256"
ACCESS_TOKEN_PRIVATE_KEY_PEM = os.environ.get("ACCESS_TOKEN_PRIVATE_KEY_PEM")
ACCESS_TOKEN_PRIVATE_KEY = SigningKey.from_pem(ACCESS_TOKEN_PRIVATE_KEY_PEM)


# never remove any used schemes, or existing users won't be able to log in
global_passphrase_context = CryptContext(schemes=["argon2"], deprecated="auto")
global_token_cache = Cache()


class AuthenticationService:
    # one of database or user_repository must be defined
    def __init__(  # pylint: disable=too-many-arguments
        self,
        database: Session | None = None,
        user_repository: UserRepository | None = None,
        role_repository: RoleRepository | None = None,
        passphrase_context: CryptContext = global_passphrase_context,
        token_cache: Cache = global_token_cache,
    ):
        self.passphrase_context = passphrase_context
        self.token_cache = token_cache

        # pylint: disable=duplicate-code
        if user_repository is not None:
            self.user_repository = user_repository
        elif database is not None:
            self.user_repository = UserRepository(database=database)
        else:
            raise Exception()

        # pylint: disable=duplicate-code
        if role_repository is not None:
            self.role_repository = role_repository
        elif database is not None:
            self.role_repository = RoleRepository(database=database)
        else:
            raise Exception()

    async def create_user_with_passphrase(
        self, email: str, passphrase: str
    ) -> UserType:
        hashed_passphrase = self._hash_passphrase(passphrase=passphrase)
        user = await self.user_repository.create(
            email=email, hashed_passphrase=hashed_passphrase
        )
        return UserType(id=user.id, email=user.email)

    async def authenticate_by_passphrase(self, email: str, passphrase: str) -> UserType:
        user = await self.user_repository.get_by_email(email=email)
        if not self._verify_passphrase(passphrase, user.hashed_passphrase):
            raise UnauthorizedException()

        return UserType(id=user.id, email=user.email)

    async def create_access_token(self, user_id: UUID, scope: Role) -> str:
        valid_roles = await self.role_repository.all_for_user_id(user_id=user_id)
        if scope.value not in [role.name for role in valid_roles]:
            raise UnauthorizedException()

        payload: dict[str, Any] = {"sub": str(user_id), "scope": scope.value}
        expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)
        payload.update({"exp": expires.timestamp()})
        encoded_jwt = jwt.encode(
            payload, ACCESS_TOKEN_PRIVATE_KEY, algorithm=ACCESS_TOKEN_ALGORITHM
        )

        return encoded_jwt

    async def create_refresh_token(self, user: UserType) -> str:
        refresh_token = token_urlsafe(48)

        await self.token_cache.store_refresh_token(
            refresh_token=refresh_token,
            user_id=user.id,
            expiration=(
                datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRATION_DAYS)
            ),
        )

        return refresh_token

    async def destroy_refresh_token(self, refresh_token: str) -> None:
        await self.token_cache.purge_refresh_token(refresh_token=refresh_token)

    async def destroy_all_refresh_tokens_for_user_id(self, user_id: UUID) -> None:
        await self.token_cache.purge_all_refresh_tokens_for_user_id(user_id=user_id)

    async def verify_and_extract_uuid_from_refresh_token(
        self, refresh_token: str
    ) -> UUID:
        return await self.token_cache.fetch_user_id_from_valid_refresh_token(
            refresh_token=refresh_token
        )

    def _hash_passphrase(self, passphrase: str) -> str:
        return self.passphrase_context.hash(passphrase)

    def _verify_passphrase(self, passphrase: str, hashed_passphrase: str) -> bool:
        return self.passphrase_context.verify(passphrase, hashed_passphrase)
