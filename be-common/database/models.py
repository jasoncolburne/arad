# Make sure you are editing this file in be-common

from datetime import date
from typing import Optional
from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlalchemy import String
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlmodel import Field, SQLModel
from sqlmodel.sql.sqltypes import AutoString
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL

class User(SQLModel, table=True):
    id: UUID | None = Field(sa_column=Column(
        "id",
        GUID,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL,
        nullable=False
    ))
    email: EmailStr = Field(sa_column=Column("email", AutoString, unique=True, nullable=False, index=True))
    hashed_passphrase: str

class Role(SQLModel, table=True):
    id: UUID | None = Field(sa_column=Column(
        "id",
        GUID,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL,
        nullable=False
    ))
    name: str = Field(sa_column=Column("name", AutoString, unique=True, nullable=False, index=True))

class UserRole(SQLModel, table=True):
    id: UUID | None = Field(sa_column=Column(
        "id",
        GUID,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL,
        nullable=False
    ))
    user_id: UUID = Field(sa_column=Column("user_id", GUID, ForeignKey("user.id"), nullable=False, index=True))
    role_id: UUID = Field(sa_column=Column("role_id", GUID, ForeignKey("role.id"), nullable=False))

# class Article(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True, nullable=False)
#     digital_object_identifier: str = Field(index=True, sa_column=Column("name", String, unique=True))
#     author: str = Field(index=True)
#     title: str = Field(index=True)
#     journal: str = Field(index=True)
#     year: date = Field(index=True)
