from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class Role(Enum):
    READER = "READER"
    REVIEWER = "REVIEWER"
    ADMINISTRATOR = "ADMINISTRATOR"


class User(BaseModel):
    id: UUID
    email: str


class UserPage(BaseModel):
    users: list[User]
    count: int
    page: int
    pages: int
