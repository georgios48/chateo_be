from collections.abc import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import AsyncDatabaseConnection


async def get_main_session(
    request: Request,
) -> AsyncGenerator[AsyncSession, None]:
    db_main: AsyncDatabaseConnection = request.app.state.db_main
    async with db_main.session() as session:
        yield session
