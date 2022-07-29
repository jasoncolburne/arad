# pylint: disable=no-member

import enum
import uuid

import pydantic

import common.datatypes.domain


class AuthenticationRequest(pydantic.BaseModel):
    email: str
    passphrase: str


class RegisterRequest(AuthenticationRequest):
    pass


class LoginRequest(AuthenticationRequest):
    pass


class LogoutRequest(pydantic.BaseModel):
    refresh_token: str


class TokenRequest(pydantic.BaseModel):
    refresh_token: str
    scope: common.datatypes.domain.Role


class RoleAction(enum.Enum):
    ASSIGN = "ASSIGN"
    REVOKE = "REVOKE"


class RoleRequest(pydantic.BaseModel):
    user_id: uuid.UUID
    role: common.datatypes.domain.Role
    action: RoleAction


class UsersRequest(pydantic.BaseModel):  # pylint: disable=no-member
    page: int | None
    email_filter: str
