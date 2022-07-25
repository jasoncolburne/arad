import sqlalchemy
import sqlmodel

import common.datatypes.domain
import common.mixins
import database.models


PAGE_SIZE_USER = 10


class UserRepository(common.mixins.RolesForUserID):
    def __init__(self, _database: sqlmodel.Session):
        self.database = _database

    async def _count(self, email_filter: str | None) -> int:
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
    ) -> common.datatypes.domain.UserPage:
        if number is None:
            raise Exception()

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
        user_models = result.scalars().all()
        users: list[common.datatypes.domain.User] = []
        for user_model in user_models:
            roles = await self.roles_for_user_id(user_id=user_model.id)
            users.append(
                common.datatypes.domain.User(
                    id=user_model.id,
                    email=user_model.email,
                    roles=roles,
                )
            )

        total = await self._count(email_filter=email_filter)
        pages = (total - 1) / PAGE_SIZE_USER + 1

        return common.datatypes.domain.UserPage(
            users=users, count=len(users), page=number, pages=pages
        )
