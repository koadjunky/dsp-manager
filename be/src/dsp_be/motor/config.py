from dataclasses import dataclass
from typing import Any, Dict, Optional

from fastapi.encoders import jsonable_encoder

from dsp_be.logic.config import Config
from dsp_be.motor.driver import db


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
