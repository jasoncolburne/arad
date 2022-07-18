from uuid import UUID

from sqlmodel import Session

from common.repositories.user import UserRepository
from common.types.response import User, Role


class RoleRepository:
    def __init__(self, database: Session):
        self.database = database

    def all(self) -> list[Role]:
        return [Role.ADMINISTRATOR, Role.REVIEWER, Role.READER]

    async def all_for_user_id(self, user_id: UUID) -> list[Role]:
        # this is a hack. eventually we want to pull roles from the db using only the user_id
        user_repository = UserRepository(database=self.database)
        user = await user_repository.get_by_id(user_id=user_id)

        roles = [Role.READER]
        if "reviewer" in user.email or "admin" in user.email:
            roles.append(Role.REVIEWER)
        if "admin" in user.email:
            roles.append(Role.ADMINISTRATOR)

        return roles
          
