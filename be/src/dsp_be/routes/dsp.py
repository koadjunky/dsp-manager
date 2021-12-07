from typing import List

from fastapi import APIRouter, Depends

from dsp_be.logic import star, planet, get_db
from dsp_be.routes import models

router = APIRouter()


@router.get(
    "/api/stars",
    response_model=List[models.Star],
    dependencies=[Depends(get_db)],
    summary="Return list of all recorded star systems.",
    description="Return list of all recorded star systems.",
    response_description="Return list of all recorded star systems."
)
def get_stars() -> List[star.Star]:
    stars = list(star.Star.select())
    return stars


@router.get(
    "/api/stars/{star_id}",
    response_model=List[models.Planet],
    dependencies=[Depends(get_db)],
    summary="Return list of all recorded planets in star sysem.",
    description="Return list of all recorded star systems.",
    response_description="Return list of all recorded star systems."
)
def get_planets(star_id:int) -> List[planet.Planet]:
    planets = list(planet.Planet.select().where(planet.Planet.star_id == star_id))
    return planets
