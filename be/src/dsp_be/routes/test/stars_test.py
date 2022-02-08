from typing import Any, AsyncGenerator, Callable, List
from unittest.mock import ANY

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
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
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


async def create_star(
    client: AsyncClient,
    name: str,
    imports: List[str] = None,
    exports: List[str] = None,
) -> Any:
    imports_list = imports if imports is not None else []
    exports_list = exports if exports is not None else []
    request = {"name": name, "imports": imports_list, "exports": exports_list}
    return await client.post("/dsp/api/stars/", json=request)


async def read_star(client: AsyncClient, name: str) -> Response:
    return await client.get(f"/dsp/api/stars/{name}")


async def update_star(
    client: AsyncClient,
    id: str,
    name: str,
    imports: List[str] = None,
    exports: List[str] = None,
) -> None:
    imports_list = imports if imports is not None else []
    exports_list = exports if exports is not None else []
    request = {"id": id, "name": name, "imports": imports_list, "exports": exports_list}
    await client.put("/dsp/api/stars/", json=request)


async def delete_star(client: AsyncClient, name: str) -> None:
    response = await read_star(client, name)
    if response.status_code != 200:
        return
    star = response.json()
    if "id" not in star:
        return
    id = star["id"]
    await client.delete(f"/dsp/api/stars/{id}")


TEST_STAR = "Test Star"


@pytest.mark.anyio
async def test_create_star(async_client: AsyncClient) -> None:
    await delete_star(async_client, TEST_STAR)
    response = await create_star(async_client, TEST_STAR)
    assert response.status_code == 200
    response = await read_star(async_client, TEST_STAR)
    assert response.status_code == 200
    assert response.json() == {"name": TEST_STAR, "imports": [], "exports": [], "planets": [], "trade": {}, "id": ANY}
    await delete_star(async_client, TEST_STAR)


@pytest.mark.anyio
async def test_create_star_duplicate_name(async_client: AsyncClient) -> None:
    await delete_star(async_client, TEST_STAR)
    await create_star(async_client, TEST_STAR, imports=["iron_ingot"])
    response = await create_star(async_client, TEST_STAR)
    assert response.status_code != 200
    response = await read_star(async_client, TEST_STAR)
    assert response.status_code == 200
    assert response.json() == {"name": TEST_STAR, "imports": ["iron_ingot"], "exports": [], "planets": [], "trade": {}, "id": ANY}
    await delete_star(async_client, TEST_STAR)


@pytest.mark.anyio
async def test_create_star_empty_name(async_client: AsyncClient) -> None:
    await delete_star(async_client, "")
    response = await create_star(async_client, "")
    assert response.status_code != 200
    await delete_star(async_client, "")


@pytest.mark.anyio
async def test_create_star_import_export(async_client: AsyncClient) -> None:
    await delete_star(async_client, TEST_STAR)
    response = await create_star(
        async_client, TEST_STAR, imports=["iron_ingot"], exports=["copper_ingot"]
    )
    assert response.status_code == 200
    response = await read_star(async_client, TEST_STAR)
    assert response.status_code == 200
    assert response.json() == {"name": TEST_STAR, "imports": ["iron_ingot"], "exports": ["copper_ingot"], "planets": [], "trade": {}, "id": ANY}
    await delete_star(async_client, TEST_STAR)


@pytest.mark.anyio
async def test_create_star_wrong_imports(async_client: AsyncClient) -> None:
    await delete_star(async_client, TEST_STAR)
    response = await create_star(async_client, TEST_STAR, imports=["bad_resource"])
    assert response.status_code != 200
    response = await read_star(async_client, TEST_STAR)
    assert response.status_code != 200


@pytest.mark.anyio
async def test_create_star_wrong_exports(async_client: AsyncClient) -> None:
    await delete_star(async_client, TEST_STAR)
    response = await create_star(async_client, TEST_STAR, exports=["bad_resource"])
    assert response.status_code != 200
    response = await read_star(async_client, TEST_STAR)
    assert response.status_code != 200
