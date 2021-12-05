from typing import Callable

from fastapi import FastAPI
from loguru import logger


def start_app_handler(app: FastAPI) -> Callable:
    def startup() -> None:
        logger.info("Running app start handler.")
        from dsp_be.logic.star import Star
        from dsp_be.logic.planet import Planet
        from dsp_be.logic.factory import Factory
        from dsp_be.logic import test_database, close_database
        test_database([Star, Planet, Factory])
        sun = Star.create(name='Sun')
        earth = Planet.create(name='Earth', star=sun)
        Factory.create(planet=earth, machine_name="assembler2", recipe_name="processor", count=3)
        Factory.create(planet=earth, machine_name="assembler2", recipe_name="circuit_board", count=1)
        Factory.create(planet=earth, machine_name="arc_smelter", recipe_name="iron_ingot", count=2)
        Factory.create(planet=earth, machine_name="mine", recipe_name="iron_ore_vein", count=4)
        Factory.create(planet=earth, machine_name="assembler2", recipe_name="microcrystalline_component", count=4)
        Factory.create(planet=earth, machine_name="arc_smelter", recipe_name="high_purity_silicon", count=8)
        Factory.create(planet=earth, machine_name="mine", recipe_name="silicon_ore_vein", count=16)
        Factory.create(planet=earth, machine_name="arc_smelter", recipe_name="copper_ingot", count=3)
        Factory.create(planet=earth, machine_name="mine", recipe_name="copper_ore_vein", count=6)
        print(sun.production())
        close_database()
    return startup


def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        logger.info("Running app shutdown handler.")

    return shutdown
