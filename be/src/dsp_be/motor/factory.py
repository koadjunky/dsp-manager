from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from fastapi.encoders import jsonable_encoder

from dsp_be.logic.config import Config
from dsp_be.logic.factory import Factory
from dsp_be.logic.planet import Planet
from dsp_be.motor.driver import db


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
