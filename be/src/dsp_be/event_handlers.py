from typing import Callable

from fastapi import FastAPI
from loguru import logger

from dsp_be.logic.star import Star
from dsp_be.logic.planet import Planet
from dsp_be.logic.factory import Factory
from dsp_be.logic.config import Config
from dsp_be.motor import FactoryModel, PlanetModel, StarModel, ConfigModel


def start_app_handler(app: FastAPI) -> Callable:
    async def startup() -> None:
        logger.info("Running app start handler.")
        config = Config()
        await ConfigModel.update(config)
        sun = Star(name='Sun', exports=["circuit_board", "copper_ingot"], imports=["iron_ore"])
        await StarModel.update(sun)
        earth = Planet(name='Sun 3', resources={}, exports=["processor"], imports=[], star=sun)
        await PlanetModel.update(earth)
        await FactoryModel.update(Factory(name="Processor #1", machine_name="assembler2", recipe_name="processor", count=3, planet=earth, config=config))
        await FactoryModel.update(Factory(name="Circuit Board #1", machine_name="assembler2", recipe_name="circuit_board", count=1, planet=earth, config=config))
        await FactoryModel.update(Factory(name="Iron Ingot #1", machine_name="arc_smelter", recipe_name="iron_ingot", count=2, planet=earth, config=config))
        await FactoryModel.update(Factory(name="Iron Mine #1", machine_name="mine", recipe_name="iron_ore_vein", count=4, planet=earth, config=config))
        await FactoryModel.update(Factory(name="Microcrystalline #1", machine_name="assembler2", recipe_name="microcrystalline_component", count=4, planet=earth, config=config))
        await FactoryModel.update(Factory(name="Silicon #1", machine_name="arc_smelter", recipe_name="high_purity_silicon", count=8, planet=earth, config=config))
        await FactoryModel.update(Factory(name="Silicon Mine #1", machine_name="mine", recipe_name="silicon_ore_vein", count=16, planet=earth, config=config))
        await FactoryModel.update(Factory(name="Copper Ingot #1", machine_name="arc_smelter", recipe_name="copper_ingot", count=3, planet=earth, config=config))
        await FactoryModel.update(Factory(name="Copper Mine #1", machine_name="mine", recipe_name="copper_ore_vein", count=6, planet=earth, config=config))
        print(earth.trade())
    return startup


def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        logger.info("Running app shutdown handler.")

    return shutdown
