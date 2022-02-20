from typing import Any, Dict, Optional
from unittest.mock import ANY

import pytest
from httpx import AsyncClient
from requests import Response

from dsp_be.routes.test.planets_test import TEST_PLANET, TEST_PLANET_1, create_planet
from dsp_be.routes.test.stars_test import TEST_STAR, TEST_STAR_1, create_star


async def create_factory(
    client: AsyncClient,
    star_name: str,
    planet_name: str,
    name: str,
    machine: str = "matrix_lab",
    recipe: str = "green_science",
    count: int = 24,
) -> Response:
    request = {
        "star_name": star_name,
        "planet_name": planet_name,
        "name": name,
        "machine": machine,
        "recipe": recipe,
        "count": count,
    }
    return await client.post("/dsp/api/factories/", json=request)


async def read_factory(
    client: AsyncClient, star_name: str, planet_name: str, name: str
) -> Optional[Dict[str, Any]]:
    response = await client.get(f"/dsp/api/stars/{star_name}/planets/{planet_name}")
    if response.status_code != 200:
        return None
    factories = response.json()["factories"]
    filtered = list(filter(lambda f: f["name"] == name, factories))
    if not filtered:
        return None
    return filtered[0]


async def update_factory(
    client: AsyncClient,
    id_: str,
    star_name: str,
    planet_name: str,
    name: str,
    machine: str = "matrix_lab",
    recipe: str = "green_science",
    count: int = 1,
) -> Response:
    request = {
        "id": id_,
        "name": name,
        "planet_name": planet_name,
        "star_name": star_name,
        "machine": machine,
        "recipe": recipe,
        "count": count,
    }
    return await client.put("/dsp/api/factories/", json=request)


async def delete_factory_id(client: AsyncClient, id_: str) -> Response:
    return await client.delete(f"/dsp/api/factories/{id_}")


TEST_FACTORY = "Green Science #1"
TEST_FACTORY_1 = "Red Science #1"


