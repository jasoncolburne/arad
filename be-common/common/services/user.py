from uuid import UUID

from sqlmodel import Session

from common.repositories.user import UserRepository, PAGE_SIZE_USER
from common.types.response import UserPage, User as UserType
from database.models import User as UserModel


class UserService:
    def __init__(
        self,
        database: Session | None = None,
        user_repository: UserRepository | None = None,
    ):
        self.user_repository = user_repository or UserRepository(database=database)

    async def page(self, number: int = 1) -> UserPage:
        users = await self.user_repository.page(number=number)
        total = await self.user_repository.count()

        pages = (total - 1) // PAGE_SIZE_USER + 1

        return {
            "users": [self._sanitize_user(user) for user in users],
            "count": len(users),
            "page": number,
            "pages": pages,
        }

    # here we remove passphrases
    def _sanitize_user(self, user: UserModel) -> UserType:
        return UserType(id=user.id, email=user.email)
