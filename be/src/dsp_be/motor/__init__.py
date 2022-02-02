from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import motor.motor_asyncio
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

from dsp_be.logic.config import Config
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
    id: str
    name: str
    planet_name: str
    recipe_name: str
    machine_name: str
    count: int

    @classmethod
    def from_logic(cls, factory: Factory) -> "FactoryModel":
        model = FactoryModel(
            id=factory.id,
            planet_name=factory.planet_name,
            name=factory.name,
            recipe_name=factory.recipe_name,
            machine_name=factory.machine_name,
            count=factory.count,
        )
        return model

    def to_logic(self, planet: Planet, config: Config):
        factory = Factory(
            id=self.id,
            name=self.name,
            recipe_name=self.recipe_name,
            machine_name=self.machine_name,
            count=self.count,
            planet=planet,
            config=config,
        )
        return factory

    @classmethod
    def from_dict(cls, document: Dict[str, Any]) -> "FactoryModel":
        model = FactoryModel(
            id=document["id"],
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
        if (model_db := await db.factory.find_one({"id": model.id})) is not None:
            _id = model_db["_id"]
            await db.factory.update_one({"_id": _id}, {"$set": jsonable_encoder(model)})
        else:
            await db.factory.insert_one(jsonable_encoder(model))

    @classmethod
    async def list(cls, planet_name: str) -> List["FactoryModel"]:
        return [
            FactoryModel.from_dict(doc)
            async for doc in db.factory.find({"planet_name": planet_name})
        ]

    @classmethod
    async def find_name(
        cls, planet_name: str, factory_name: str
    ) -> Optional["FactoryModel"]:
        doc = await db.factory.find_one(
            {"planet_name": planet_name, "name": factory_name}
        )
        if doc is None:
            return None
        return FactoryModel.from_dict(doc)

    @classmethod
    async def find_id(
        cls, planet_name: str, factory_id: str
    ) -> Optional["FactoryModel"]:
        doc = await db.factory.find_one({"planet_name": planet_name, "id": factory_id})
        if doc is None:
            return None
        return FactoryModel.from_dict(doc)

    @classmethod
    async def delete_id(cls, factory_id: str) -> None:
        await db.factory.delete_many({"id": factory_id})


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
    async def update(cls, planet: Planet) -> None:
        model = PlanetModel.from_logic(planet)
        if (model_db := await db.planet.find_one({"name": model.name})) is not None:
            _id = model_db["_id"]
            await db.planet.update_one({"_id": _id}, {"$set": jsonable_encoder(model)})
        else:
            await db.planet.insert_one(jsonable_encoder(model))

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
    async def update(cls, star: Star) -> None:
        model = StarModel.from_logic(star)
        if (model_db := await db.star.find_one({"name": model.name})) is not None:
            _id = model_db["_id"]
            await db.star.update_one({"_id": _id}, {"$set": jsonable_encoder(model)})
        else:
            await db.star.insert_one(jsonable_encoder(model))

    @classmethod
    async def list(cls) -> List["StarModel"]:
        return [StarModel.from_dict(doc) async for doc in db.star.find()]

    @classmethod
    async def find(cls, star_name: str) -> Optional["StarModel"]:
        doc = await db.star.find_one({"name": star_name})
        if doc is None:
            return None
        return StarModel.from_dict(doc)


@dataclass
class ConfigModel:
    veins_utilization: int

    @classmethod
    def from_logic(cls, config: Config) -> "ConfigModel":
        model = ConfigModel(veins_utilization=config.veins_utilization)
        return model

    def to_logic(self) -> Config:
        config = Config(veins_utilization=self.veins_utilization)
        return config

    @classmethod
    def from_dict(cls, document: Dict[str, Any]) -> "ConfigModel":
        model = ConfigModel(veins_utilization=document["veins_utilization"])
        return model

    @classmethod
    async def update(cls, config: Config) -> None:
        model = ConfigModel.from_logic(config)
        if (model_db := await db.config.find_one()) is not None:
            _id = model_db["_id"]
            await db.config.update_one({"_id": _id}, {"$set": jsonable_encoder(model)})
        else:
            await db.config.insert_one(jsonable_encoder(model))

    @classmethod
    async def find(cls) -> Optional["ConfigModel"]:
        doc = await db.config.find_one()
        if doc is None:
            return None
        return ConfigModel.from_dict(doc)