@pytest.mark.anyio
async def test_create_factory(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    await create_planet(async_client, TEST_STAR, TEST_PLANET)
    response = await create_factory(async_client, TEST_STAR, TEST_PLANET, TEST_FACTORY)
    assert response.status_code == 200
    factory = await read_factory(async_client, TEST_STAR, TEST_PLANET, TEST_FACTORY)
    assert factory == {
        "name": TEST_FACTORY,
        "planet_name": TEST_PLANET,
        "star_name": TEST_STAR,
        "machine": "matrix_lab",
        "recipe": "green_science",
        "count": 24,
        "id": ANY,
        "production": {
            "graviton_lens": -1.0,
            "green_science": 2.0,
            "quantum_chip": -1.0,
        },
    }


@pytest.mark.anyio
async def test_create_factory_empty_name(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    await create_planet(async_client, TEST_STAR, TEST_PLANET)
    response = await create_factory(async_client, TEST_STAR, TEST_PLANET, "")
    assert response.status_code != 200


@pytest.mark.anyio
async def test_create_factory_wrong_star(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    await create_planet(async_client, TEST_STAR, TEST_PLANET)
    response = await create_factory(
        async_client, TEST_STAR_1, TEST_PLANET, TEST_FACTORY
    )
    assert response.status_code != 200


@pytest.mark.anyio
async def test_create_factory_wrong_planet(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    await create_planet(async_client, TEST_STAR, TEST_PLANET)
    response = await create_factory(
        async_client, TEST_STAR, TEST_PLANET_1, TEST_FACTORY
    )
    assert response.status_code != 200


@pytest.mark.anyio
async def test_create_factory_star_planet_mismatch(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    await create_star(async_client, TEST_STAR_1)
    await create_planet(async_client, TEST_STAR, TEST_PLANET)
    response = await create_factory(
        async_client, TEST_STAR_1, TEST_PLANET, TEST_FACTORY
    )
    assert response.status_code != 200


@pytest.mark.anyio
async def test_create_factory_wrong_machine(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    await create_planet(async_client, TEST_STAR, TEST_PLANET)
    response = await create_factory(
        async_client, TEST_STAR, TEST_PLANET, TEST_FACTORY, machine="bad"
    )
    assert response.status_code != 200


@pytest.mark.anyio
async def test_create_factory_wrong_recipe(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    await create_planet(async_client, TEST_STAR, TEST_PLANET)
    response = await create_factory(
        async_client, TEST_STAR, TEST_PLANET, TEST_FACTORY, recipe="bad"
    )
    assert response.status_code != 200


@pytest.mark.anyio
async def test_create_factory_recipe_mismatch(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    await create_planet(async_client, TEST_STAR, TEST_PLANET)
    response = await create_factory(
        async_client, TEST_STAR, TEST_PLANET, TEST_FACTORY, machine="oil_extractor"
    )
    assert response.status_code != 200


@pytest.mark.anyio
async def test_create_factory_wrong_count(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    await create_planet(async_client, TEST_STAR, TEST_PLANET)
    response = await create_factory(
        async_client, TEST_STAR, TEST_PLANET, TEST_FACTORY, count=0
    )
    assert response.status_code != 200


@pytest.mark.anyio
async def test_update_factory(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    await create_star(async_client, TEST_STAR_1)
    await create_planet(async_client, TEST_STAR, TEST_PLANET)
    await create_planet(async_client, TEST_STAR_1, TEST_PLANET_1)
    await create_factory(async_client, TEST_STAR, TEST_PLANET, TEST_FACTORY)
    factory = await read_factory(async_client, TEST_STAR, TEST_PLANET, TEST_FACTORY)
    id_ = factory["id"]
    response = await update_factory(
        client=async_client,
        id_=id_,
        star_name=TEST_STAR_1,
        planet_name=TEST_PLANET_1,
        name=TEST_FACTORY_1,
        machine="assembler1",
        recipe="solar_sail",
        count=4,
    )
    assert response.status_code == 200
    factory = await read_factory(
        async_client, TEST_STAR_1, TEST_PLANET_1, TEST_FACTORY_1
    )
    assert factory == {
        "star_name": TEST_STAR_1,
        "planet_name": TEST_PLANET_1,
        "name": TEST_FACTORY_1,
        "machine": "assembler1",
        "recipe": "solar_sail",
        "count": 4,
        "id": ANY,
        "production": {
            "graphene": -0.75,
            "photon_combiner": -0.75,
            "solar_sail": 1.5,
        },
    }


@pytest.mark.anyio
async def test_update_factory_wrong_star(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    await create_planet(async_client, TEST_STAR, TEST_PLANET)
    await create_factory(async_client, TEST_STAR, TEST_PLANET, TEST_FACTORY)
    factory = await read_factory(async_client, TEST_STAR, TEST_PLANET, TEST_FACTORY)
    id_ = factory["id"]
    response = await update_factory(
        client=async_client,
        id_=id_,
        star_name=TEST_STAR_1,
        planet_name=TEST_PLANET,
        name=TEST_FACTORY,
    )
    assert response.status_code != 200


@pytest.mark.anyio
async def test_update_factory_wrong_planet(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    await create_planet(async_client, TEST_STAR, TEST_PLANET)
    await create_factory(async_client, TEST_STAR, TEST_PLANET, TEST_FACTORY)
    factory = await read_factory(async_client, TEST_STAR, TEST_PLANET, TEST_FACTORY)
    id_ = factory["id"]
    response = await update_factory(
        client=async_client,
        id_=id_,
        star_name=TEST_STAR,
        planet_name=TEST_PLANET_1,
        name=TEST_FACTORY,
    )
    assert response.status_code != 200


@pytest.mark.anyio
async def test_update_factory_star_planet_mismatch(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    await create_star(async_client, TEST_STAR_1)
    await create_planet(async_client, TEST_STAR, TEST_PLANET)
    await create_factory(async_client, TEST_STAR, TEST_PLANET, TEST_FACTORY)
    factory = await read_factory(async_client, TEST_STAR, TEST_PLANET, TEST_FACTORY)
    id_ = factory["id"]
    response = await update_factory(
        client=async_client,
        id_=id_,
        star_name=TEST_STAR_1,
        planet_name=TEST_PLANET,
        name=TEST_FACTORY,
    )
    assert response.status_code != 200


@pytest.mark.anyio
async def test_update_factory_empty_name(async_client: AsyncClient) -> None:
    await create_star(async_client, TEST_STAR)
    await create_planet(async_client, TEST_STAR, TEST_PLANET)
    await create_factory(async_client, TEST_STAR, TEST_PLANET, TEST_FACTORY)
    factory = await read_factory(async_client, TEST_STAR, TEST_PLANET, TEST_FACTORY)
    id_ = factory["id"]
    response = await update_factory(
        client=async_client,
        id_=id_,
        star_name=TEST_STAR,
        planet_name=TEST_PLANET,
        name="",
    )
    assert response.status_code != 200
