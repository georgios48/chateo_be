import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.chateo_be.users.logic import UserLogic


@pytest.mark.asyncio
async def test_does_phone_number_exist_false_when_no_match() -> None:
    session = AsyncMock()
    result = MagicMock()
    result.scalar_one_or_none.return_value = None
    session.execute = AsyncMock(return_value=result)

    assert await UserLogic.does_phone_number_exist("+15550001111", session) is False


@pytest.mark.asyncio
async def test_does_phone_number_exist_true_when_row_present() -> None:
    session = AsyncMock()
    result = MagicMock()
    result.scalar_one_or_none.return_value = uuid.uuid4()
    session.execute = AsyncMock(return_value=result)

    assert await UserLogic.does_phone_number_exist("+15550001111", session) is True
