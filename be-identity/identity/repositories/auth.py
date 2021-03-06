import typing
import uuid

import sqlalchemy
import sqlmodel

import common.datatypes.domain
import common.datatypes.exception
import common.mixins
import database.models


DEFAULT_USER_ROLES = [common.datatypes.domain.Role.READER]
global_role_id_cache: dict[str, uuid.UUID] = {}


class AuthRepository(common.mixins.RolesForUserID):
    def __init__(self, _database: sqlmodel.Session):
        self.database = _database

    async def _warm_global_role_id_cache(self) -> None:
        if global_role_id_cache:
            return

        query = sqlalchemy.select(database.models.Role)
        result = await self.database.execute(query)  # type: ignore
        global_role_id_cache.update(
            {role.name: role.id for role in result.scalars().all()}
        )

    async def all_roles(self) -> list[common.datatypes.domain.Role]:
        await self._warm_global_role_id_cache()

        return [
            common.datatypes.domain.Role(role_name)
            for role_name in global_role_id_cache
        ]

    async def create_user(
        self, email: str, hashed_passphrase: str
    ) -> common.datatypes.domain.User:
        user = database.models.User(email=email, hashed_passphrase=hashed_passphrase)
        self.database.add(user)
        await self.database.commit()  # type: ignore

        default_roles = DEFAULT_USER_ROLES
        await self._warm_global_role_id_cache()

        for role in default_roles:
            role_id = global_role_id_cache[role.value]
            user_role = database.models.UserRole(user_id=user.id, role_id=role_id)
            self.database.add(user_role)
            await self.database.commit()  # type: ignore

        return common.datatypes.domain.User(
            id=user.id, email=user.email, roles=default_roles
        )

    async def verify_user_email_and_passphrase(
        self, email: str, passphrase: str, verify: typing.Callable[[str, str], bool]
    ) -> common.datatypes.domain.User:
        query = sqlalchemy.select(database.models.User).where(
            database.models.User.email == email
        )
        result = await self.database.execute(query)  # type: ignore
        user = result.scalars().one()
        roles = await self.roles_for_user_id(user_id=user.id)

        if not verify(passphrase, user.hashed_passphrase):
            raise common.datatypes.exception.UnauthorizedException()

        return common.datatypes.domain.User(
            id=user.id,
            email=user.email,
            roles=roles,
        )

    async def assign_role_for_user_id(self, user_id: uuid.UUID, role_name: str) -> None:
        await self._warm_global_role_id_cache()
        role_id = global_role_id_cache[role_name]

        user_role = database.models.UserRole(user_id=user_id, role_id=role_id)
        self.database.add(user_role)
        await self.database.commit()  # type: ignore

    async def revoke_role_for_user_id(self, user_id: uuid.UUID, role_name: str) -> None:
        await self._warm_global_role_id_cache()
        role_id = global_role_id_cache[role_name]

        statement = (
            sqlalchemy.delete(database.models.UserRole)
            .where(database.models.UserRole.user_id == user_id)
            .where(database.models.UserRole.role_id == role_id)
        )

        await self.database.execute(statement)  # type: ignore
        await self.database.commit()  # type: ignore
