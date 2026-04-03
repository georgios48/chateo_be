from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


def to_async_database_url(url: str) -> str:
    if url.startswith("postgresql+psycopg://"):
        rest = url.removeprefix("postgresql+psycopg://")
        return f"postgresql+psycopg_async://{rest}"
    if url.startswith("postgresql://"):
        rest = url.removeprefix("postgresql://")
        return f"postgresql+psycopg_async://{rest}"
    return url


class AsyncDatabaseConnection:
    def __init__(self, database_url: str) -> None:
        self._engine = create_async_engine(
            to_async_database_url(database_url),
            pool_pre_ping=True,
        )
        self._session_factory = async_sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )

    @property
    def engine(self):
        return self._engine

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._session_factory() as session:
            yield session

    async def dispose(self) -> None:
        await self._engine.dispose()
