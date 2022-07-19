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
    
    async def all(self) -> list[Role]:
        role_models = await self.role_repository.all()
        return [Role(role_model.name) for role_model in role_models]

    async def all_for_user(self, user: User) -> list[Role]:
        role_models = await self.role_repository.all_for_user_id(user_id=user.id)
        return [Role(role_model.name) for role_model in role_models]

    async def assign_to_user(self, user: User, role: Role) -> Role:
        await self.role_repository.assign_to_user_id(user_id=user.id, role_name=role.value)
        return role
