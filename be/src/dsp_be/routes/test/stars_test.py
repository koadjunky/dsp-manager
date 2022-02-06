from typing import Any, AsyncGenerator, Callable, List

import httpx
import pytest
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from requests import Response

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
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


async def create_star(
    client: httpx.AsyncClient,
    name: str,
    imports: List[str] = None,
    exports: List[str] = None,
) -> Any:
    imports_list = imports if imports is not None else []
    exports_list = exports if exports is not None else []
    request = {"name": name, "imports": imports_list, "exports": exports_list}
    return await client.post("/dsp/api/stars/", json=request)


async def read_star(client: httpx.AsyncClient, name: str) -> Response:
    return await client.get(f"/dsp/api/stars/{name}")


async def update_star(
    client: httpx.AsyncClient,
    id: str,
    name: str,
    imports: List[str] = None,
    exports: List[str] = None,
) -> None:
    imports_list = imports if imports is not None else []
    exports_list = exports if exports is not None else []
    request = {"id": id, "name": name, "imports": imports_list, "exports": exports_list}
    await client.put("/dsp/api/stars/", json=request)


async def delete_star(client: httpx.AsyncClient, name: str) -> None:
    response = await read_star(client, name)
    if response.status_code != 200:
        return
    star = response.json()
    id = star["id"]
    await client.delete(f"/dsp/api/stars/{id}")


@pytest.mark.anyio
async def test_create_star(async_client: httpx.AsyncClient) -> None:
    await delete_star(async_client, "Test Star")
    response = await create_star(async_client, "Test Star")
    assert response.status_code == 200
