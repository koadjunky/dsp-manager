from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from fastapi.encoders import jsonable_encoder

from dsp_be.logic.planet import Planet
from dsp_be.logic.star import Star
from dsp_be.motor.driver import db


@dataclass
class PlanetModel:
    id: str
    name: str
    star_name: str
    resources: Dict[str, float]
    imports: List[str]
    exports: List[str]

    @classmethod
    def from_logic(cls, planet: Planet) -> "PlanetModel":
        model = PlanetModel(
            id=planet.id,
            name=planet.name,
            star_name=planet.star_name,
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
            star_name=document["star_name"],
            resources=document["resources"].copy(),
            imports=document["imports"].copy(),
            exports=document["exports"].copy(),
        )
        return model

    @classmethod
    async def create(cls, planet: Planet) -> None:
        model = PlanetModel.from_logic(planet)
        await db.planet.insert_one(jsonable_encoder(model))

    @classmethod
    async def update(cls, planet: Planet) -> None:
        model = PlanetModel.from_logic(planet)
        model_db = await db.planet.find_one({"id": model.id})
        _id = model_db["_id"]
        await db.planet.update_one({"_id": _id}, {"$set": jsonable_encoder(model)})

    @classmethod
    async def list(cls, star_name: str) -> List["PlanetModel"]:
        return [
            PlanetModel.from_dict(doc)
            async for doc in db.planet.find({"star_name": star_name})
        ]

    @classmethod
    async def find(cls, planet_name) -> Optional["PlanetModel"]:
        doc = await db.planet.find_one({"name": planet_name})
        if doc is None:
            return None
        return PlanetModel.from_dict(doc)

    @classmethod
    async def delete(cls, planet_name: str) -> None:
        await db.planet.delete_many({"name": planet_name})
