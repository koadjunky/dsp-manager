from typing import Callable

from fastapi import FastAPI
from loguru import logger

from dsp_be.logic.config import Config
from dsp_be.logic.factory import Factory
from dsp_be.logic.planet import Planet
from dsp_be.logic.star import Star
from dsp_be.motor.config import ConfigModel
from dsp_be.motor.factory import FactoryModel
from dsp_be.motor.planet import PlanetModel
from dsp_be.motor.star import StarModel


def start_app_handler(app: FastAPI) -> Callable:
    async def update_or_create_factory(factory: Factory):
        factory_db = await FactoryModel.find_name(factory.planet_name, factory.name)
        if factory_db is not None:
            factory.id = factory_db.id
            await FactoryModel.update(factory)
        else:
            await FactoryModel.create(factory)

    async def update_or_create_planet(planet: Planet):
        planet_db = await PlanetModel.find(planet.name)
        if planet_db is not None:
            planet.id = planet_db.id
            await PlanetModel.update(planet)
        else:
            await PlanetModel.create(planet)

    async def update_or_create_star(star: Star):
        star_db = await StarModel.find(star.name)
        if star_db is not None:
            star.id = star_db.id
            await StarModel.update(star)
        else:
            await StarModel.create(star)

    async def startup() -> None:
        logger.info("Running app start handler.")
        config = Config()
        await ConfigModel.update(config)
        sun = Star(
            name="Sun", exports=["circuit_board", "copper_ingot"], imports=["iron_ore"]
        )
        await update_or_create_star(sun)
        earth = Planet(
            name="Sun 3", resources={}, exports=["processor"], imports=[], star=sun
        )
        await update_or_create_planet(earth)
        await update_or_create_factory(
            Factory(
                name="Processor #1",
                machine_name="assembler2",
                recipe_name="processor",
                count=3,
                planet=earth,
                config=config,
            )
        )
        await update_or_create_factory(
            Factory(
                name="Circuit Board #1",
                machine_name="assembler2",
                recipe_name="circuit_board",
                count=1,
                planet=earth,
                config=config,
            )
        )
        await update_or_create_factory(
            Factory(
                name="Iron Ingot #1",
                machine_name="arc_smelter",
                recipe_name="iron_ingot",
                count=2,
                planet=earth,
                config=config,
            )
        )
        await update_or_create_factory(
            Factory(
                name="Iron Mine #1",
                machine_name="mine",
                recipe_name="iron_ore_vein",
                count=4,
                planet=earth,
                config=config,
            )
        )
        await update_or_create_factory(
            Factory(
                name="Microcrystalline #1",
                machine_name="assembler2",
                recipe_name="microcrystalline_component",
                count=4,
                planet=earth,
                config=config,
            )
        )
        await update_or_create_factory(
            Factory(
                name="Silicon #1",
                machine_name="arc_smelter",
                recipe_name="high_purity_silicon",
                count=8,
                planet=earth,
                config=config,
            )
        )
        await update_or_create_factory(
            Factory(
                name="Silicon Mine #1",
                machine_name="mine",
                recipe_name="silicon_ore_vein",
                count=16,
                planet=earth,
                config=config,
            )
        )
        await update_or_create_factory(
            Factory(
                name="Copper Ingot #1",
                machine_name="arc_smelter",
                recipe_name="copper_ingot",
                count=3,
                planet=earth,
                config=config,
            )
        )
        await update_or_create_factory(
            Factory(
                name="Copper Mine #1",
                machine_name="mine",
                recipe_name="copper_ore_vein",
                count=6,
                planet=earth,
                config=config,
            )
        )
        print(earth.trade())

    return startup


def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        logger.info("Running app shutdown handler.")

    return shutdown
