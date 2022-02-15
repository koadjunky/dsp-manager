from typing import AsyncGenerator, Callable

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from dsp_be.motor.driver import MONGODB_URL, get_db


@pytest.fixture()
def anyio_backend():
    return "asyncio"


@pytest.fixture()
async def db_session() -> AsyncIOMotorClient:
    yield AsyncIOMotorClient(MONGODB_URL)


@pytest.fixture()
def override_get_db(
    db_session: AsyncIOMotorClient,
) -> Callable[[], AsyncIOMotorDatabase]:
    async def _override_get_db() -> AsyncIOMotorDatabase:
        yield db_session.dsp_database

    return _override_get_db


@pytest.fixture()
async def app(override_get_db: Callable[[], AsyncIOMotorDatabase]) -> FastAPI:
    from dsp_be.main import get_app

    app = get_app()
    app.dependency_overrides[get_db] = override_get_db
    return app


@pytest.fixture()
async def async_client(app: FastAPI) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(autouse=True)
async def fix_database(db_session: AsyncIOMotorDatabase) -> AsyncGenerator:
    async def cleanup() -> None:
        await db_session.dsp_database.star.delete_many({"name": "Test Star"})
        await db_session.dsp_database.star.delete_many({"name": "Other Star"})
        await db_session.dsp_database.star.delete_many({"name": ""})
        await db_session.dsp_database.planet.delete_many({"name": "Test Star 3"})
        await db_session.dsp_database.planet.delete_many({"name": "Other Star 3"})
        await db_session.dsp_database.planet.delete_many({"name": ""})

    await cleanup()
    yield
    await cleanup()
