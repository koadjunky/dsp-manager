from typing import Dict, List

from pydantic import BaseModel, validator

from dsp_be.logic.recipe import resources


class PlanetCreateDto(BaseModel):
    name: str
    star_name: str
    resources: Dict[str, float]
    imports: List[str]
    exports: List[str]

    @validator("name", allow_reuse=True)
    def name_must_be_not_empty(cls, name):
        if name == "":
            raise ValueError("Planet name must not be empty")
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

    @validator("resources", allow_reuse=True)
    def resources_must_be_resources(cls, res):
        if not set(res.keys()).issubset(resources):
            raise ValueError("Resources must be resources")
        return res


class PlanetUpdateDto(PlanetCreateDto):
    id: str


class PlanetDeleteDto(BaseModel):
    id: str
