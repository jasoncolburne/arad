from typing import List
from uuid import UUID

from sqlalchemy import func, select
from sqlmodel import Session

from database.models import User


class UserService:
    def __init__(self, database: Session):
        self.database = database      

    async def create(self, user: User) -> User:
        self.database.add(user)
        await self.database.commit()

        return user

    async def get_current(self, token: str) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, TOKEN_KEY, algorithms=[TOKEN_ALGORITHM])
            user_id = UUID(payload.get("sub"))
            if user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        
        user = await self.get_by_id(user_id)
        if user is None:
            raise credentials_exception
        return user

    async def get_by_id(self, user_id: UUID) -> User:
        query = select(User).where(User.id == user_id)
        result = await self.database.execute(query)
        user = result.scalars().one()

        return user

    async def get_by_email(self, email: str) -> User:
        query = select(User).where(User.email == email)
        result = await self.database.execute(query)
        user = result.scalars().one()

        return user

    async def list_paginated(self, page: int = 1) -> List[User]:
        limit = 10
        offset = (page - 1) * limit

        query = await self.database.execute(select(User).order_by(User.email).limit(limit).offset(offset))
        return list(query.scalars().all())

    async def count(self) -> int:
        return await self.database.scalar(select(func.count(User.id)))
