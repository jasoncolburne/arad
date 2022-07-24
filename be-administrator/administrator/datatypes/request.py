from pydantic import BaseModel  # pylint: disable=no-name-in-module


class UsersRequest(BaseModel):
    page: int | None
    email_filter: str
