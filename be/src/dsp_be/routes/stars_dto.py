from typing import Dict, List

from pydantic import BaseModel, validator

from dsp_be.logic.factory import Factory
from dsp_be.logic.planet import Planet
from dsp_be.logic.recipe import resources
from dsp_be.logic.star import Star


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
    star_name: str
    exports: List[str]
    imports: List[str]
    resources: Dict[str, float]
    trade: Dict[str, float]
    factories: List[FactoryDto]

    @classmethod
    def from_logic(cls, planet: Planet):
        factories = [FactoryDto.from_logic(factory) for factory in planet.factories]
        dto = PlanetDto(
            id=planet.id,
            name=planet.name,
            star_name=planet.star_name,
            imports=planet.imports,
            exports=planet.exports,
            resources=planet.resources,
            trade=planet.trade().to_dict(),
            factories=factories,
        )
        return dto


class StarDto(BaseModel):
    id: str
    name: str
    imports: List[str]
    exports: List[str]
    trade: Dict[str, float]
    planets: List[PlanetDto]

    @classmethod
    def from_logic(cls, star: Star):
        planets = [PlanetDto.from_logic(planet) for planet in star.planets]
        dto = StarDto(
            id=star.id,
            name=star.name,
            imports=star.imports,
            exports=star.exports,
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


class StarCreateDto(BaseModel):
    name: str
    imports: List[str]
    exports: List[str]

    @validator("name", allow_reuse=True)
    def name_must_be_not_empty(cls, name):
        if name == "":
            raise ValueError("Star name must not be empty")
        return name

    @validator("imports", allow_reuse=True)
    def imports_must_be_resources(cls, imports):
        if not set(imports).issubset(resources):
            raise ValueError("Imports must be resources")
        return imports

    @validator("exports", allow_reuse=True)
    def exports_must_be_resources(cls, exports):
        if not set(exports).issubset(resources):
            raise ValueError("Imports must be resources")
        return exports


class StarUpdateDto(StarCreateDto):
    id: str
