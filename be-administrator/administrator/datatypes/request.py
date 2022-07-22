from pydantic import BaseModel

class UsersRequest(BaseModel):
    page: int | None
    email_filter: str
