from typing import Dict, List

from pydantic import BaseModel, validator

from dsp_be.logic.factory import Factory
from dsp_be.logic.planet import Planet
from dsp_be.logic.star import Star
from dsp_be.logic.recipe import recipes
from dsp_be.logic.machine import machines


class FactoryCreateDto(BaseModel):
    star_name: str
    planet_name: str
    name: str
    machine: str
    recipe: str
    count: int

    @validator('recipe')
    def recipe_must_be_known_and_matching_machine(cls, recipe_name, values):
        machine_name = values['machine']
        if not recipes.has(recipe_name):
            raise ValueError(f"Recipe {recipe_name} is invalid")
        recipe = recipes.get(recipe_name)
        if machine_name not in machines:
            raise ValueError(f"Machine {machine_name} is invalid")
        machine = machines[machine_name]
        if recipe.machine != machine.type:
            raise ValueError(f"Recipe {recipe_name} does not match machine {machine_name}")
        return recipe_name


class FactoryUpdateDto(FactoryCreateDto):
    id: str


class FactoryDto(BaseModel):
    id: str
    name: str
    recipe: str
    machine: str
    count: int
    production: Dict[str, float]

    @classmethod
    def from_logic(cls, factory: Factory):
        dto = FactoryDto(
            id=factory.id,
            name=factory.name,
            recipe=factory.recipe_name,
            machine=factory.machine_name,
            count=factory.count,
            production=factory.production().to_dict(),
        )
        return dto


class PlanetDto(BaseModel):
    id: str
    name: str
    trade: Dict[str, float]
    factories: List[FactoryDto]

    @classmethod
    def from_logic(cls, planet: Planet):
        factories = [FactoryDto.from_logic(factory) for factory in planet.factories]
        dto = PlanetDto(
            id=planet.id,
            name=planet.name,
            trade=planet.trade().to_dict(),
            factories=factories,
        )
        return dto


class StarDto(BaseModel):
    id: str
    name: str
    trade: Dict[str, float]
    planets: List[PlanetDto]

    @classmethod
    def from_logic(cls, star: Star):
        planets = [PlanetDto.from_logic(planet) for planet in star.planets]
        dto = StarDto(
            id=star.id,
            name=star.name,
            trade=star.trade().to_dict(),
            planets=planets,
        )
        return dto


class SystemDto(BaseModel):
    stars: List[StarDto]

    @classmethod
    def from_logic(cls, star_list: List[Star]):
        stars = [StarDto.from_logic(star) for star in star_list]
        dto = SystemDto(
            stars=stars,
        )
        return dto
