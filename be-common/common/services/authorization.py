from datetime import datetime
from functools import wraps
from typing import Any, Awaitable, Callable
import os

from fastapi import HTTPException, status
from ecdsa import VerifyingKey
from jose import jwt, JWTError

from common.datatypes.exception import UnauthorizedException
from common.datatypes.response import Role, Token


ACCESS_TOKEN_ALGORITHM = "ES256"
ACCESS_TOKEN_PUBLIC_KEY_PEM = os.environ.get("ACCESS_TOKEN_PUBLIC_KEY_PEM")
ACCESS_TOKEN_PUBLIC_KEY = VerifyingKey.from_pem(ACCESS_TOKEN_PUBLIC_KEY_PEM)


class AuthorizationService:
    def verify_and_parse_token(self, token: str) -> Token:
        try:
            payload = jwt.decode(
                token, ACCESS_TOKEN_PUBLIC_KEY, algorithms=[ACCESS_TOKEN_ALGORITHM]
            )
        except JWTError as exc:
            raise UnauthorizedException() from exc

        try:
            if payload["exp"] - int(datetime.utcnow().timestamp()) < 0:
                raise UnauthorizedException()
        except KeyError as exc:
            raise UnauthorizedException() from exc

        return Token(**payload)


global_authorization_service = AuthorizationService()
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def require_authorization(role: Role) -> Callable[..., Callable[..., Awaitable[Any]]]:
    def _callable(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
        @wraps(func)
        async def wrapped(*args: Any, **kwargs: Any) -> Awaitable[Any]:
            try:
                token_string: str = kwargs["token"]
                token = global_authorization_service.verify_and_parse_token(
                    token=token_string
                )
            except UnauthorizedException as exc:
                raise credentials_exception from exc

            if token.scope != role.value:
                raise credentials_exception

            return await func(*args, **kwargs)

        return wrapped

    return _callable
