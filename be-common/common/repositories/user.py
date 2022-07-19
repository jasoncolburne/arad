from uuid import UUID

from sqlalchemy import func, select
from sqlmodel import Session

from database.models import User


PAGE_SIZE_USER = 10


class UserRepository:
    def __init__(self, database: Session):
        self.database = database

    async def create(self, email: str, hashed_passphrase: str) -> User:
        user = User(email=email, hashed_passphrase=hashed_passphrase)
        self.database.add(user)
        await self.database.commit()
        return user

    async def get_by_id(self, user_id: UUID) -> User:
        query = select(User).where(User.id == user_id)
        result = await self.database.execute(query)
        return result.scalars().one()

    async def get_by_email(self, email: str) -> User:
        query = select(User).where(User.email == email)
        result = await self.database.execute(query)
        return result.scalars().one()

    async def count(self) -> int:
        return await self.database.scalar(select(func.count(User.id)))

    async def page(self, number: int = 1) -> list[User]:
        limit = PAGE_SIZE_USER
        offset = (number - 1) * limit

        query = select(User).order_by(User.email).limit(limit).offset(offset)
        result = await self.database.execute(query)
        return list(result.scalars().all())
