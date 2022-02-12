from dataclasses import dataclass
from typing import Any, Dict, Optional

from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase

from dsp_be.logic.config import Config


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


class ConfigRepository:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.db = db

    async def create(self, config: Config) -> None:
        model = ConfigModel.from_logic(config)
        await self.db.config.insert_one(jsonable_encoder(model))

    async def update(self, config: Config) -> None:
        model = ConfigModel.from_logic(config)
        model_db = await self.db.config.find_one()
        _id = model_db["_id"]
        await self.db.config.update_one({"_id": _id}, {"$set": jsonable_encoder(model)})

    async def find(self) -> Optional["ConfigModel"]:
        doc = await self.db.config.find_one()
        if doc is None:
            return None
        return ConfigModel.from_dict(doc)
