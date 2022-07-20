from datetime import datetime
from functools import wraps
import os

from fastapi import HTTPException, status
from ecdsa import VerifyingKey
from jose import jwt, JWTError

from common.types.exception import UnauthorizedException


ACCESS_TOKEN_ALGORITHM = "ES256"
ACCESS_TOKEN_PUBLIC_KEY_PEM = os.environ.get("ACCESS_TOKEN_PUBLIC_KEY_PEM")
ACCESS_TOKEN_PUBLIC_KEY = VerifyingKey.from_pem(ACCESS_TOKEN_PUBLIC_KEY_PEM)


class AuthenticationService:
    def verify_and_parse_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, ACCESS_TOKEN_PUBLIC_KEY, algorithms=[ACCESS_TOKEN_ALGORITHM])
        except JWTError:
            raise UnauthorizedException()
        
        if (payload["exp"] - int(datetime.utcnow().timestamp()) < 0):
            raise UnauthorizedException()

        return payload


global_authentication_service = AuthenticationService()
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

def require_authorization(role):
    def callable(func):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            try:
                token = kwargs["token"]
                token_contents = global_authentication_service.verify_and_parse_token(token=token)
            except UnauthorizedException:
                raise credentials_exception

            if token_contents.get("scope") != role.value:
                raise credentials_exception

            return await func(*args, **kwargs)

        return wrapped

    return callable

