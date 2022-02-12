from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase

from dsp_be.logic.config import Config
from dsp_be.logic.factory import Factory
from dsp_be.logic.planet import Planet


@dataclass
class FactoryModel:
    id: str
    name: str
    planet_name: str  # TODO: Should link by planet_id
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


class FactoryRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def create(self, factory: Factory) -> None:
        model = FactoryModel.from_logic(factory)
        await self.db.factory.insert_one(jsonable_encoder(model))

    async def update(self, factory: Factory) -> None:
        model = FactoryModel.from_logic(factory)
        model_db = await self.db.factory.find_one({"id": model.id})
        _id = model_db["_id"]
        await self.db.factory.update_one(
            {"_id": _id}, {"$set": jsonable_encoder(model)}
        )

    async def list(self, planet_name: str) -> List["FactoryModel"]:
        return [
            FactoryModel.from_dict(doc)
            async for doc in self.db.factory.find({"planet_name": planet_name})
        ]

    async def find_name(
        self, planet_name: str, factory_name: str
    ) -> Optional["FactoryModel"]:
        doc = await self.db.factory.find_one(
            {"planet_name": planet_name, "name": factory_name}
        )
        if doc is None:
            return None
        return FactoryModel.from_dict(doc)

    async def find(self, factory_id: str) -> Optional["FactoryModel"]:
        doc = await self.db.factory.find_one({"id": factory_id})
        if doc is None:
            return None
        return FactoryModel.from_dict(doc)

    async def delete(self, factory_id: str) -> None:
        await self.db.factory.delete_many({"id": factory_id})
