import pydantic


class UsersRequest(pydantic.BaseModel):  # pylint: disable=no-member
    page: int | None
    email_filter: str
