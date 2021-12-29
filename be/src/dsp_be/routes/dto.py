from typing import Dict, List

from pydantic import BaseModel


class StarDto(BaseModel):
    name: str


class ProductionDto(BaseModel):
    name: str
    value: float


class FactoryDto(BaseModel):
    name: str
    recipe: str
    machine: str
    count: int
    production: List[ProductionDto]


class PlanetDto(BaseModel):
    name: str
    trade: List[ProductionDto]
    factories: List[FactoryDto]

