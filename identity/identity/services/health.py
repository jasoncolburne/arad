import sqlmodel

import identity.repositories.user


class HealthService:
    def __init__(
        self,
        database: sqlmodel.Session | None = None,
        user_repository: identity.repositories.user.UserRepository | None = None,
    ):
        # pylint: disable=duplicate-code
        if user_repository is not None:
            self.user_repository = user_repository
        elif database is not None:
            self.user_repository = identity.repositories.user.UserRepository(
                _database=database
            )
        else:
            raise Exception()

    async def healthy(self) -> bool:
        await self.user_repository.count()

        return True
