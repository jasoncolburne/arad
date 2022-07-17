from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    id: UUID
    email: str


class UserPage(BaseModel):
    users: list[User]
    count: int
    page: int
    pages: int
