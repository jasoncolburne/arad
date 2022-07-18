from datetime import datetime, timedelta
from secrets import token_urlsafe
from uuid import UUID
import os

from ecdsa import SigningKey
from jose import jwt
from passlib.context import CryptContext
from sqlmodel import Session

from common.repositories.user import UserRepository
from common.types.exception import UnauthorizedException
from common.types.response import User as UserType, Role

from identity.cache import Cache


REFRESH_TOKEN_EXPIRATION_DAYS = 7

ACCESS_TOKEN_EXPIRATION_MINUTES = 10
ACCESS_TOKEN_ALGORITHM = "ES256"
ACCESS_TOKEN_PRIVATE_KEY_PEM = os.environ.get(
    "ACCESS_TOKEN_PRIVATE_KEY_PEM",
"""
-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIPDn6E30e3lwXXnW1GyYYH942x0OiU/lRhYKYh9IJReaoAoGCCqGSM49
AwEHoUQDQgAEnoH4lyjW4T0uUFbAYRL1G/3dxF1Mkak4CYTwDU8lSubpkIKXFqo7
KtsWIycbTKbfLm2IdwNXDOO346u4OhCaBg==
-----END EC PRIVATE KEY-----
""",
)
ACCESS_TOKEN_PRIVATE_KEY = SigningKey.from_pem(ACCESS_TOKEN_PRIVATE_KEY_PEM)


# never remove any used schemes, or existing users won't be able to log in
global_passphrase_context = CryptContext(schemes=["argon2"], deprecated="auto")
token_cache = Cache()


class AuthenticationService:
    # one of database or user_repository must be defined
    def __init__(
        self,
        database: Session | None = None,
        user_repository: UserRepository | None = None,
        passphrase_context: CryptContext = global_passphrase_context,
    ):
        self.passphrase_context = passphrase_context
        self.user_repository = user_repository or UserRepository(database=database)

    async def create_user_with_passphrase(self, email: str, passphrase: str) -> UserType:
        hashed_passphrase = self._hash_passphrase(passphrase=passphrase)
        user = await self.user_repository.create(email=email, hashed_passphrase=hashed_passphrase)
        return UserType(id=user.id, email=user.email)

    async def authenticate_by_passphrase(self, email: str, passphrase: str) -> UserType:
        user = await self.user_repository.get_by_email(email=email)
        if self._verify_passphrase(passphrase, user.hashed_passphrase):
            return UserType(id=user.id, email=user.email)
        else:
            raise UnauthorizedException()

    def create_access_token(self, user_id: UUID, scope: Role) -> str:
        payload = {"sub": str(user_id), "scope": str(scope)}
        expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)
        payload.update({"exp": expires})
        encoded_jwt = jwt.encode(payload, ACCESS_TOKEN_PRIVATE_KEY, algorithm=ACCESS_TOKEN_ALGORITHM)

        return encoded_jwt
    
    async def create_refresh_token(self, user: UserType) -> str:
        refresh_token = token_urlsafe(48)

        await token_cache.store_refresh_token(
            refresh_token=refresh_token,
            user_id=user.id,
            expiration=(datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRATION_DAYS)),
        )

        return refresh_token
    
    async def verify_and_extract_uuid_from_refresh_token(self, refresh_token: str) -> UUID:
        return await token_cache.fetch_user_id_from_valid_refresh_token(refresh_token=refresh_token)
    
    def _hash_passphrase(self, passphrase: str) -> str:
        return self.passphrase_context.hash(passphrase)

    def _verify_passphrase(self, passphrase: str, hashed_passphrase: str) -> bool:
        return self.passphrase_context.verify(passphrase, hashed_passphrase)
