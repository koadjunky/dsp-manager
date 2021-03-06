from typing import Dict, List
from unittest.mock import ANY

import pytest
from httpx import AsyncClient
from requests import Response

from dsp_be.routes.test.stars_test import TEST_STAR, TEST_STAR_1, create_star


async def create_planet(
    client: AsyncClient,
    star_name: str,
    planet_name: str,
    resources: Dict[str, float] = None,
    imports: List[str] = None,
    exports: List[str] = None,
) -> Response:
    imports_list = imports if imports is not None else []
    exports_list = exports if exports is not None else []
    resources_dict = resources if resources is not None else {}
    request = {
        "name": planet_name,
        "star_name": star_name,
        "resources": resources_dict,
        "imports": imports_list,
        "exports": exports_list,
    }
    return await client.post("/dsp/api/planets/", json=request)


async def read_planet(
    client: AsyncClient, star_name: str, planet_name: str
) -> Response:
    return await client.get(f"/dsp/api/stars/{star_name}/planets/{planet_name}")


async def update_planet(
    client: AsyncClient,
    id_: str,
    star_name: str,
    name: str,
    resources: Dict[str, float],
    imports: List[str] = None,
    exports: List[str] = None,
) -> Response:
    imports_list = imports if imports is not None else []
    exports_list = exports if exports is not None else []
    resources_dict = resources if resources is not None else {}
    request = {
        "id": id_,
        "name": name,
        "star_name": star_name,
        "resources": resources_dict,
        "imports": imports_list,
        "exports": exports_list,
    }
    return await client.put("/dsp/api/planets/", json=request)


async def delete_planet_id(client: AsyncClient, id_: str) -> Response:
    return await client.delete(f"/dsp/api/planets/{id_}")


TEST_PLANET = "Test Star 3"
TEST_PLANET_1 = "Other Star 3"


