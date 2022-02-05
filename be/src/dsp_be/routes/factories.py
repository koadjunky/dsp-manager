from fastapi import APIRouter, HTTPException

from dsp_be.logic.factory import Factory
from dsp_be.motor.config import ConfigModel
from dsp_be.motor.factory import FactoryModel
from dsp_be.motor.planet import PlanetModel
from dsp_be.motor.star import StarModel
from dsp_be.routes.factories_dto import (
    FactoryCreateDto,
    FactoryDeleteDto,
    FactoryUpdateDto,
)

router = APIRouter()


# TODO: Errors, etc
@router.post("/")
async def create_factory(factory_dto: FactoryCreateDto):
    config = (await ConfigModel.find()).to_logic()
    star = (await StarModel.find(factory_dto.star_name)).to_logic()
    planet = (await PlanetModel.find(factory_dto.planet_name)).to_logic(star)
    factory_model = await FactoryModel.find_name(planet.name, factory_dto.name)
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
    await FactoryModel.create(factory)


@router.put("/")
async def update_factory(factory_dto: FactoryUpdateDto):
    config = (await ConfigModel.find()).to_logic()
    star = (await StarModel.find(factory_dto.star_name)).to_logic()
    planet = (await PlanetModel.find(factory_dto.planet_name)).to_logic(star)
    factory_model = await FactoryModel.find_id(planet.name, factory_dto.id)
    if factory_model is None:
        raise HTTPException(
            status_code=400,
            detail=f"Factory {factory_dto.name} does not exist on planet {planet.name}",
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
    await FactoryModel.update(factory)


@router.delete("/")
async def delete_factory(factory_dto: FactoryDeleteDto):
    await FactoryModel.delete_id(factory_dto.id)
