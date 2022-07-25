# pylint: disable=no-member

import pydantic

import common.datatypes.domain


class AuthenticationResponse(pydantic.BaseModel):
    refresh_token: str
    user: common.datatypes.domain.User


class RegisterResponse(AuthenticationResponse):
    pass


class LoginResponse(AuthenticationResponse):
    pass


class LogoutResponse(pydantic.BaseModel):
    status: str


class TokenResponse(pydantic.BaseModel):
    access_token: str


class RolesResponse(pydantic.BaseModel):
    roles: list[common.datatypes.domain.Role]


class RoleResponse(pydantic.BaseModel):
    role: common.datatypes.domain.Role
