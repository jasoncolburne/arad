from enum import Enum
from uuid import UUID

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class HealthCheckResponse(BaseModel):
    status: str


class Role(Enum):
    READER = "READER"
    REVIEWER = "REVIEWER"
    ADMINISTRATOR = "ADMINISTRATOR"


class User(BaseModel):
    id: UUID
    email: str
    roles: list[Role] | None


class UserPage(BaseModel):
    users: list[User]
    count: int
    page: int
    pages: int


class Token(BaseModel):
    sub: str
    exp: str
    scope: str
