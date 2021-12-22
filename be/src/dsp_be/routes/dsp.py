from typing import List

from loguru import logger
from fastapi import APIRouter, Depends

from dsp_be.logic import get_db
from dsp_be.logic.star import Star
from dsp_be.logic.planet import Planet
from dsp_be.routes.models import StarModel, PlanetModel, FactoryModel, ProductionModel

router = APIRouter()


@router.get(
    "/api/stars",
    response_model=List[StarModel],
    dependencies=[Depends(get_db)],
    summary="Return list of all recorded star systems.",
    description="Return list of all recorded star systems.",
    response_description="Return list of all recorded star systems."
)
def get_stars() -> List[Star]:
    stars = list(Star.select())
    return stars


@router.get(
    "/api/stars/{star_id}",
    response_model=List[PlanetModel],
    dependencies=[Depends(get_db)],
    summary="Return list of all recorded planets in star sysem.",
    description="Return list of all recorded star systems.",
    response_description="Return list of all recorded star systems."
)
def get_planets(star_id:int) -> List[Planet]:
    planets = list(Planet.select().where(Planet.star_id == star_id))
    return planets


@router.get(
    "/api/stars/{star_id}/planets/{planet_id}",
    response_model=PlanetModel,
    dependencies=[Depends(get_db)],
    summary="Return planet with all factories.",
    description="Return planet with all factories.",
    response_description="Return planet with all factories.",
)
def get_planet(star_id:int, planet_id:int) -> PlanetModel:
    planet = list(Planet.select().where(Planet.star_id == star_id, Planet.id == planet_id))[0]
    factory_model_list = []
    for factory in planet.factories:
        factory_model_list.append(
            FactoryModel(
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
            ProductionModel(
                name=product,
                value=value
            )
        )
    planet_model = PlanetModel(
        id=planet.id,
        name=planet.name,
        trade=trade_model_list,
        factories = factory_model_list
    )
    return planet_model
