from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase

from dsp_be.logic.planet import Planet
from dsp_be.logic.star import Star


@dataclass
class PlanetModel:
    id: str
    name: str
    star_id: str
    resources: Dict[str, float]
    imports: List[str]
    exports: List[str]

    @classmethod
    def from_logic(cls, planet: Planet) -> "PlanetModel":
        model = PlanetModel(
            id=planet.id,
            name=planet.name,
            star_id=planet.star_id,
            resources=planet.resources.copy(),
            imports=planet.imports.copy(),
            exports=planet.exports.copy(),
        )
        return model

    def to_logic(self, star: Star) -> Planet:
        planet = Planet(
            id=self.id,
            name=self.name,
            resources=self.resources.copy(),
            imports=self.imports.copy(),
            exports=self.exports.copy(),
            star=star,
        )
        return planet

    @classmethod
    def from_dict(cls, document: Dict[str, Any]) -> "PlanetModel":
        model = PlanetModel(
            id=document["id"],
            name=document["name"],
            star_id=document["star_id"],
            resources=document["resources"].copy(),
            imports=document["imports"].copy(),
            exports=document["exports"].copy(),
        )
        return model


class PlanetRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def create(self, planet: Planet) -> None:
        model = PlanetModel.from_logic(planet)
        await self.db.planet.insert_one(jsonable_encoder(model))

    async def update(self, planet: Planet) -> None:
        model = PlanetModel.from_logic(planet)
        model_db = await self.db.planet.find_one({"id": model.id})
        _id = model_db["_id"]
        await self.db.planet.update_one({"_id": _id}, {"$set": jsonable_encoder(model)})

    async def list(self, star_name: str) -> List["PlanetModel"]:
        return [
            PlanetModel.from_dict(doc)
            async for doc in self.db.planet.find({"star_name": star_name})
        ]

    async def find(self, planet_id: str) -> Optional["PlanetModel"]:
        doc = await self.db.planet.find_one({"id": planet_id})
        if doc is None:
            return None
        return PlanetModel.from_dict(doc)

    async def find_name(self, planet_name: str) -> Optional["PlanetModel"]:
        doc = await self.db.planet.find_one({"name": planet_name})
        if doc is None:
            return None
        return PlanetModel.from_dict(doc)

    async def delete(self, planet_id: str) -> None:
        await self.db.planet.delete_many({"id": planet_id})
