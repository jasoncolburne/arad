import asyncio
import collections


DEFAULT_USER_ID = "00000000-0000-0000-0000-000000000000"


class CurrentUserCache:
    def __init__(self) -> None:
        def default_user_id() -> str:
            return DEFAULT_USER_ID

        self.cache: dict[str, str] = collections.defaultdict(default_user_id)

    def key(self) -> str:
        task = asyncio.current_task()
        key = task.get_name() if task else "default"
        return key

    def set_current_user_id(self, user_id: str) -> None:
        self.cache[self.key()] = user_id

    def get_current_user_id(self) -> str:
        return self.cache[self.key()]


application_cache = CurrentUserCache()
