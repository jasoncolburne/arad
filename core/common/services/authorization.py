# Make sure you are editing this file in arad/core

import datetime
import functools
import typing
import os

import fastapi
import ecdsa
import jose
from jose import jwt

import common.datatypes.domain
import common.datatypes.exception


ACCESS_TOKEN_ALGORITHM = "ES256"
ACCESS_TOKEN_PUBLIC_KEY_PEM = os.environ.get("ACCESS_TOKEN_PUBLIC_KEY_PEM")
ACCESS_TOKEN_PUBLIC_KEY = ecdsa.VerifyingKey.from_pem(ACCESS_TOKEN_PUBLIC_KEY_PEM)


class AuthorizationService:
    def verify_and_parse_token(self, token: str) -> common.datatypes.domain.Token:
        try:
            payload = jwt.decode(
                token, ACCESS_TOKEN_PUBLIC_KEY, algorithms=[ACCESS_TOKEN_ALGORITHM]
            )
        except jose.JWTError as exc:
            raise common.datatypes.exception.UnauthorizedException() from exc

        try:
            if payload["exp"] - int(datetime.datetime.utcnow().timestamp()) < 0:
                raise common.datatypes.exception.UnauthorizedException()
        except KeyError as exc:
            raise common.datatypes.exception.UnauthorizedException() from exc

        return common.datatypes.domain.Token(**payload)


global_authorization_service = AuthorizationService()
credentials_exception = fastapi.HTTPException(
    status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def require_authorization(
    role: common.datatypes.domain.Role,
) -> typing.Callable[..., typing.Callable[..., typing.Awaitable[typing.Any]]]:
    def _callable(
        func: typing.Callable[..., typing.Awaitable[typing.Any]]
    ) -> typing.Callable[..., typing.Awaitable[typing.Any]]:
        @functools.wraps(func)
        async def wrapped(
            *args: typing.Any, **kwargs: typing.Any
        ) -> typing.Awaitable[typing.Any]:
            try:
                token_string: str = kwargs["token"]
                token = global_authorization_service.verify_and_parse_token(
                    token=token_string
                )
            except common.datatypes.exception.UnauthorizedException as exc:
                raise credentials_exception from exc

            if token.scope != role.value:
                raise credentials_exception

            return await func(*args, **kwargs)

        return wrapped

    return _callable
