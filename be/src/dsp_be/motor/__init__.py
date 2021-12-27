from dataclasses import dataclass, field
from typing import Dict, List

import motor.motor_asyncio
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

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
    def from_logic(cls, factory: Factory):
        model = FactoryModel(
            planet_name=factory.planet_name,
            name=factory.name,
            recipe_name=factory.recipe_name,
            machine_name=factory.machine_name,
            count=factory.count,
        )
        return model

    @classmethod
    async def update(cls, factory: Factory):
        model = FactoryModel.from_logic(factory)
        if (model_db := await db["factory"].find_one({"name": model.name})) is not None:
            _id = model_db._id
            await db["factory"].update_one({"_id": _id}, {"$set": jsonable_encoder(model)})
        else:
            await db["factory"].insert_one(jsonable_encoder(model))


@dataclass
class PlanetModel:
    name: str
    star_name: str
    resources: Dict[str, float]
    imports: List[str]
    exports: List[str]

    @classmethod
    def from_logic(cls, planet: Planet):
        model = PlanetModel(
            name=planet.name,
            star_name=planet.star_name,
            resources=planet.resources.copy(),
            imports=planet.imports.copy(),
            exports=planet.exports.copy(),
        )
        return model

    @classmethod
    async def update(cls, planet: Planet):
        model = PlanetModel.from_logic(planet)
        if (model_db := await db["planet"].find_one({"name": model.name})) is not None:
            _id = model_db._id
            await db["planet"].update_one({"_id": _id}, {"$set": jsonable_encoder(model)})
        else:
            await db["planet"].insert_one(jsonable_encoder(model))


@dataclass
class StarModel:
    name: str
    imports: List[str]
    exports: List[str]

    @classmethod
    def from_logic(cls, star: Star):
        model = StarModel(
            name=star.name,
            imports=star.imports.copy(),
            exports=star.exports.copy(),
        )
        return model

    @classmethod
    async def update(cls, star: Star):
        model = StarModel.from_logic(star)
        if (model_db := await db["planet"].find_one({"name": model.name})) is not None:
            _id = model_db._id
            await db["star"].update_one({"_id": _id}, {"$set": jsonable_encoder(model)})
        else:
            await db["star"].insert_one(jsonable_encoder(model))
