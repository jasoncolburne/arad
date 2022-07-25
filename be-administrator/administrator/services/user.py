import sqlmodel

import common.datatypes.domain

import administrator.repositories.user


class UserService:
    def __init__(
        self,
        database: sqlmodel.Session | None = None,
        user_repository: administrator.repositories.user.UserRepository | None = None,
    ):
        if user_repository is not None:
            self.user_repository = user_repository
        elif database is not None:
            self.user_repository = administrator.repositories.user.UserRepository(
                _database=database
            )
        else:
            raise Exception()

    # TODO make this fast with a single query after figuring out sqlalchemy
    async def page(
        self, email_filter: str, number: int | None = 1
    ) -> common.datatypes.domain.UserPage:
        return await self.user_repository.page(email_filter=email_filter, number=number)
