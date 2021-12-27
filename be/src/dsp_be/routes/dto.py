from typing import Dict, List

from pydantic import BaseModel


class StarDto(BaseModel):
    name: str


class FactoryDto(BaseModel):
    name: str
    recipe: str
    machine: str
    count: int
    production: Dict[str, float]


class ProductionDto(BaseModel):
    name: str
    value: float


class PlanetDto(BaseModel):
    name: str
    trade: List[ProductionDto]
    factories: List[FactoryDto]

