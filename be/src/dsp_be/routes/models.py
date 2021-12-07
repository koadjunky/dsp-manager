from typing import Any

import peewee
from pydantic import BaseModel
from pydantic.utils import GetterDict


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class Star(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class Planet(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
