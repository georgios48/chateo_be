import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from src.chateo_be.schemas.user import CreateUserRequest
from src.chateo_be.users.service import UserService


@pytest.mark.asyncio
async def test_does_phone_number_exist_false_when_no_match() -> None:
    session = AsyncMock()
    result = MagicMock()
    result.scalar_one_or_none.return_value = None
    session.execute = AsyncMock(return_value=result)

    assert await UserService.does_phone_number_exist("+15550001111", session) is False


@pytest.mark.asyncio
async def test_does_phone_number_exist_true_when_row_present() -> None:
    session = AsyncMock()
    result = MagicMock()
    result.scalar_one_or_none.return_value = uuid.uuid4()
    session.execute = AsyncMock(return_value=result)

    assert await UserService.does_phone_number_exist("+15550001111", session) is True


@pytest.mark.asyncio
async def test_create_user_success() -> None:
    payload = CreateUserRequest(
        phone_number="+15550009999",
        first_name="Ada",
        last_name="Lovelace",
        pin="4242",
    )
    session = AsyncMock()
    session.add = MagicMock()
    session.commit = AsyncMock()

    async def assign_id_on_refresh(user) -> None:
        user.id = uuid.uuid4()

    session.refresh = AsyncMock(side_effect=assign_id_on_refresh)

    result = await UserService.create_user(payload, session)

    session.add.assert_called_once()
    session.commit.assert_awaited_once()
    session.refresh.assert_awaited_once()
    assert result.user.phone_number == "+15550009999"
    assert result.user.first_name == "Ada"
    assert result.user.last_name == "Lovelace"
    assert result.user.id is not None


@pytest.mark.asyncio
async def test_create_user_integrity_error_returns_409() -> None:
    payload = CreateUserRequest(
        phone_number="+15550009999",
        first_name="Ada",
        last_name="Lovelace",
        pin="4242",
    )
    session = AsyncMock()
    session.add = MagicMock()
    session.commit = AsyncMock(side_effect=IntegrityError("stmt", {}, None))
    session.refresh = AsyncMock()
    session.rollback = AsyncMock()

    with pytest.raises(HTTPException) as exc:
        await UserService.create_user(payload, session)

    assert exc.value.status_code == 409
    session.rollback.assert_awaited_once()
