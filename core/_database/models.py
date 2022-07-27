# Make sure you are editing this file in arad/core

# from uuid import UUID

# from pydantic import EmailStr  # pylint: disable=no-name-in-module
# from sqlalchemy.sql.schema import Column, ForeignKey, UniqueConstraint
# from sqlmodel import Field, SQLModel
# from sqlmodel.sql.sqltypes import AutoString
# from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL


# class User(SQLModel, table=True):
#     id: UUID | None = Field(
#         sa_column=Column(
#             "id",
#             GUID,
#             primary_key=True,
#             server_default=GUID_SERVER_DEFAULT_POSTGRESQL,
#             nullable=False,
#         )
#     )

# class Article(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True, nullable=False)
#     digital_object_identifier: str = Field(index=True, sa_column=Column("name", String, unique=True))
#     author: str = Field(index=True)
#     title: str = Field(index=True)
#     journal: str = Field(index=True)
#     year: date = Field(index=True)
