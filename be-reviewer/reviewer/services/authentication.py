from datetime import datetime, timedelta
from os import environ

from jose import jwt
from passlib.context import CryptContext

from database.models import User


TOKEN_EXPIRATION_MINUTES = 10080
TOKEN_KEY = environ.get("TOKEN_KEY", "d2c4293024e14c0716fe2135d351ba718c06c70d0d30af4b59752176e2a34152")
TOKEN_ALGORITHM = "HS256"


class AuthenticationService:
    def __init__(self):
        # never remove any used schemes, or existing users won't be able to log in
        self.passphrase_context = CryptContext(schemes=["argon2"], deprecated="auto")

    def verify_passphrase(self, passphrase: str, hashed_passphrase: str) -> bool:
        return self.passphrase_context.verify(passphrase, hashed_passphrase)

    def authenticate_user(self, user: User, passphrase: str) -> User:
        return self.verify_passphrase(passphrase, user.hashed_passphrase)
