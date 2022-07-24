from uuid import UUID

from sqlmodel import Session

from common.repositories.role import RoleRepository
from common.repositories.user import UserRepository, PAGE_SIZE_USER
from common.datatypes.response import UserPage, User as UserType, Role as RoleType
from database.models import User as UserModel, Role as RoleModel


class UserService:
    def __init__(
        self,
        database: Session | None = None,
        role_repository: RoleRepository | None = None,
        user_repository: UserRepository | None = None,
    ):
        # pylint: disable=duplicate-code
        if role_repository is not None:
            self.role_repository = role_repository
        elif database is not None:
            self.role_repository = RoleRepository(database=database)
        else:
            raise Exception()

        # pylint: disable=duplicate-code
        if user_repository is not None:
            self.user_repository = user_repository
        elif database is not None:
            self.user_repository = UserRepository(database=database)
        else:
            raise Exception()

    async def get(self, user_id: UUID) -> UserType:
        user_model = await self.user_repository.get_by_id(user_id=user_id)
        role_models = await self.role_repository.all_for_user_id(user_id=user_id)

        return self._sanitize_user(user_model=user_model, role_models=role_models)

    # TODO make this fast with a single query after figuring out sqlalchemy
    async def page(self, email_filter: str, number: int | None = 1) -> UserPage:
        user_models = await self.user_repository.page(
            email_filter=email_filter, number=number
        )
        total = await self.user_repository.count(email_filter=email_filter)

        users = []
        for user_model in user_models:
            if user_model.id is None:
                raise Exception()

            role_models = await self.role_repository.all_for_user_id(
                user_id=user_model.id
            )
            user = self._sanitize_user(user_model=user_model, role_models=role_models)
            users.append(user)

        print(f"total: {total}")
        pages = (total - 1) // PAGE_SIZE_USER + 1

        return UserPage(users=users, count=len(users), page=number, pages=pages)

    # here we remove passphrases
    def _sanitize_user(
        self, user_model: UserModel, role_models: list[RoleModel] | None
    ) -> UserType:
        return UserType(
            id=user_model.id,
            email=user_model.email,
            roles=[RoleType(role_model.name) for role_model in role_models],
        )
