import concurrent.futures
import sqlmodel

import identity.cache
import identity.repositories.user


class HealthService:
    def __init__(
        self,
        database: sqlmodel.Session | None = None,
        user_repository: identity.repositories.user.UserRepository | None = None,
        token_cache: identity.cache.Cache | None = None,
    ):
        if token_cache is not None:
            self.token_cache = token_cache
        else:
            self.token_cache = identity.cache.global_cache_manager.get_cache()

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
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [
                executor.submit(self.user_repository.count),
                executor.submit(self.token_cache.count),
            ]

        concurrent.futures.wait(futures)

        return True
