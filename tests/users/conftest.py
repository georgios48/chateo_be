import pytest
from fastapi import FastAPI

from src.chateo_be.users.router import users_router


@pytest.fixture
def users_test_app() -> FastAPI:
    app = FastAPI()
    app.include_router(users_router)
    return app
