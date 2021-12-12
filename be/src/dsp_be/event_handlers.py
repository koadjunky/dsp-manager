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
        sun, _ = Star.get_or_create(name='Sun')
        earth, _ = Planet.get_or_create(name='Earth', star=sun)
        Factory.get_or_create(name="Processor #1", planet=earth, machine_name="assembler2", recipe_name="processor", count=3)
        Factory.get_or_create(name="Circuit Board #1", planet=earth, machine_name="assembler2", recipe_name="circuit_board", count=1)
        Factory.get_or_create(name="Iron Ingot #1", planet=earth, machine_name="arc_smelter", recipe_name="iron_ingot", count=2)
        Factory.get_or_create(name="Iron Mine #1", planet=earth, machine_name="mine", recipe_name="iron_ore_vein", count=4)
        Factory.get_or_create(name="Microcrystalline #1", planet=earth, machine_name="assembler2", recipe_name="microcrystalline_component", count=4)
        Factory.get_or_create(name="Silicon #1", planet=earth, machine_name="arc_smelter", recipe_name="high_purity_silicon", count=8)
        Factory.get_or_create(name="Silicon Mine #1", planet=earth, machine_name="mine", recipe_name="silicon_ore_vein", count=16)
        Factory.get_or_create(name="Copper Ingot #1", planet=earth, machine_name="arc_smelter", recipe_name="copper_ingot", count=3)
        Factory.get_or_create(name="Copper Mine #1", planet=earth, machine_name="mine", recipe_name="copper_ore_vein", count=6)
        print(sun.production())
        close_database()
    return startup


def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        logger.info("Running app shutdown handler.")

    return shutdown
