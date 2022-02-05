from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from fastapi.encoders import jsonable_encoder

from dsp_be.logic.star import Star
from dsp_be.motor.driver import db


@dataclass
class StarModel:
    id: str
    name: str
    imports: List[str]
    exports: List[str]

    @classmethod
    def from_logic(cls, star: Star) -> "StarModel":
        model = StarModel(
            id=star.id,
            name=star.name,
            imports=star.imports.copy(),
            exports=star.exports.copy(),
        )
        return model

    def to_logic(self) -> Star:
        star = Star(
            id=self.id,
            name=self.name,
            imports=self.imports.copy(),
            exports=self.exports.copy(),
        )
        return star

    @classmethod
    def from_dict(cls, document: Dict[str, Any]) -> "StarModel":
        model = StarModel(
            id=document["id"],
            name=document["name"],
            imports=document["imports"].copy(),
            exports=document["exports"].copy(),
        )
        return model

    @classmethod
    async def create(cls, star: Star) -> None:
        model = StarModel.from_logic(star)
        await db.star.insert_one(jsonable_encoder(model))

    @classmethod
    async def update(cls, star: Star) -> None:
        model = StarModel.from_logic(star)
        model_db = await db.star.find_one({"id": model.id})
        _id = model_db["_id"]
        await db.star.update_one({"_id": _id}, {"$set": jsonable_encoder(model)})

    @classmethod
    async def list(cls) -> List["StarModel"]:
        return [StarModel.from_dict(doc) async for doc in db.star.find()]

    @classmethod
    async def find(cls, star_id: str) -> Optional["StarModel"]:
        doc = await db.star.find_one({"id": star_id})
        if doc is None:
            return None
        return StarModel.from_dict(doc)

    @classmethod
    async def find_name(cls, star_name: str) -> Optional["StarModel"]:
        doc = await db.star.find_one({"name": star_name})
        if doc is None:
            return None
        return StarModel.from_dict(doc)
