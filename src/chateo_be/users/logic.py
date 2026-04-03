from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.chateo_be.models.user import User


class UserLogic:
    @staticmethod
    async def does_phone_number_exist(phone_number: str, session: AsyncSession) -> bool:
        result = await session.execute(
            select(User.id).where(User.phone_number == phone_number).limit(1)
        )
        return result.scalar_one_or_none() is not None
