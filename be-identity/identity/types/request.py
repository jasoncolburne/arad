from pydantic import BaseModel

from common.types.response import Role


class AuthenticationRequest(BaseModel):
    email: str
    passphrase: str


class RegisterRequest(AuthenticationRequest):
    pass


class LoginRequest(AuthenticationRequest):
    pass


class TokenRequest(BaseModel):
    refresh_token: str
    scope: Role
