from uuid import UUID

from sqlalchemy import select
from sqlmodel import Session

from database.models import Role, UserRole


class RoleRepository:
    def __init__(self, database: Session):
        self.database = database

    async def all(self) -> list[Role]:
        query = select(Role)
        result = await self.database.execute(query)  # type: ignore
        roles = list(result.scalars().all())

        return roles

    async def all_for_user_id(self, user_id: UUID) -> list[Role]:
        query = select(UserRole.role_id).where(UserRole.user_id == user_id)
        result = await self.database.execute(query)  # type: ignore
        role_ids = list(result.scalars().all())

        query = select(Role).where(Role.id.in_(role_ids))  # type: ignore
        result = await self.database.execute(query)  # type: ignore
        roles = list(result.scalars().all())

        return roles
