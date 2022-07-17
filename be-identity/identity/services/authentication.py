from datetime import datetime, timedelta
import os

from jose import jwt
from passlib.context import CryptContext
from sqlmodel import Session

from common.repositories.user import UserRepository
from common.types.response import User as UserType

TOKEN_EXPIRATION_MINUTES = 15
TOKEN_KEY = os.environ.get("TOKEN_KEY", "d2c4293024e14c0716fe2135d351ba718c06c70d0d30af4b59752176e2a34152")
TOKEN_ALGORITHM = "HS256"


# never remove any used schemes, or existing users won't be able to log in
global_passphrase_context = CryptContext(schemes=["argon2"], deprecated="auto")


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
            raise Exception("Invalid username or passphrase")

    def create_access_token(self, user: UserType) -> str:
        payload = {"sub": str(user.id)}
        expires = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_MINUTES)
        payload.update({"exp": expires})
        encoded_jwt = jwt.encode(payload, TOKEN_KEY, algorithm=TOKEN_ALGORITHM)

        return encoded_jwt
    
    def _hash_passphrase(self, passphrase: str) -> str:
        return self.passphrase_context.hash(passphrase)

    def _verify_passphrase(self, passphrase: str, hashed_passphrase: str) -> bool:
        return self.passphrase_context.verify(passphrase, hashed_passphrase)
