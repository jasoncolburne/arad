from uuid import UUID

from sqlalchemy import func, select
from sqlmodel import Session

from database.models import Role, UserRole


class RoleRepository:
    def __init__(self, database: Session):
        self.database = database

    async def all(self) -> list[UserRole]:
        query = select(Role)
        result = await self.database.execute(query)
        roles = list(result.scalars().all())

        return roles

    async def all_for_user_id(self, user_id: UUID) -> list[UserRole]:
        query = select(UserRole.role_id).where(UserRole.user_id == user_id)
        result = await self.database.execute(query)
        role_ids = list(result.scalars().all())
        
        query = select(Role).where(Role.id.in_(role_ids))
        result = await self.database.execute(query)
        roles = list(result.scalars().all())
        
        return roles

    async def assign_to_user_id(self, user_id: UUID, role_name: str) -> UserRole:
        query = select(Role.id).where(Role.name == role_name)
        result = await self.database.execute(query)
        role_id = result.scalars().one()

        user_role = UserRole(user_id=user_id, role_id=role_id)
        self.database.add(user_role)
        await self.database.commit()

        return user_role
