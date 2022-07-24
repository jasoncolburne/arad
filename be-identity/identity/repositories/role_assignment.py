from uuid import UUID

from sqlalchemy import select, delete
from sqlmodel import Session

from database.models import Role, UserRole


class RoleAssignmentRepository:
    def __init__(self, database: Session):
        self.database = database

    async def assign_for_user_id(self, user_id: UUID, role_name: str) -> UserRole:
        query = select(Role.id).where(Role.name == role_name)
        result = await self.database.execute(query)  # type: ignore
        role_id = result.scalars().one()

        user_role = UserRole(user_id=user_id, role_id=role_id)
        self.database.add(user_role)
        await self.database.commit()  # type: ignore

        return user_role

    async def revoke_for_user_id(self, user_id: UUID, role_name: str) -> None:
        query = select(Role.id).where(Role.name == role_name)
        result = await self.database.execute(query)  # type: ignore
        role_id = result.scalars().one()

        statement = (
            delete(UserRole)
            .where(UserRole.user_id == user_id)
            .where(UserRole.role_id == role_id)
        )

        await self.database.execute(statement)  # type: ignore
        await self.database.commit()  # type: ignore
