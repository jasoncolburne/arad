from sqlmodel import Session

from common.repositories.role import RoleRepository
from common.types.response import User, Role


class RoleService:
    def __init__(
        self,
        database: Session | None = None,
        role_repository: RoleRepository | None = None,
    ):
        self.role_repository = role_repository or RoleRepository(database=database)
    
    def all():
        self.role_repository.all()

    async def all_for_user(self, user: User) -> list[Role]:
        return await self.role_repository.all_for_user_id(user_id=user.id)

