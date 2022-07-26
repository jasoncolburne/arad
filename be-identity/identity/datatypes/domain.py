# pylint: disable=no-member

import uuid

import pydantic

import common.datatypes.domain


class User(pydantic.BaseModel):
    id: uuid.UUID
    email: str
    roles: list[common.datatypes.domain.Role]


class UserPage(pydantic.BaseModel):
    users: list[User]
    count: int
    page: int
    pages: int
