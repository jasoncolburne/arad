from enum import Enum
from pydantic import BaseModel

from common.datatypes.response import User, Role


class AuthenticationResponse(BaseModel):
    refresh_token: str
    user: User
    roles: list[Role]


class RegisterResponse(AuthenticationResponse):
    pass


class LoginResponse(AuthenticationResponse):
    pass


class LogoutResponse(BaseModel):
    status: str


class TokenResponse(BaseModel):
    access_token: str


class RolesResponse(BaseModel):
    roles: list[Role]


class RoleResponse(BaseModel):
    role: Role
