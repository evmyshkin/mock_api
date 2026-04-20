from collections.abc import AsyncGenerator

import pytest_asyncio

from fastapi import FastAPI
from httpx import ASGITransport
from httpx import AsyncClient

from app.api.router import router as main_router
from app.main import fastapi_app


@pytest_asyncio.fixture(scope='class')
async def async_client() -> AsyncGenerator[AsyncClient]:
    transport = ASGITransport(app=fastapi_app)

    async with AsyncClient(
        transport=transport,
        base_url='http://test',
    ) as test_client:
        yield test_client


@pytest_asyncio.fixture(scope='class')
async def api_app() -> AsyncGenerator[FastAPI]:
    """Облегченный клиент для API-контроллеров без запуска lifespan (scheduler/broker)."""
    app = FastAPI()
    app.include_router(main_router)
    yield app


@pytest_asyncio.fixture(scope='class')
async def api_async_client(api_app: FastAPI) -> AsyncGenerator[AsyncClient]:
    transport = ASGITransport(app=api_app)

    async with AsyncClient(
        transport=transport,
        base_url='http://test',
    ) as test_client:
        yield test_client


@pytest_asyncio.fixture
async def api_dependency_overrides(api_app: FastAPI) -> AsyncGenerator[dict]:
    api_app.dependency_overrides.clear()
    yield api_app.dependency_overrides
    api_app.dependency_overrides.clear()
