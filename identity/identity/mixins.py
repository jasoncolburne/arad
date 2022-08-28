import uuid

import sqlalchemy
import sqlmodel

import common.datatypes.domain
import common.datatypes.exception
import database.models


class RolesForUserID:
    database: sqlmodel.Session

    async def roles_for_user_id(
        self, user_id: uuid.UUID
    ) -> list[common.datatypes.domain.Role]:
        query = sqlalchemy.select(database.models.UserRole.role_id).where(
            database.models.UserRole.user_id == user_id
        )
        result = await self.database.execute(query)  # type: ignore
        role_ids = result.scalars().all()

        query = sqlalchemy.select(database.models.Role).where(database.models.Role.id.in_(role_ids))  # type: ignore # pylint: disable=no-member
        result = await self.database.execute(query)  # type: ignore
        roles = result.fetchall()

        return [common.datatypes.domain.Role(role.name) for role in roles]
