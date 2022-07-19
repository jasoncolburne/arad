from pydantic import BaseModel

from common.types.response import UserPage, Role


class UsersResponse(UserPage):
    pass


class RolesResponse(BaseModel):
    roles: list[Role]
