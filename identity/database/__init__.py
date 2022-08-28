import os

import sqlalchemy.ext.asyncio
import sqlalchemy.orm


DATABASE_URL = os.environ.get("DATABASE_URL")


class DatabaseManager:
    def __init__(self) -> None:
        self.engine: sqlalchemy.ext.asyncio.AsyncEngine | None = None

    def get_engine(self) -> sqlalchemy.ext.asyncio.AsyncEngine:
        if self.engine is None:
            self.engine = sqlalchemy.ext.asyncio.create_async_engine(
                DATABASE_URL,
                pool_recycle=900,
                pool_pre_ping=True,
                future=True,
            )

        return self.engine


global_database_manager = DatabaseManager()


async def get_session():  # type: ignore
    async_session = sqlalchemy.orm.sessionmaker(
        global_database_manager.get_engine(),
        class_=sqlalchemy.ext.asyncio.AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session
