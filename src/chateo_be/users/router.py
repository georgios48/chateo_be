import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.chateo_be.schemas.user import (
    DoesPhoneNumberExistRequest,
    DoesPhoneNumberExistResponse,
)
from src.chateo_be.users.logic import UserLogic
from src.chateo_be.utils.dependencies import get_main_session

users_router = APIRouter(prefix="/users")

logger = logging.getLogger("chateo.users")


@users_router.post(
    "/does-phone-number-exist",
    response_model=DoesPhoneNumberExistResponse,
)
async def does_phone_number_exist(
    payload: DoesPhoneNumberExistRequest,
    session: AsyncSession = Depends(get_main_session),
) -> DoesPhoneNumberExistResponse:
    exists = await UserLogic.does_phone_number_exist(payload.phone_number, session)
    return DoesPhoneNumberExistResponse(exists=exists)
