# Make sure you are editing this file in be-common

from datetime import date
from typing import Optional
from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlalchemy import String
from sqlalchemy.sql.schema import Column
from sqlmodel import Field, SQLModel
from sqlmodel.sql.sqltypes import AutoString, GUID


class User(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, sa_column=Column("id", GUID, primary_key=True, nullable=False))
    email: EmailStr = Field(index=True, sa_column=Column("email", AutoString, unique=True, nullable=False))
    hashed_passphrase: str

# class Role(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True, nullable=False)
#     name: str = Field(index=True, sa_column=Column("name", String, unique=True))

# class UserRole(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True, nullable=False)
#     user_id: int = Field(foreign_key="user.id", index=True)
#     role_id: int = Field(foreign_key="role.id")

# class Article(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True, nullable=False)
#     digital_object_identifier: str = Field(index=True, sa_column=Column("name", String, unique=True))
#     author: str = Field(index=True)
#     title: str = Field(index=True)
#     journal: str = Field(index=True)
#     year: date = Field(index=True)
