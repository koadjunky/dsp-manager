from fastapi import APIRouter

from dsp_be.motor.config import ConfigModel
from dsp_be.motor.factory import FactoryModel
from dsp_be.motor.planet import PlanetModel
from dsp_be.motor.star import StarModel
from dsp_be.routes.stars_dto import PlanetDto, StarDto, SystemDto

router = APIRouter()


@router.get(
    "/",
    response_model=SystemDto,
    summary="Return list of all recorded star systems.",
    description="Return list of all recorded star systems.",
    response_description="Return list of all recorded star systems.",
)
async def get_stars() -> SystemDto:
    config = (await ConfigModel.find()).to_logic()
    stars = [model.to_logic() for model in await StarModel.list()]
    for star in stars:
        planets = [model.to_logic(star) for model in await PlanetModel.list(star.name)]
        for planet in planets:
            for model in await FactoryModel.list(planet.name):
                model.to_logic(planet, config)
    return SystemDto.from_logic(stars)


@router.get(
    "/{star_name}",
    response_model=StarDto,
    summary="Return list of all recorded planets in star sysem.",
    description="Return list of all recorded star systems.",
    response_description="Return list of all recorded star systems.",
)
async def get_star(star_name: str) -> StarDto:
    config = (await ConfigModel.find()).to_logic()
    star = (await StarModel.find(star_name)).to_logic()
    planets = [model.to_logic(star) for model in await PlanetModel.list(star_name)]
    for planet in planets:
        for model in await FactoryModel.list(planet.name):
            model.to_logic(planet, config)
    return StarDto.from_logic(star)


@router.get(
    "/{star_name}/planets/{planet_name}",
    response_model=PlanetDto,
    summary="Return planet with all factories.",
    description="Return planet with all factories.",
    response_description="Return planet with all factories.",
)
async def get_planet(star_name: str, planet_name: str) -> PlanetDto:
    config = (await ConfigModel.find()).to_logic()
    star = (await StarModel.find(star_name)).to_logic()
    planet = (await PlanetModel.find(planet_name)).to_logic(star)
    for model in await FactoryModel.list(planet.name):
        model.to_logic(planet, config)
    return PlanetDto.from_logic(planet)