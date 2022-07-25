import uuid
import os

import sqlalchemy
import sqlmodel

import common.datatypes.domain
import common.datatypes.exception

import identity.datatypes.request
import identity.datatypes.response
import identity.services.auth


DEFAULT_ADMIN_EMAIL = os.environ.get("DEFAULT_ADMIN_EMAIL")


async def arad_register(
    email: str, passphrase: str, database: sqlmodel.Session
) -> identity.datatypes.response.RegisterResponse:
    auth_service = identity.services.auth.AuthService(database=database)
    try:
        user = await auth_service.create_user_with_passphrase(
            email=email,
            passphrase=passphrase,
        )
    except sqlalchemy.exc.IntegrityError as ex:
        raise common.datatypes.exception.BadRequestException() from ex

    if DEFAULT_ADMIN_EMAIL and email == DEFAULT_ADMIN_EMAIL:
        await auth_service.assign_role_for_user_id(
            user_id=user.id, role=common.datatypes.domain.Role.REVIEWER
        )
        await auth_service.assign_role_for_user_id(
            user_id=user.id, role=common.datatypes.domain.Role.ADMINISTRATOR
        )

    refresh_token = await auth_service.create_refresh_token(user=user)

    return identity.datatypes.response.RegisterResponse(
        refresh_token=refresh_token,
        user=user,
        roles=user.roles,
    )


async def arad_login(
    email: str, passphrase: str, database: sqlmodel.Session
) -> identity.datatypes.response.LoginResponse:
    auth_service = identity.services.auth.AuthService(database=database)
    try:
        user = await auth_service.authenticate_user_by_email_and_passphrase(
            email=email,
            passphrase=passphrase,
        )
    except sqlalchemy.exc.NoResultFound as ex:
        raise common.datatypes.exception.UnauthorizedException() from ex

    refresh_token = await auth_service.create_refresh_token(user=user)

    return identity.datatypes.response.LoginResponse(
        refresh_token=refresh_token,
        user=user,
        roles=user.roles,
    )


async def arad_logout(
    refresh_token: str, database: sqlmodel.Session
) -> identity.datatypes.response.LogoutResponse:
    auth_service = identity.services.auth.AuthService(database=database)
    await auth_service.destroy_refresh_token(refresh_token=refresh_token)

    return identity.datatypes.response.LogoutResponse(status="ok")


async def arad_access_token(
    refresh_token: str, scope: common.datatypes.domain.Role, database: sqlmodel.Session
) -> identity.datatypes.response.TokenResponse:
    auth_service = identity.services.auth.AuthService(database=database)
    user_id = await auth_service.verify_and_extract_uuid_from_refresh_token(
        refresh_token=refresh_token
    )

    access_token = await auth_service.create_access_token(user_id=user_id, scope=scope)

    return identity.datatypes.response.TokenResponse(access_token=access_token)


async def arad_roles(
    database: sqlmodel.Session,
) -> identity.datatypes.response.RolesResponse:
    auth_service = identity.services.auth.AuthService(database=database)
    roles = await auth_service.all_roles()

    return identity.datatypes.response.RolesResponse(roles=roles)


async def arad_modify_role_assignment(
    user_id: uuid.UUID,
    role: common.datatypes.domain.Role,
    action: identity.datatypes.request.RoleAction,
    database: sqlmodel.Session,
) -> identity.datatypes.response.RoleResponse:
    auth_service = identity.services.auth.AuthService(database=database)

    # this admin function isn't critical and the ui should protect us from most edge cases so we'll just let these
    # calls explode if for instance the role has already been assigned to the user (possible with two tabs open)
    if action == identity.datatypes.request.RoleAction.ASSIGN:
        await auth_service.assign_role_for_user_id(user_id=user_id, role=role)
    elif action == identity.datatypes.request.RoleAction.REVOKE:
        await auth_service.revoke_role_for_user_id(user_id=user_id, role=role)
    else:
        raise Exception()

    auth_service = identity.services.auth.AuthService(database=database)
    await auth_service.destroy_all_refresh_tokens_for_user_id(user_id=user_id)

    return identity.datatypes.response.RoleResponse(role=role)
