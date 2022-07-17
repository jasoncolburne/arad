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

    async def create(self, email: str, hashed_passphrase: str) -> UserType:
        user = await self.user_repository.create(
            UserModel(
                email=email,
                hashed_passphrase=hashed_passphrase
            )
        )

        return self._sanitize_user(user)

    # async def get_by_id(self, user_id: UUID) -> UserType:
    #     user = await self.user_repository.get_by_id(user_id=user_id)
    #     return self._sanitize_user(user)

    # async def get_by_email(self, email: str) -> UserType:
    #     user = await self.user_repository.get_by_email(email=email)
    #     return self._sanitize_user(user)

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
