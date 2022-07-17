from enum import Enum
from pydantic import BaseModel

from common.types.response import User


class Role(Enum):
    READER = "READER"
    REVIEWER = "REVIEWER"
    ADMINISTRATOR = "ADMINISTRATOR"


class Credentials(BaseModel):
    token: str
    token_type: str


class AuthenticationResponse(BaseModel):
    credentials: Credentials
    user: User
    roles: list[Role]


class RegisterResponse(AuthenticationResponse):
    pass


class LoginResponse(AuthenticationResponse):
    pass
