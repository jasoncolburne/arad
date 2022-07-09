# Make sure you are editing this file in node-common

from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    email: str

class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    name: str

class UserRole(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    user_id: int = Field(foreign_key="user.id")
    role_id: int = Field(foreign_key="role.id")

class Article(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    digital_object_identifier: str
    author: str
    title: str
    journal: str
    year: date
