from typing import Dict, List

from pydantic import BaseModel

from dsp_be.logic.factory import Factory
from dsp_be.logic.planet import Planet


class StarDto(BaseModel):
    name: str


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
