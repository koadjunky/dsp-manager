from typing import Dict, List

from pydantic import BaseModel


class PlanetCreateDto(BaseModel):
    name: str
    star_name: str
    resources: Dict[str, float]
    imports: List[str]
    exports: List[str]


class PlanetUpdateDto(PlanetCreateDto):
    id: str


class PlanetDeleteDto(BaseModel):
    name: str
