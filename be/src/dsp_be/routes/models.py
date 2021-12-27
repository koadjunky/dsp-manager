from typing import Dict, List

from pydantic import BaseModel


class StarModel(BaseModel):
    id: int
    name: str


class FactoryModel(BaseModel):
    id: int
    name: str
    recipe: str
    machine: str
    count: int
    production: Dict[str, float]


class ProductionModel(BaseModel):
    name: str
    value: float


class PlanetModel(BaseModel):
    id: int
    name: str
    trade: List[ProductionModel]
    factories: List[FactoryModel]

