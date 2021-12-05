from typing import List

from fastapi import APIRouter, Depends

from dsp_be.logic import star, get_db
from dsp_be.routes import models

router = APIRouter()


@router.get(
    "/stars",
    response_model=List[models.Star],
    dependencies=[Depends(get_db)],
    summary="Return list of all recorded star systems.",
    description="Return list of all recorded star systems.",
    response_description="Return list of all recorded star systems."
)
def get_stars() -> List[star.Star]:
    stars = list(star.Star.select())
    return stars