@pytest.mark.anyio
async def test_create_planet(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    response = await create_planet(
        async_client, star_name=TEST_STAR, planet_name=TEST_PLANET
    )
    assert response.status_code == 200
    response = await read_planet(
        async_client, star_name=TEST_STAR, planet_name=TEST_PLANET
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": TEST_PLANET,
        "star_name": TEST_STAR,
        "resources": {},
        "imports": [],
        "exports": [],
        "id": ANY,
        "factories": [],
        "trade": {},
    }


@pytest.mark.anyio
async def test_create_planet_duplicate_name(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    response = await create_planet(
        async_client,
        TEST_STAR,
        TEST_PLANET,
        resources={"hydrogen": 10.0},
        imports=["iron_ingot"],
        exports=["processor"],
    )
    assert response.status_code == 200
    response = await create_planet(async_client, TEST_STAR, TEST_PLANET)
    assert response.status_code != 200
    response = await read_planet(async_client, TEST_STAR, TEST_PLANET)
    assert response.status_code == 200
    assert response.json() == {
        "name": TEST_PLANET,
        "star_name": TEST_STAR,
        "resources": {"hydrogen": 10.0},
        "imports": ["iron_ingot"],
        "exports": ["processor"],
        "factories": [],
        "trade": {},
        "id": ANY,
    }


@pytest.mark.anyio
async def test_create_planet_empty_name(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    response = await create_planet(async_client, TEST_STAR, "")
    assert response.status_code != 200


@pytest.mark.anyio
async def test_create_planet_import_export(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    response = await create_planet(
        async_client,
        TEST_STAR,
        TEST_PLANET,
        imports=["iron_ingot"],
        exports=["copper_ingot"],
        resources={"hydrogen": 10.0},
    )
    assert response.status_code == 200
    response = await read_planet(async_client, TEST_STAR, TEST_PLANET)
    assert response.status_code == 200
    assert response.json() == {
        "name": TEST_PLANET,
        "star_name": TEST_STAR,
        "imports": ["iron_ingot"],
        "exports": ["copper_ingot"],
        "resources": {"hydrogen": 10.0},
        "factories": [],
        "trade": {},
        "id": ANY,
    }


@pytest.mark.anyio
async def test_create_planet_wrong_imports(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    response = await create_planet(
        async_client, TEST_STAR, TEST_PLANET, imports=["bad_resource"]
    )
    assert response.status_code != 200
    response = await read_planet(async_client, TEST_STAR, TEST_PLANET)
    assert response.status_code != 200


@pytest.mark.anyio
async def test_create_planet_wrong_exports(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    response = await create_planet(
        async_client, TEST_STAR, TEST_PLANET, exports=["bad_resource"]
    )
    assert response.status_code != 200
    response = await read_planet(async_client, TEST_STAR, TEST_PLANET)
    assert response.status_code != 200


@pytest.mark.anyio
async def test_create_planet_wrong_resources(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    response = await create_planet(
        async_client, TEST_STAR, TEST_PLANET, resources={"bad_resource": 10.0}
    )
    assert response.status_code != 200
    response = await read_planet(async_client, TEST_STAR, TEST_PLANET)
    assert response.status_code != 200


@pytest.mark.anyio
async def test_update_planet(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    await create_star(async_client, TEST_STAR_1)
    await create_planet(async_client, TEST_STAR, TEST_PLANET)
    response = await read_planet(async_client, TEST_STAR, TEST_PLANET)
    id_ = response.json()["id"]
    response = await update_planet(
        async_client,
        id_=id_,
        name=TEST_PLANET_1,
        star_name=TEST_STAR_1,
        imports=["iron_ingot"],
        exports=["copper_ingot"],
        resources={"deuterium": 10.0},
    )
    assert response.status_code == 200
    response = await read_planet(async_client, TEST_STAR_1, TEST_PLANET_1)
    assert response.status_code == 200
    assert response.json() == {
        "name": TEST_PLANET_1,
        "star_name": TEST_STAR_1,
        "imports": ["iron_ingot"],
        "exports": ["copper_ingot"],
        "resources": {"deuterium": 10.0},
        "factories": [],
        "trade": {},
        "id": ANY,
    }


@pytest.mark.anyio
async def test_update_planet_duplicate_name(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    await create_planet(async_client, TEST_STAR, TEST_PLANET_1)
    await create_planet(async_client, TEST_STAR, TEST_PLANET, imports=["iron_ingot"])
    response = await read_planet(async_client, TEST_STAR, TEST_PLANET)
    id_ = response.json()["id"]
    response = await update_planet(
        async_client,
        id_=id_,
        name=TEST_PLANET_1,
        star_name=TEST_STAR,
        imports=["iron_ingot"],
        exports=["copper_ingot"],
        resources={"hydrogen": 1.0},
    )
    assert response.status_code != 200
    response = await read_planet(async_client, TEST_STAR, TEST_PLANET)
    assert response.status_code == 200
    assert response.json() == {
        "name": TEST_PLANET,
        "star_name": TEST_STAR,
        "imports": ["iron_ingot"],
        "exports": [],
        "resources": {},
        "factories": [],
        "trade": {},
        "id": ANY,
    }
    response = await read_planet(async_client, TEST_STAR, TEST_PLANET_1)
    assert response.status_code == 200
    assert response.json() == {
        "name": TEST_PLANET_1,
        "star_name": TEST_STAR,
        "imports": [],
        "exports": [],
        "resources": {},
        "factories": [],
        "trade": {},
        "id": ANY,
    }


@pytest.mark.anyio
async def test_update_planet_empty_name(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    await create_planet(async_client, TEST_STAR, TEST_PLANET, imports=["iron_ingot"])
    response = await read_planet(async_client, TEST_STAR, TEST_PLANET)
    id_ = response.json()["id"]
    response = await update_planet(
        async_client,
        id_=id_,
        name="",
        star_name=TEST_STAR,
        imports=["iron_ingot"],
        exports=["copper_ingot"],
        resources={"hydrogen": 1.0},
    )
    assert response.status_code != 200
    response = await read_planet(async_client, TEST_STAR, TEST_PLANET)
    assert response.status_code == 200
    assert response.json() == {
        "name": TEST_PLANET,
        "star_name": TEST_STAR,
        "imports": ["iron_ingot"],
        "exports": [],
        "resources": {},
        "factories": [],
        "trade": {},
        "id": ANY,
    }


@pytest.mark.anyio
async def test_update_planet_empty_star(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    await create_planet(async_client, TEST_STAR, TEST_PLANET, imports=["iron_ingot"])
    response = await read_planet(async_client, TEST_STAR, TEST_PLANET)
    id_ = response.json()["id"]
    response = await update_planet(
        async_client,
        id_=id_,
        name=TEST_PLANET,
        star_name=TEST_STAR_1,
        imports=["iron_ingot"],
        exports=["copper_ingot"],
        resources={"hydrogen": 1.0},
    )
    assert response.status_code != 200
    response = await read_planet(async_client, TEST_STAR, TEST_PLANET)
    assert response.status_code == 200
    assert response.json() == {
        "name": TEST_PLANET,
        "star_name": TEST_STAR,
        "imports": ["iron_ingot"],
        "exports": [],
        "resources": {},
        "factories": [],
        "trade": {},
        "id": ANY,
    }


@pytest.mark.anyio
async def test_update_planet_no_star(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    await create_planet(async_client, TEST_STAR, TEST_PLANET, imports=["iron_ingot"])
    response = await read_planet(async_client, TEST_STAR, TEST_PLANET)
    id_ = response.json()["id"]
    response = await update_planet(
        async_client,
        id_=id_,
        name=TEST_PLANET,
        star_name="",
        imports=["iron_ingot"],
        exports=["copper_ingot"],
        resources={"hydrogen": 1.0},
    )
    assert response.status_code != 200
    response = await read_planet(async_client, TEST_STAR, TEST_PLANET)
    assert response.status_code == 200
    assert response.json() == {
        "name": TEST_PLANET,
        "star_name": TEST_STAR,
        "imports": ["iron_ingot"],
        "exports": [],
        "resources": {},
        "factories": [],
        "trade": {},
        "id": ANY,
    }


@pytest.mark.anyio
async def test_update_planet_wrong_imports(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    await create_planet(async_client, TEST_STAR, TEST_PLANET, imports=["iron_ingot"])
    response = await read_planet(async_client, TEST_STAR, TEST_PLANET)
    id_ = response.json()["id"]
    response = await update_planet(
        async_client,
        id_=id_,
        name=TEST_PLANET,
        star_name=TEST_STAR,
        imports=["wrong_resource"],
        exports=[],
        resources={},
    )
    assert response.status_code != 200
    response = await read_planet(async_client, TEST_STAR, TEST_PLANET)
    assert response.status_code == 200
    assert response.json() == {
        "name": TEST_PLANET,
        "star_name": TEST_STAR,
        "imports": ["iron_ingot"],
        "exports": [],
        "resources": {},
        "factories": [],
        "trade": {},
        "id": ANY,
    }


@pytest.mark.anyio
async def test_update_planet_wrong_exports(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    await create_planet(async_client, TEST_STAR, TEST_PLANET, imports=["iron_ingot"])
    response = await read_planet(async_client, TEST_STAR, TEST_PLANET)
    id_ = response.json()["id"]
    response = await update_planet(
        async_client,
        id_=id_,
        name=TEST_PLANET,
        star_name=TEST_STAR,
        imports=[],
        exports=["wrong_resource"],
        resources={},
    )
    assert response.status_code != 200
    response = await read_planet(async_client, TEST_STAR, TEST_PLANET)
    assert response.status_code == 200
    assert response.json() == {
        "name": TEST_PLANET,
        "star_name": TEST_STAR,
        "imports": ["iron_ingot"],
        "exports": [],
        "resources": {},
        "factories": [],
        "trade": {},
        "id": ANY,
    }


@pytest.mark.anyio
async def test_update_planet_wrong_resources(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    await create_planet(async_client, TEST_STAR, TEST_PLANET, imports=["iron_ingot"])
    response = await read_planet(async_client, TEST_STAR, TEST_PLANET)
    id_ = response.json()["id"]
    response = await update_planet(
        async_client,
        id_=id_,
        name=TEST_PLANET,
        star_name=TEST_STAR,
        imports=[],
        exports=[],
        resources={"wrong_resource": 10.0},
    )
    assert response.status_code != 200
    response = await read_planet(async_client, TEST_STAR, TEST_PLANET)
    assert response.status_code == 200
    assert response.json() == {
        "name": TEST_PLANET,
        "star_name": TEST_STAR,
        "imports": ["iron_ingot"],
        "exports": [],
        "resources": {},
        "factories": [],
        "trade": {},
        "id": ANY,
    }


@pytest.mark.anyio
async def test_delete_planet(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    await create_planet(async_client, TEST_STAR, TEST_PLANET, imports=["iron_ingot"])
    response = await read_planet(async_client, TEST_STAR, TEST_PLANET)
    assert response.status_code == 200
    id_ = response.json()["id"]
    response = await delete_planet_id(async_client, id_)
    assert response.status_code == 200
    response = await read_planet(async_client, TEST_STAR, TEST_PLANET)
    assert response.status_code != 200


@pytest.mark.anyio
async def test_delete_not_existing_planet(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    await create_planet(async_client, TEST_STAR, TEST_PLANET, imports=["iron_ingot"])
    response = await read_planet(async_client, TEST_STAR, TEST_PLANET)
    assert response.status_code == 200
    id_ = response.json()["id"]
    response = await delete_planet_id(async_client, id_)
    assert response.status_code == 200
    response = await delete_planet_id(async_client, id_)
    assert response.status_code == 200
