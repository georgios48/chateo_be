from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import ASGITransport, AsyncClient

from src.chateo_be.utils.dependencies import get_main_session


@pytest.mark.asyncio
async def test_does_phone_number_exist_returns_exists_false(users_test_app) -> None:
    session = AsyncMock()
    result = MagicMock()
    result.scalar_one_or_none.return_value = None
    session.execute = AsyncMock(return_value=result)

    async def override_session():
        yield session

    users_test_app.dependency_overrides[get_main_session] = override_session
    transport = ASGITransport(app=users_test_app)
    try:
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/users/does-phone-number-exist",
                json={"phone_number": "+15550001111"},
            )
    finally:
        users_test_app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {"exists": False}


@pytest.mark.asyncio
async def test_does_phone_number_exist_rejects_blank_phone(users_test_app) -> None:
    async def override_session():
        yield AsyncMock()

    users_test_app.dependency_overrides[get_main_session] = override_session
    transport = ASGITransport(app=users_test_app)
    try:
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/users/does-phone-number-exist",
                json={"phone_number": "   "},
            )
    finally:
        users_test_app.dependency_overrides.clear()

    assert response.status_code == 422
