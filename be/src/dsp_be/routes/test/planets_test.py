from typing import Dict, List, Optional
from unittest.mock import ANY

import pytest
from httpx import AsyncClient
from requests import Response

from dsp_be.routes.test.stars_test import TEST_STAR, create_star


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


async def delete_planet(
    client: AsyncClient, star_name: str, planet_name: str
) -> Optional[Response]:
    response = await read_planet(client, star_name, planet_name)
    if response.status_code != 200:
        return None
    planet = response.json()
    if "id" not in planet:
        return None
    id_ = planet["id"]
    return await delete_planet_id(client, id_)


async def delete_planet_id(client: AsyncClient, id_: str) -> Response:
    return await client.delete(f"/dsp/api/planets/{id_}")


TEST_PLANET = "Test Star 3"


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
