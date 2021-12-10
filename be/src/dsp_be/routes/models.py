from typing import Any, Dict, List

import peewee
from pydantic import BaseModel
from pydantic.utils import GetterDict


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class StarModel(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class FactoryModel(BaseModel):
    id: int
    name: str
    recipe: str
    machine: str
    count: int
    production: Dict[str, float]


class PlanetModel(BaseModel):
    id: int
    name: str
    imports: Dict[str, float]
    exports: Dict[str, float]
    factories: List[FactoryModel]

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
