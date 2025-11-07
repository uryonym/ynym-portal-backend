"""pytest 設定と fixture."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_session
from app.config import settings


@pytest.fixture
def client():
    """FastAPI テストクライアント."""
    return TestClient(app)


@pytest.fixture
async def async_client():
    """FastAPI 用の非同期テストクライアント."""
    from httpx import AsyncClient

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
