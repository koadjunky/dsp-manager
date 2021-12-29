from typing import List

from fastapi import APIRouter

from dsp_be.logic.star import Star
from dsp_be.logic.planet import Planet
from dsp_be.motor import StarModel, PlanetModel, FactoryModel
from dsp_be.routes.dto import StarDto, PlanetDto, FactoryDto, ProductionDto

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
    "/api/stars/{star_id}/planets/{planet_id}",
    response_model=PlanetDto,
    summary="Return planet with all factories.",
    description="Return planet with all factories.",
    response_description="Return planet with all factories.",
)
def get_planet(star_id:int, planet_id:int) -> PlanetDto:
    planet = list(Planet.select().where(Planet.star_id == star_id, Planet.id == planet_id))[0]
    factory_model_list = []
    for factory in planet.factories:
        factory_model_list.append(
            FactoryDto(
                id=factory.id,
                name=factory.name,
                recipe=factory.recipe_name,
                machine=factory.machine_name,
                count=factory.count,
                production=factory.production().to_dict()
            )
        )
    trade_model_list = []
    for product, value in planet.trade().to_list():
        trade_model_list.append(
            ProductionDto(
                name=product,
                value=value
            )
        )
    planet_model = PlanetDto(
        id=planet.id,
        name=planet.name,
        trade=trade_model_list,
        factories = factory_model_list
    )
    return planet_model
