from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from dsp_be.logic.star import Star
from dsp_be.motor.config import ConfigRepository
from dsp_be.motor.driver import get_db
from dsp_be.motor.factory import FactoryRepository
from dsp_be.motor.planet import PlanetRepository
from dsp_be.motor.star import StarRepository
from dsp_be.routes.stars_dto import (
    PlanetDto,
    StarCreateDto,
    StarDto,
    StarUpdateDto,
    SystemDto,
)

router = APIRouter()


@router.get(
    "/",
    response_model=SystemDto,
    summary="Return list of all recorded star systems.",
    description="Return list of all recorded star systems.",
    response_description="Return list of all recorded star systems.",
)
async def get_stars(db: Any = Depends(get_db)) -> SystemDto:
    logger.info("Fetching system information")
    config = (await ConfigRepository(db).find()).to_logic()
    stars = [model.to_logic() for model in await StarRepository(db).list()]
    for star in stars:
        planets = [
            model.to_logic(star) for model in await PlanetRepository(db).list(star.name)
        ]
        for planet in planets:
            for model in await FactoryRepository(db).list(planet.id):
                model.to_logic(planet, config)
    return SystemDto.from_logic(stars)


@router.get(
    "/{star_name}",
    response_model=StarDto,
    summary="Return list of all recorded planets in star sysem.",
    description="Return list of all recorded star systems.",
    response_description="Return list of all recorded star systems.",
)
async def get_star(star_name: str, db: Any = Depends(get_db)) -> StarDto:
    logger.info(f"Fetching star {star_name} information")
    config = (await ConfigRepository(db).find()).to_logic()
    star_model = await StarRepository(db).find_name(star_name)
    if star_model is None:
        raise HTTPException(status_code=400, detail=f"Star {star_name} doesn't exist")
    star = star_model.to_logic()
    planets = [
        model.to_logic(star) for model in await PlanetRepository(db).list(star_name)
    ]
    for planet in planets:
        for model in await FactoryRepository(db).list(planet.id):
            model.to_logic(planet, config)
    return StarDto.from_logic(star)


@router.get(
    "/{star_name}/planets/{planet_name}",
    response_model=PlanetDto,
    summary="Return planet with all factories.",
    description="Return planet with all factories.",
    response_description="Return planet with all factories.",
)
async def get_planet(
    star_name: str, planet_name: str, db: Any = Depends(get_db)
) -> PlanetDto:
    logger.info(f"Fetching planet {planet_name} information")
    config = (await ConfigRepository(db).find()).to_logic()
    star_model = await StarRepository(db).find_name(star_name)
    if star_model is None:
        logger.warning(f"Star {star_name} does not exist")
        raise HTTPException(status_code=400, detail=f"Star {star_name} does not exist")
    star = star_model.to_logic()
    planet_model = await PlanetRepository(db).find_name(planet_name)
    if planet_model is None:
        logger.warning(f"Planet {planet_name} does not exist")
        raise HTTPException(
            status_code=400, detail=f"Planet {planet_name} does not exist"
        )
    planet = planet_model.to_logic(star)
    for model in await FactoryRepository(db).list(planet.id):
        model.to_logic(planet, config)
    return PlanetDto.from_logic(planet)


@router.post("/")
async def create_star(star_dto: StarCreateDto, db: Any = Depends(get_db)):
    logger.info(f"Creating star {star_dto.name}")
    star_name = await StarRepository(db).find_name(star_dto.name)
    if star_name is not None:
        raise HTTPException(
            status_code=400, detail=f"Star {star_dto.name} already exists"
        )
    star = Star(
        name=star_dto.name,
        imports=star_dto.imports,
        exports=star_dto.exports,
    )
    await StarRepository(db).create(star)


@router.put("/")
async def update_star(star_dto: StarUpdateDto, db: Any = Depends(get_db)):
    logger.info(f"Updating star {star_dto.name}")
    star_name = await StarRepository(db).find_name(star_dto.name)
    if star_name is not None and star_dto.id != star_name.id:
        raise HTTPException(
            status_code=400, detail=f"Star {star_dto.name} already exists"
        )
    star = Star(
        id=star_dto.id,
        name=star_dto.name,
        imports=star_dto.imports,
        exports=star_dto.exports,
    )
    await StarRepository(db).update(star)


@router.delete("/{star_id}")
async def delete_star(star_id: str, db: Any = Depends(get_db)):
    logger.info(f"Deleting star {star_id}")
    await StarRepository(db).delete(star_id)
