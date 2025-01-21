from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(
        self,
        db_username: str,
        db_password: str,
        db_host: str,
        db_name: str,
        connect_args: Optional[Any] = None,
    ):
        connect_string = f"{db_username}:{db_password}@{db_host}/{db_name}"
        # '+asyncpg' tells SQLAlchemy to use the 'asyncpg' module to connect
        self.db_url = f"postgresql+asyncpg://{connect_string}"
        self.connect_args = connect_args or {}

    async def open(self):
        self.async_engine = create_async_engine(
            self.db_url, connect_args=self.connect_args
        )
        self.async_sessionmaker = sessionmaker(
            bind=self.async_engine,
            expire_on_commit=False,
            class_=AsyncSession,
            future=True,
        )

    async def close(self):
        if self.async_engine is not None:
            await self.async_engine.dispose()
