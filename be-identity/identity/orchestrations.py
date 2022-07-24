from uuid import UUID
import os

from sqlalchemy import exc
from sqlmodel import Session

from common.services.user import UserService
from common.datatypes.exception import BadRequestException, UnauthorizedException
from common.datatypes.response import User, Role

from .services.authentication import AuthenticationService
from .services.role import RoleService
from .datatypes.request import RoleAction
from .datatypes.response import (
    AuthenticationResponse,
    LoginResponse,
    RegisterResponse,
    TokenResponse,
    RolesResponse,
    RoleResponse,
    LogoutResponse,
)


DEFAULT_ADMIN_EMAIL = os.environ.get("DEFAULT_ADMIN_EMAIL")


async def arad_register(
    email: str, passphrase: str, database: Session
) -> RegisterResponse:
    authentication_service = AuthenticationService(database=database)
    try:
        user = await authentication_service.create_user_with_passphrase(
            email=email,
            passphrase=passphrase,
        )
    except exc.IntegrityError as ex:
        raise BadRequestException() from ex

    role_service = RoleService(database=database)
    await role_service.assign_for_user(user=user, role=Role.READER)

    if DEFAULT_ADMIN_EMAIL and email == DEFAULT_ADMIN_EMAIL:
        await role_service.assign_for_user(user=user, role=Role.REVIEWER)
        await role_service.assign_for_user(user=user, role=Role.ADMINISTRATOR)

    response = await _arad_authentication_response(
        database=database, user=user, authentication_service=authentication_service
    )

    return RegisterResponse(**response.dict())


async def arad_login(email: str, passphrase: str, database: Session) -> LoginResponse:
    authentication_service = AuthenticationService(database=database)
    try:
        user = await authentication_service.authenticate_by_passphrase(
            email=email,
            passphrase=passphrase,
        )
    except exc.NoResultFound as ex:
        raise UnauthorizedException() from ex

    response = await _arad_authentication_response(
        user=user,
        authentication_service=authentication_service,
        database=database,
    )

    return LoginResponse(**response.dict())


async def _arad_authentication_response(
    user: User,
    authentication_service: AuthenticationService,
    database: Session,
) -> AuthenticationResponse:
    refresh_token = await authentication_service.create_refresh_token(user=user)

    role_service = RoleService(database=database)
    roles = await role_service.all_for_user(user=user)

    return AuthenticationResponse(
        refresh_token=refresh_token,
        user=user,
        roles=roles,
    )


async def arad_logout(refresh_token: str, database: Session) -> LogoutResponse:
    authentication_service = AuthenticationService(database=database)
    await authentication_service.destroy_refresh_token(refresh_token=refresh_token)

    return LogoutResponse(status="ok")


async def arad_access_token(
    refresh_token: str, scope: Role, database: Session
) -> TokenResponse:
    authentication_service = AuthenticationService(database=database)
    user_id = await authentication_service.verify_and_extract_uuid_from_refresh_token(
        refresh_token=refresh_token
    )

    access_token = await authentication_service.create_access_token(
        user_id=user_id, scope=scope
    )

    return TokenResponse(access_token=access_token)


async def arad_roles(database: Session) -> RolesResponse:
    role_service = RoleService(database=database)
    roles = await role_service.all()

    return RolesResponse(roles=roles)


async def arad_assign_role(
    user_id: UUID, role: Role, action: RoleAction, database: Session
) -> RoleResponse:
    role_service = RoleService(database=database)
    user_service = UserService(database=database)

    user = await user_service.get(user_id=user_id)

    # this admin function isn't critical and the ui should protect us from most edge cases so we'll just let these
    # calls explode if for instance the role has already been assigned to the user (possible with two tabs open)
    if action == RoleAction.ASSIGN:
        role = await role_service.assign_for_user(user=user, role=role)
    elif action == RoleAction.REVOKE:
        role = await role_service.revoke_for_user(user=user, role=role)
    else:
        # this code should be unreachable
        raise Exception()

    authentication_service = AuthenticationService(database=database)
    await authentication_service.destroy_all_refresh_tokens_for_user_id(user_id=user.id)

    return RoleResponse(role=role)
