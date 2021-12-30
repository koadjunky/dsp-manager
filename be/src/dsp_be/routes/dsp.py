from typing import List

from fastapi import APIRouter

from dsp_be.logic.star import Star
from dsp_be.motor import StarModel, PlanetModel, FactoryModel
from dsp_be.routes.dto import StarDto, PlanetDto

router = APIRouter()


@router.get(
    "/api/stars",
    response_model=List[StarDto],
    summary="Return list of all recorded star systems.",
    description="Return list of all recorded star systems.",
    response_description="Return list of all recorded star systems."
)
async def get_stars() -> List[Star]:
    return [model.to_logic() for model in await StarModel.list()]


@router.get(
    "/api/stars/{star_name}",
    response_model=List[PlanetDto],
    summary="Return list of all recorded planets in star sysem.",
    description="Return list of all recorded star systems.",
    response_description="Return list of all recorded star systems."
)
async def get_planets(star_name: str) -> List[PlanetDto]:
    star = (await StarModel.find(star_name)).to_logic()
    planets = [model.to_logic(star) for model in await PlanetModel.list(star_name)]
    for planet in planets:
        for model in await FactoryModel.list(planet.name):
            model.to_logic(planet)
    return [PlanetDto.from_logic(planet) for planet in planets]


@router.get(
    "/api/stars/{star_name}/planets/{planet_name}",
    response_model=PlanetDto,
    summary="Return planet with all factories.",
    description="Return planet with all factories.",
    response_description="Return planet with all factories.",
)
async def get_planet(star_name:str, planet_name:str) -> PlanetDto:
    star = (await StarModel.find(star_name)).to_logic()
    planet = (await PlanetModel.find(planet_name)).to_logic(star)
    for model in await FactoryModel.list(planet.name):
        model.to_logic(planet)
    return PlanetDto.from_logic(planet)
