# Make sure you are editing this file in arad/core

# pylint: disable=no-member

import enum

import pydantic


class Role(enum.Enum):
    READER = "READER"
    REVIEWER = "REVIEWER"
    ADMINISTRATOR = "ADMINISTRATOR"


class Token(pydantic.BaseModel):
    sub: str
    exp: int
    scope: str
