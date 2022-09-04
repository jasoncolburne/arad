# make sure you are editing this file in core/common

import functools
import typing

import fastapi

import common.current_user_cache
import common.datatypes.domain
import common.datatypes.exception
import common.services.authorization


global_authorization_service = common.services.authorization.AuthorizationService()
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

            common.current_user_cache.application_cache.set_current_user_id(token.sub)

            return await func(*args, **kwargs)

        return wrapped

    return _callable


def no_authorization() -> typing.Callable[
    ..., typing.Callable[..., typing.Awaitable[typing.Any]]
]:
    def _callable(
        func: typing.Callable[..., typing.Awaitable[typing.Any]]
    ) -> typing.Callable[..., typing.Awaitable[typing.Any]]:
        @functools.wraps(func)
        async def wrapped(
            *args: typing.Any, **kwargs: typing.Any
        ) -> typing.Awaitable[typing.Any]:
            common.current_user_cache.application_cache.set_current_user_id(
                common.current_user_cache.DEFAULT_USER_ID
            )

            return await func(*args, **kwargs)

        return wrapped

    return _callable
