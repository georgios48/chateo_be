from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.chateo_be.models.user import User
from src.chateo_be.schemas.user import CreateUserRequest, CreateUserResponse, UserPublic


class UserService:
    @staticmethod
    async def does_phone_number_exist(phone_number: str, session: AsyncSession) -> bool:
        result = await session.execute(
            select(User.id).where(User.phone_number == phone_number).limit(1)
        )
        return result.scalar_one_or_none() is not None

    @staticmethod
    async def create_user(
        payload: CreateUserRequest, session: AsyncSession
    ) -> CreateUserResponse:
        try:
            user = User(
                phone_number=payload.phone_number,
                first_name=payload.first_name,
                last_name=payload.last_name or None,
            )
            user.set_pin(payload.pin)

            session.add(user)
            await session.commit()
            await session.refresh(user)

            return CreateUserResponse(user=UserPublic.model_validate(user))
        except IntegrityError as e:
            await session.rollback()

            raise HTTPException(
                status_code=409,
                detail="A user with this phone number already exists",
            ) from e
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve)) from ve
