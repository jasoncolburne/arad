import sqlalchemy
import sqlmodel

import common.datatypes.exception
import database.models

import identity.datatypes.domain
import identity.mixins


PAGE_SIZE_USER = 10


class UserRepository(identity.mixins.RolesForUserID):
    def __init__(self, _database: sqlmodel.Session):
        self.database = _database

    async def count(self, email_filter: str | None = None) -> int:
        if email_filter:
            query = sqlalchemy.select(
                sqlalchemy.func.count(database.models.User.id)
            ).where(
                sqlalchemy.func.lower(database.models.User.email).contains(
                    sqlalchemy.func.lower(email_filter)
                )
            )
        else:
            query = sqlalchemy.select(sqlalchemy.func.count(database.models.User.id))
        return await self.database.scalar(query)

    async def page(
        self, email_filter: str, number: int | None = 1
    ) -> identity.datatypes.domain.UserPage:
        if number is None:
            raise common.datatypes.exception.AradException()

        limit = PAGE_SIZE_USER
        offset = (number - 1) * limit

        if email_filter:
            query = sqlalchemy.select(database.models.User).where(
                sqlalchemy.func.lower(database.models.User.email).contains(
                    sqlalchemy.func.lower(email_filter)
                )
            )
        else:
            query = sqlalchemy.select(database.models.User)
        query = query.order_by(database.models.User.email).limit(limit).offset(offset)

        result = await self.database.execute(query)  # type: ignore
        user_models = result.scalars()
        users: list[identity.datatypes.domain.User] = []
        for user_model in user_models:
            roles = await self.roles_for_user_id(user_id=user_model.id)
            users.append(
                identity.datatypes.domain.User(
                    id=user_model.id,
                    email=user_model.email,
                    roles=roles,
                )
            )

        total = await self.count(email_filter=email_filter)
        pages = (total - 1) / PAGE_SIZE_USER + 1

        return identity.datatypes.domain.UserPage(
            users=users, count=len(users), page=number, pages=pages
        )
