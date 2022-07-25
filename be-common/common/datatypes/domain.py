# pylint: disable=no-member

import enum
import uuid

import pydantic


class Role(enum.Enum):
    READER = "READER"
    REVIEWER = "REVIEWER"
    ADMINISTRATOR = "ADMINISTRATOR"


class User(pydantic.BaseModel):
    id: uuid.UUID
    email: str
    roles: list[Role] | None


class UserPage(pydantic.BaseModel):
    users: list[User]
    count: int
    page: int
    pages: int


class Token(pydantic.BaseModel):
    sub: str
    exp: str
    scope: str
