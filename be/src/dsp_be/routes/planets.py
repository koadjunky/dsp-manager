from fastapi import APIRouter, HTTPException

from dsp_be.logic.planet import Planet
from dsp_be.motor.planet import PlanetModel
from dsp_be.motor.star import StarModel
from dsp_be.routes.planets_dto import PlanetCreateDto, PlanetDeleteDto, PlanetUpdateDto

router = APIRouter()


@router.post("/")
async def create_planet(planet_dto: PlanetCreateDto):
    star = (await StarModel.find_name(planet_dto.star_name)).to_logic()
    if star is None:
        raise HTTPException(
            status_code=400,
            detail=f"Star {planet_dto.star_name} does not exist"
        )
    planet_name = (await PlanetModel.find_name(planet_dto.name))
    if planet_name is not None:
        raise HTTPException(
            status_code=400,
            detail=f"Planet {planet_dto.name} already exists"
        )
    planet = Planet(
        name=planet_dto.name,
        resources=planet_dto.resources,
        imports=planet_dto.imports,
        exports=planet_dto.exports,
        star=star,
    )
    await PlanetModel.create(planet)


# TODO: Make id key for planets
@router.put("/")
async def update_planet(planet_dto: PlanetUpdateDto):
    star = (await StarModel.find_name(planet_dto.star_name)).to_logic()
    if star is None:
        raise HTTPException(
            status_code=400,
            detail=f"Star {planet_dto.star_name} does not exist"
        )
    planet_model = (await PlanetModel.find(planet_dto.id)).to_logic(star)
    if planet_model is None:
        raise HTTPException(
            status_code=400,
            detail=f"Planet {planet_dto.id} does not exist",
        )
    planet_name = (await PlanetModel.find_name(planet_dto.name))
    if planet_name is not None and planet_name.id != planet_dto.id:
        raise HTTPException(
            status_code=400,
            detail=f"Duplicated planet name {planet_dto.name}"
        )
    planet = Planet(
        id=planet_dto.id,
        name=planet_dto.name,
        resources=planet_dto.resources,
        imports=planet_dto.imports,
        exports=planet_dto.exports,
        star=star,
    )
    await PlanetModel.update(planet)


@router.delete("/")
async def delete_planet(planet_dto: PlanetDeleteDto):
    await PlanetModel.delete(planet_dto.name)
