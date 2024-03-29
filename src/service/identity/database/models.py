# Make sure you are editing this file in be-common

from uuid import UUID

from pydantic import EmailStr  # pylint: disable=no-name-in-module
from sqlalchemy.sql.schema import Column, ForeignKey, UniqueConstraint
from sqlmodel import Field, SQLModel
from sqlmodel.sql.sqltypes import AutoString
from common.datatypes.database import GUID, GUID_SERVER_DEFAULT_POSTGRESQL


class User(SQLModel, table=True):
    id: UUID | None = Field(
        sa_column=Column(
            "id",
            GUID,
            primary_key=True,
            server_default=GUID_SERVER_DEFAULT_POSTGRESQL,
            nullable=False,
        )
    )
    email: EmailStr = Field(
        sa_column=Column("email", AutoString, unique=True, nullable=False, index=True)
    )
    hashed_passphrase: str


class Role(SQLModel, table=True):
    id: UUID | None = Field(
        sa_column=Column(
            "id",
            GUID,
            primary_key=True,
            server_default=GUID_SERVER_DEFAULT_POSTGRESQL,
            nullable=False,
        )
    )
    name: str = Field(
        sa_column=Column("name", AutoString, unique=True, nullable=False, index=True)
    )


class UserRole(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("user_id", "role_id"),)
    id: UUID | None = Field(
        sa_column=Column(
            "id",
            GUID,
            primary_key=True,
            server_default=GUID_SERVER_DEFAULT_POSTGRESQL,
            nullable=False,
        )
    )
    user_id: UUID = Field(
        sa_column=Column(
            "user_id", GUID, ForeignKey("user.id"), nullable=False, index=True
        )
    )
    role_id: UUID = Field(
        sa_column=Column("role_id", GUID, ForeignKey("role.id"), nullable=False)
    )
