from sqlmodel import Session

from common.services.user import UserService

from .types.response import UsersResponse


async def arad_users(email_filter: str, page: int, database: Session) -> UsersResponse:
    user_service = UserService(database=database)
    return await user_service.page(email_filter=email_filter, number=page)
