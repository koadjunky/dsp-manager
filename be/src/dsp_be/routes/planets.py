from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from dsp_be.logic.planet import Planet
from dsp_be.motor.driver import get_db
from dsp_be.motor.planet import PlanetRepository
from dsp_be.motor.star import StarRepository
from dsp_be.routes.planets_dto import PlanetCreateDto, PlanetDeleteDto, PlanetUpdateDto

router = APIRouter()


@router.post("/")
async def create_planet(planet_dto: PlanetCreateDto, db: Any = Depends(get_db)):
    star_model = await StarRepository(db).find_name(planet_dto.star_name)
    if star_model is None:
        raise HTTPException(
            status_code=400, detail=f"Star {planet_dto.star_name} does not exist"
        )
    star = star_model.to_logic()
    planet_name = await PlanetRepository(db).find_name(planet_dto.name)
    if planet_name is not None:
        raise HTTPException(
            status_code=400, detail=f"Planet {planet_dto.name} already exists"
        )
    planet = Planet(
        name=planet_dto.name,
        resources=planet_dto.resources,
        imports=planet_dto.imports,
        exports=planet_dto.exports,
        star=star,
    )
    await PlanetRepository(db).create(planet)


# TODO: Make id key for planets
@router.put("/")
async def update_planet(planet_dto: PlanetUpdateDto, db: Any = Depends(get_db)):
    star_model = await StarRepository(db).find_name(planet_dto.star_name)
    if star_model is None:
        raise HTTPException(
            status_code=400, detail=f"Star {planet_dto.star_name} does not exist"
        )
    star = star_model.to_logic()
    planet_model = (await PlanetRepository(db).find(planet_dto.id)).to_logic(star)
    if planet_model is None:
        raise HTTPException(
            status_code=400,
            detail=f"Planet {planet_dto.id} does not exist",
        )
    planet_name = await PlanetRepository(db).find_name(planet_dto.name)
    if planet_name is not None and planet_name.id != planet_dto.id:
        raise HTTPException(
            status_code=400, detail=f"Duplicated planet name {planet_dto.name}"
        )
    planet = Planet(
        id=planet_dto.id,
        name=planet_dto.name,
        resources=planet_dto.resources,
        imports=planet_dto.imports,
        exports=planet_dto.exports,
        star=star,
    )
    await PlanetRepository(db).update(planet)


@router.delete("/")
async def delete_planet(planet_dto: PlanetDeleteDto, db: Any = Depends(get_db)):
    await PlanetRepository(db).delete(planet_dto.id)
