from typing import Dict, List

from pydantic import BaseModel


# TODO: Check resources, imports, exports
class PlanetCreateDto(BaseModel):
    name: str
    star_name: str
    resources: Dict[str, float]
    imports: List[str]
    exports: List[str]


class PlanetUpdateDto(PlanetCreateDto):
    id: str


class PlanetDeleteDto(BaseModel):
    id: str
