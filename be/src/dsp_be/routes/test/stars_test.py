from typing import List, Optional
from unittest.mock import ANY

import pytest
from httpx import AsyncClient
from requests import Response


async def create_star(
    client: AsyncClient,
    name: str,
    imports: List[str] = None,
    exports: List[str] = None,
) -> Response:
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
) -> Response:
    imports_list = imports if imports is not None else []
    exports_list = exports if exports is not None else []
    request = {"id": id, "name": name, "imports": imports_list, "exports": exports_list}
    return await client.put("/dsp/api/stars/", json=request)


async def delete_star(client: AsyncClient, name: str) -> Optional[Response]:
    response = await read_star(client, name)
    if response.status_code != 200:
        return None
    star = response.json()
    if "id" not in star:
        return None
    id_ = star["id"]
    return await delete_star_id(client, id_)


async def delete_star_id(client: AsyncClient, id_: str) -> Response:
    return await client.delete(f"/dsp/api/stars/{id_}")


TEST_STAR = "Test Star"
TEST_STAR_1 = "Other Star"


@pytest.mark.anyio
async def test_create_star(async_client: AsyncClient) -> None:
    response = await create_star(async_client, TEST_STAR)
    assert response.status_code == 200
    response = await read_star(async_client, TEST_STAR)
    assert response.status_code == 200
    assert response.json() == {
        "name": TEST_STAR,
        "imports": [],
        "exports": [],
        "planets": [],
        "trade": {},
        "id": ANY,
    }


@pytest.mark.anyio
async def test_create_star_duplicate_name(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR, imports=["iron_ingot"])
    response = await create_star(async_client, TEST_STAR)
    assert response.status_code != 200
    response = await read_star(async_client, TEST_STAR)
    assert response.status_code == 200
    assert response.json() == {
        "name": TEST_STAR,
        "imports": ["iron_ingot"],
        "exports": [],
        "planets": [],
        "trade": {},
        "id": ANY,
    }


@pytest.mark.anyio
async def test_create_star_empty_name(async_client: AsyncClient) -> None:
    response = await create_star(async_client, "")
    assert response.status_code != 200


@pytest.mark.anyio
async def test_create_star_import_export(async_client: AsyncClient) -> None:
    response = await create_star(
        async_client, TEST_STAR, imports=["iron_ingot"], exports=["copper_ingot"]
    )
    assert response.status_code == 200
    response = await read_star(async_client, TEST_STAR)
    assert response.status_code == 200
    assert response.json() == {
        "name": TEST_STAR,
        "imports": ["iron_ingot"],
        "exports": ["copper_ingot"],
        "planets": [],
        "trade": {},
        "id": ANY,
    }


@pytest.mark.anyio
async def test_create_star_wrong_imports(async_client: AsyncClient) -> None:
    response = await create_star(async_client, TEST_STAR, imports=["bad_resource"])
    assert response.status_code != 200
    response = await read_star(async_client, TEST_STAR)
    assert response.status_code != 200


@pytest.mark.anyio
async def test_create_star_wrong_exports(async_client: AsyncClient) -> None:
    response = await create_star(async_client, TEST_STAR, exports=["bad_resource"])
    assert response.status_code != 200
    response = await read_star(async_client, TEST_STAR)
    assert response.status_code != 200


@pytest.mark.anyio
async def test_update_star(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    response = await read_star(async_client, TEST_STAR)
    id_ = response.json()["id"]
    response = await update_star(
        async_client,
        id=id_,
        name=TEST_STAR_1,
        imports=["iron_ingot"],
        exports=["copper_ingot"],
    )
    assert response.status_code == 200
    response = await read_star(async_client, TEST_STAR_1)
    assert response.status_code == 200
    assert response.json() == {
        "name": TEST_STAR_1,
        "imports": ["iron_ingot"],
        "exports": ["copper_ingot"],
        "planets": [],
        "trade": {},
        "id": ANY,
    }


@pytest.mark.anyio
async def test_update_star_duplicate_name(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR_1)
    await create_star(async_client, TEST_STAR, imports=["iron_ingot"])
    response = await read_star(async_client, TEST_STAR)
    id_ = response.json()["id"]
    response = await update_star(
        async_client,
        id=id_,
        name=TEST_STAR_1,
        imports=["iron_ingot"],
        exports=["copper_ingot"],
    )
    assert response.status_code != 200
    response = await read_star(async_client, TEST_STAR)
    assert response.status_code == 200
    assert response.json() == {
        "name": TEST_STAR,
        "imports": ["iron_ingot"],
        "exports": [],
        "planets": [],
        "trade": {},
        "id": ANY,
    }
    response = await read_star(async_client, TEST_STAR_1)
    assert response.status_code == 200
    assert response.json() == {
        "name": TEST_STAR_1,
        "imports": [],
        "exports": [],
        "planets": [],
        "trade": {},
        "id": ANY,
    }


@pytest.mark.anyio
async def test_update_star_empty_name(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    response = await read_star(async_client, TEST_STAR)
    id_ = response.json()["id"]
    response = await update_star(
        async_client, id=id_, name="", imports=["iron_ingot"], exports=["copper_ingot"]
    )
    assert response.status_code != 200
    response = await read_star(async_client, TEST_STAR)
    assert response.status_code == 200
    assert response.json() == {
        "name": TEST_STAR,
        "imports": [],
        "exports": [],
        "planets": [],
        "trade": {},
        "id": ANY,
    }


@pytest.mark.anyio
async def test_update_star_wrong_imports(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    response = await read_star(async_client, TEST_STAR)
    id_ = response.json()["id"]
    response = await update_star(
        async_client, id=id_, name=TEST_STAR, imports=["bad_resource"], exports=[]
    )
    assert response.status_code != 200
    response = await read_star(async_client, TEST_STAR)
    assert response.status_code == 200
    assert response.json() == {
        "name": TEST_STAR,
        "imports": [],
        "exports": [],
        "planets": [],
        "trade": {},
        "id": ANY,
    }


@pytest.mark.anyio
async def test_update_star_wrong_exports(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    response = await read_star(async_client, TEST_STAR)
    id_ = response.json()["id"]
    response = await update_star(
        async_client, id=id_, name=TEST_STAR, imports=[], exports=["bad_resource"]
    )
    assert response.status_code != 200
    response = await read_star(async_client, TEST_STAR)
    assert response.status_code == 200
    assert response.json() == {
        "name": TEST_STAR,
        "imports": [],
        "exports": [],
        "planets": [],
        "trade": {},
        "id": ANY,
    }


@pytest.mark.anyio
async def test_delete_star(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    response = await read_star(async_client, TEST_STAR)
    assert response.status_code == 200
    id_ = response.json()["id"]
    response = await delete_star_id(async_client, id_)
    assert response.status_code == 200
    response = await read_star(async_client, TEST_STAR)
    assert response.status_code != 200


@pytest.mark.anyio
async def test_delete_not_existing_star(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    response = await read_star(async_client, TEST_STAR)
    assert response.status_code == 200
    id_ = response.json()["id"]
    response = await delete_star_id(async_client, id_)
    assert response.status_code == 200
    response = await delete_star_id(async_client, id_)
    assert response.status_code == 200
