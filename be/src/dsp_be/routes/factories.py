from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from dsp_be.logic.factory import Factory
from dsp_be.motor.config import ConfigRepository
from dsp_be.motor.driver import get_db
from dsp_be.motor.factory import FactoryRepository
from dsp_be.motor.planet import PlanetRepository
from dsp_be.motor.star import StarRepository
from dsp_be.routes.factories_dto import FactoryCreateDto, FactoryUpdateDto

router = APIRouter()


@router.post("/")
async def create_factory(factory_dto: FactoryCreateDto, db: Any = Depends(get_db)):
    logger.info(
        f"Creating factory {factory_dto.name} on planet {factory_dto.planet_name}"
    )
    config = (await ConfigRepository(db).find()).to_logic()
    star_model = await StarRepository(db).find_name(factory_dto.star_name)
    if star_model is None:
        logger.warning(f"Star {factory_dto.star_name} does not exist")
        raise HTTPException(
            status_code=400, detail=f"Star {factory_dto.star_name} does not exist"
        )
    star = star_model.to_logic()
    planet_model = await PlanetRepository(db).find_name(factory_dto.planet_name)
    if planet_model is None:
        logger.warning(f"Planet {factory_dto.planet_name} does not exit")
        raise HTTPException(
            status_code=400, detail=f"Planet {factory_dto.planet_name} does not exit"
        )
    if planet_model.star_name != star_model.name:
        logger.warning(
            f"Planet {factory_dto.planet_name} doesn't belong to star {factory_dto.star_name}"
        )
        raise HTTPException(
            status_code=400,
            detail=f"Planet {factory_dto.planet_name} doesn't belong to star {factory_dto.star_name}",
        )
    planet = planet_model.to_logic(star)
    factory_model = await FactoryRepository(db).find_name(planet.name, factory_dto.name)
    if factory_model is not None:
        raise HTTPException(
            status_code=400,
            detail=f"Factory {factory_dto.name} already exists on planet {planet.name}",
        )
    factory = Factory(
        name=factory_dto.name,
        recipe_name=factory_dto.recipe,
        machine_name=factory_dto.machine,
        count=factory_dto.count,
        planet=planet,
        config=config,
    )
    await FactoryRepository(db).create(factory)


@router.put("/")
async def update_factory(factory_dto: FactoryUpdateDto, db: Any = Depends(get_db)):
    logger.info(
        f"Updating factory {factory_dto.name} on planet {factory_dto.planet_name}"
    )
    config = (await ConfigRepository(db).find()).to_logic()
    star_model = await StarRepository(db).find_name(factory_dto.star_name)
    if star_model is None:
        logger.warning(f"Star {factory_dto.star_name} does not exist")
        raise HTTPException(
            status_code=400, detail=f"Star {factory_dto.star_name} does not exist"
        )
    star = star_model.to_logic()
    planet_model = await PlanetRepository(db).find_name(factory_dto.planet_name)
    if planet_model is None:
        logger.warning(f"Planet {factory_dto.planet_name} does not exit")
        raise HTTPException(
            status_code=400, detail=f"Planet {factory_dto.planet_name} does not exit"
        )
    if planet_model.star_name != star_model.name:
        logger.warning(
            f"Planet {factory_dto.planet_name} doesn't belong to star {factory_dto.star_name}"
        )
        raise HTTPException(
            status_code=400,
            detail=f"Planet {factory_dto.planet_name} doesn't belong to star {factory_dto.star_name}",
        )
    planet = planet_model.to_logic(star)
    factory_model = await FactoryRepository(db).find(factory_dto.id)
    if factory_model is None:
        raise HTTPException(
            status_code=400,
            detail=f"Factory {factory_dto.id} does not exist.",
        )
    factory = Factory(
        id=factory_dto.id,
        name=factory_dto.name,
        recipe_name=factory_dto.recipe,
        machine_name=factory_dto.machine,
        count=factory_dto.count,
        planet=planet,
        config=config,
    )
    await FactoryRepository(db).update(factory)


@router.delete("/{factory_id}")
async def delete_factory(factory_id: str, db: Any = Depends(get_db)):
    logger.info(f"Deleting factory {factory_id}")
    await FactoryRepository(db).delete(factory_id)
