from dataclasses import dataclass, field
from typing import Dict, List, Any

import motor.motor_asyncio
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from loguru import logger

from dsp_be.logic.factory import Factory
from dsp_be.logic.planet import Planet
from dsp_be.logic.star import Star

MONGODB_URL = "mongodb://root:ChangeMe@localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client.dsp_database


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


@dataclass
class FactoryModel:
    name: str
    planet_name: str
    recipe_name: str
    machine_name: str
    count: int

    @classmethod
    def from_logic(cls, factory: Factory) -> 'FactoryModel':
        model = FactoryModel(
            planet_name=factory.planet_name,
            name=factory.name,
            recipe_name=factory.recipe_name,
            machine_name=factory.machine_name,
            count=factory.count,
        )
        return model

    def to_logic(self, planet: Planet):
        factory = Factory(
            name=self.name,
            recipe_name=self.recipe_name,
            machine_name=self.machine_name,
            count=self.count,
            planet=planet
        )
        return factory

    @classmethod
    def from_dict(cls, document: Dict[str, Any]) -> 'FactoryModel':
        model = FactoryModel(
            name=document["name"],
            planet_name=document["planet_name"],
            recipe_name=document["recipe_name"],
            machine_name=document["machine_name"],
            count=document["count"],
        )
        return model

    @classmethod
    async def update(cls, factory: Factory) -> None:
        model = FactoryModel.from_logic(factory)
        if (model_db := await db.factory.find_one({"name": model.name})) is not None:
            _id = model_db["_id"]
            await db.factory.update_one({"_id": _id}, {"$set": jsonable_encoder(model)})
        else:
            await db.factory.insert_one(jsonable_encoder(model))

    @classmethod
    async def list(cls, planet_name: str) -> List['FactoryModel']:
        return [FactoryModel.from_dict(doc) async for doc in db.factory.find({"planet_name": planet_name})]



@dataclass
class PlanetModel:
    name: str
    star_name: str
    resources: Dict[str, float]
    imports: List[str]
    exports: List[str]

    @classmethod
    def from_logic(cls, planet: Planet) -> 'PlanetModel':
        model = PlanetModel(
            name=planet.name,
            star_name=planet.star_name,
            resources=planet.resources.copy(),
            imports=planet.imports.copy(),
            exports=planet.exports.copy(),
        )
        return model

    def to_logic(self, star: Star) -> Planet:
        planet = Planet(
            name=self.name,
            resources=self.resources.copy(),
            imports=self.imports.copy(),
            exports=self.exports.copy(),
            star=star,
        )
        return planet

    @classmethod
    def from_dict(cls, document: Dict[str, Any]) -> 'PlanetModel':
        model = PlanetModel(
            name=document["name"],
            star_name=document["star_name"],
            resources=document["resources"].copy(),
            imports=document["imports"].copy(),
            exports=document["exports"].copy(),
        )
        return model

    @classmethod
    async def update(cls, planet: Planet) -> None:
        model = PlanetModel.from_logic(planet)
        if (model_db := await db.planet.find_one({"name": model.name})) is not None:
            _id = model_db["_id"]
            await db.planet.update_one({"_id": _id}, {"$set": jsonable_encoder(model)})
        else:
            await db.planet.insert_one(jsonable_encoder(model))

    @classmethod
    async def list(cls, star_name: str) -> List['PlanetModel']:
        return [PlanetModel.from_dict(doc) async for doc in db.planet.find({"star_name": star_name})]


@dataclass
class StarModel:
    name: str
    imports: List[str]
    exports: List[str]

    @classmethod
    def from_logic(cls, star: Star) -> 'StarModel':
        model = StarModel(
            name=star.name,
            imports=star.imports.copy(),
            exports=star.exports.copy(),
        )
        return model

    def to_logic(self) -> Star:
        star = Star(
            name=self.name,
            imports=self.imports.copy(),
            exports=self.exports.copy(),
        )
        return star

    @classmethod
    def from_dict(cls, document: Dict[str, Any]) -> 'StarModel':
        model = StarModel(
            name=document["name"],
            imports=document["imports"].copy(),
            exports=document["exports"].copy(),
        )
        return model

    @classmethod
    async def update(cls, star: Star) -> None:
        model = StarModel.from_logic(star)
        if (model_db := await db.star.find_one({"name": model.name})) is not None:
            _id = model_db["_id"]
            await db.star.update_one({"_id": _id}, {"$set": jsonable_encoder(model)})
        else:
            await db.star.insert_one(jsonable_encoder(model))

    @classmethod
    async def list(cls) -> List['StarModel']:
        return [StarModel.from_dict(doc) async for doc in db.star.find()]

    @classmethod
    async def find(cls, star_name) -> 'StarModel':
        doc = await db.star.find_one({"name": star_name})
        return StarModel.from_dict(doc)
