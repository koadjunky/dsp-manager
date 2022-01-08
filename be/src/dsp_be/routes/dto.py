from typing import Dict, List

from pydantic import BaseModel

from dsp_be.logic.factory import Factory
from dsp_be.logic.planet import Planet
from dsp_be.logic.star import Star


class FactoryDto(BaseModel):
    name: str
    recipe: str
    machine: str
    count: int
    production: Dict[str, float]

    @classmethod
    def from_logic(cls, factory: Factory):
        dto = FactoryDto(
            name=factory.name,
            recipe=factory.recipe_name,
            machine=factory.machine_name,
            count=factory.count,
            production=factory.production().to_dict(),
        )
        return dto


class PlanetDto(BaseModel):
    name: str
    trade: Dict[str, float]
    factories: List[FactoryDto]

    @classmethod
    def from_logic(cls, planet: Planet):
        factories = [FactoryDto.from_logic(factory) for factory in planet.factories]
        dto = PlanetDto(
            name=planet.name,
            trade=planet.trade().to_dict(),
            factories=factories,
        )
        return dto


class StarDto(BaseModel):
    name: str
    trade: Dict[str, float]
    planets: List[PlanetDto]

    @classmethod
    def from_logic(cls, star: Star):
        planets = [PlanetDto.from_logic(planet) for planet in star.planets]
        dto = StarDto(
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
