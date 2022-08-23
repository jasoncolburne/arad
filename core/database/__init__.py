# Make sure you are editing this file in arad/core

import os

from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = os.environ.get("DATABASE_URL")


class DatabaseManager:
    def __init__(self) -> None:
        self.engine: AsyncEngine | None = None

    def get_engine(self) -> AsyncEngine:
        if self.engine is None:
            self.engine = create_async_engine(DATABASE_URL, echo=False, pool_recycle=900, future=True)

        return self.engine


global_database_manager = DatabaseManager()


async def get_session() -> AsyncSession:  # type: ignore
    async_session = sessionmaker(
        global_database_manager.get_engine(),
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session
