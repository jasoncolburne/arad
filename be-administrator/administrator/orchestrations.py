from sqlmodel import Session

from common.services.user import UserService

from .datatypes.response import UsersResponse


async def arad_users(
    email_filter: str, page: int | None, database: Session
) -> UsersResponse:
    user_service = UserService(database=database)
    user_page = await user_service.page(email_filter=email_filter, number=page)

    return UsersResponse(**user_page.dict())
