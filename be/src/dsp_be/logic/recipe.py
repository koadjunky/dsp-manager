import copy
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict

from dsp_be.logic.machine import Machine
from dsp_be.logic.planet import Planet
from dsp_be.logic.stack import Stack
from dsp_be.logic.config import Config


@dataclass
class Recipe(ABC):
    name: str
    machine: str

    @abstractmethod
    def production(self, count: int, machine: Machine, planet: Planet, config: Config) -> Stack:
        pass


@dataclass
class FractinatorRecipe(Recipe):
    name: str = "fractinator"
    machine: str = "fractinator"

    def production(self, count: int, machine: Machine, planet: Planet, config: Config) -> Stack:
        stack = Stack()
        stack.add("deuterium", machine.speed * (1.0 - (0.99 ** count)))
        stack.add("hydrogen", -machine.speed * (1.0 - (0.99 ** count)))
        return stack


@dataclass
class PumpRecipe(Recipe):
    name: str
    product: str = "water"
    machine: str = "water_pump"

    def production(self, count: int, machine: Machine, planet: Planet, config: Config) -> Stack:
        stack = Stack()
        stack.add(self.product, 5.0 / 6.0 * count * (1 + 0.1 * config.veins_utilization))
        return stack


@dataclass
class OilRecipe(Recipe):
    name: str = "oil_extractor"
    product: str = "oil_extractor"
    machine: str = "oil_extractor"

    def production(self, count: int, machine: Machine, planet: Planet, config: Config) -> Stack:
        stack = Stack()
        stack.add("crude_oil", count * machine.speed * (1 + 0.1 * config.veins_utilization))
        return stack


@dataclass
class CollectorRecipe(Recipe):
    name: str = "orbital_collector"
    machine: str = "orbital_collector"

    def production(self, count: int, machine: Machine, planet: Planet, config: Config) -> Stack:
        fire_ice = 8 * count * planet.resources.get("fire_ice", 0.0) * (1 + 0.1 * config.veins_utilization)
        hydrogen = 8 * count * planet.resources.get("hydrogen", 0.0) * (1 + 0.1 * config.veins_utilization)
        deuterium = 8 * count * planet.resources.get("deuterium", 0.0) * (1 + 0.1 * config.veins_utilization)
        power = 30 * count
        fire_ice_power = 4.8 * fire_ice
        hydrogen_power = 9.0 * hydrogen
        deuterium_power = 9.0 * deuterium
        total_power = fire_ice_power + hydrogen_power + deuterium_power
        fire_ice_fraction = fire_ice_power / total_power
        hydrogen_fraction = hydrogen_power / total_power
        deuterium_fraction = deuterium_power / total_power
        stack = Stack()
        stack.add("fire_ice", (fire_ice_power - fire_ice_fraction * power) / 4.8)
        stack.add("hydrogen", (hydrogen_power - hydrogen_fraction * power) / 9.0)
        stack.add("deuterium", (deuterium_power - deuterium_fraction * power) / 9.0)
        return stack


@dataclass
class MineRecipe(Recipe):
    name: str
    product: str = "coal"
    machine: str = "mine"

    def production(self, count: int, machine: Machine, planet: Planet, config: Config) -> Stack:
        stack = Stack()
        stack.add(self.product, 0.5 * count * (1 + 0.1 * config.veins_utilization))
        return stack


mine_recipes_txt = ["coal", "copper_ore", "fire_ice", "fractal_silicon", "iron_ore", "kimberlite_ore",
                    "optical_grating_crystal", "organic_crystal", "silicon_ore", "spinform_stalagmite_crystal",
                    "stone", "titanium_ore", "unipolar_magnet"]


@dataclass
class FactoryRecipe(Recipe):
    name: str
    machine: str
    products: Dict[str, int]
    raws: Dict[str, int]
    time: float

    def production(self, count: int, machine: Machine, planet: Planet, config: Config) -> Stack:
        stack = Stack()
        for name, value in self.products.items():
            stack.add(name, value * count * machine.speed / self.time)
        for name, value in self.raws.items():
            stack.add(name, -value * count * machine.speed / self.time)
        return stack


factory_recipes_txt = [
    {
        "name": "gear",
        "machine": "assembler",
        "products": {
            "gear": 1
        },
        "raws": {
            "iron_ingot": 1
        },
        "time": 1.0
    },
    {
        "name": "magnetic_coil",
        "machine": "assembler",
        "products": {
            "magnetic_coil": 2
        },
        "raws": {
            "magnet": 2,
            "copper_ingot": 1
        },
        "time": 1.0
    },
    {
        "name": "prism",
        "machine": "assembler",
        "products": {
            "prism": 2
        },
        "raws": {
            "glass": 3
        },
        "time": 2.0
    },
    {
        "name": "plasma_exciter",
        "machine": "assembler",
        "products": {
            "plasma_exciter": 1
        },
        "raws": {
            "magnetic_coil": 4,
            "prism": 2
        },
        "time": 2.0
    },
    {
        "name": "titanium_crystal",
        "machine": "assembler",
        "products": {
            "titanium_crystal": 1
        },
        "raws": {
            "organic_crystal": 1,
            "titanium_ingot": 3
        },
        "time": 4.0
    },
    {
        "name": "casimir_crystal",
        "machine": "assembler",
        "products": {
            "casimir_crystal": 1
        },
        "raws": {
            "titanium_crystal": 1,
            "graphene": 2,
            "hydrogen": 12
        },
        "time": 4.0
    },
    {
        "name": "casimir_crystal_plus",
        "machine": "assembler",
        "products": {
            "casimir_crystal": 1
        },
        "raws": {
            "optical_grating_crystal": 4,
            "graphene": 2,
            "hydrogen": 12
        },
        "time": 4.0
    },
    {
        "name": "titanium_glass",
        "machine": "assembler",
        "products": {
            "titanium_glass": 2
        },
        "raws": {
            "glass": 2,
            "titanium_ingot": 2,
            "water": 2
        },
        "time": 5.0
    },
    {
        "name": "patricle_broadband",
        "machine": "assembler",
        "products": {
            "patricle_broadband": 1
        },
        "raws": {
            "carbon_nanotube": 2,
            "crystal_silicon": 2,
            "plastic": 1
        },
        "time": 8.0
    },
    {
        "name": "plane_filter",
        "machine": "assembler",
        "products": {
            "plane_filter": 1
        },
        "raws": {
            "casimir_crystal": 1,
            "titanium_glass": 2
        },
        "time": 12.0
    },
    {
        "name": "deuteron_fuel_rod",
        "machine": "assembler",
        "products": {
            "deuteron_fuel_rod": 2
        },
        "raws": {
            "titanium_alloy": 1,
            "deuterium": 20,
            "super_magnetic_ring": 1
        },
        "time": 12.0
    },
    {
        "name": "annihilation_constraint_sphere",
        "machine": "assembler",
        "products": {
            "annihilation_constraint_sphere": 1
        },
        "raws": {
            "patricle_container": 1,
            "processor": 1
        },
        "time": 20.0
    },
    {
        "name": "circuit_board",
        "machine": "assembler",
        "products": {
            "circuit_board": 2
        },
        "raws": {
            "iron_ingot": 2,
            "copper_ingot": 1
        },
        "time": 1.0
    },
    {
        "name": "processor",
        "machine": "assembler",
        "products": {
            "processor": 1
        },
        "raws": {
            "circuit_board": 2,
            "microcrystalline_component": 2
        },
        "time": 3.0
    },
    {
        "name": "quantum_chip",
        "machine": "assembler",
        "products": {
            "quantum_chip": 1
        },
        "raws": {
            "processor": 2,
            "plane_filter": 2
        },
        "time": 6.0
    },
    {
        "name": "microcrystalline_component",
        "machine": "assembler",
        "products": {
            "microcrystalline_component": 1
        },
        "raws": {
            "high_purity_silicon": 2,
            "copper_ingot": 1
        },
        "time": 2.0
    },
    {
        "name": "crystal_silicon_plus",
        "machine": "assembler",
        "products": {
            "crystal_silicon": 2
        },
        "raws": {
            "fractal_silicon": 1,
        },
        "time": 1.5
    },
    {
        "name": "photon_combiner",
        "machine": "assembler",
        "products": {
            "photon_combiner": 1
        },
        "raws": {
            "prism": 2,
            "circuit_board": 1
        },
        "time": 3.0
    },
    {
        "name": "photon_combiner_plus",
        "machine": "assembler",
        "products": {
            "photon_combiner": 1
        },
        "raws": {
            "optical_grating_crystal": 1,
            "circuit_board": 1
        },
        "time": 3.0
    },
    {
        "name": "solar_sail",
        "machine": "assembler",
        "products": {
            "solar_sail": 2
        },
        "raws": {
            "graphene": 1,
            "photon_combiner": 1
        },
        "time": 4.0
    },
    {
        "name": "frame_material",
        "machine": "assembler",
        "products": {
            "frame_material": 1
        },
        "raws": {
            "carbon_nanotube": 4,
            "titanium_alloy": 1,
            "high_purity_silicon": 1
        },
        "time": 6.0
    },
    {
        "name": "dyson_sphere_component",
        "machine": "assembler",
        "products": {
            "dyson_sphere_component": 1
        },
        "raws": {
            "frame_material": 3,
            "solar_sail": 3,
            "processor": 3
        },
        "time": 8.0
    },
    {
        "name": "small_carrier_rocket",
        "machine": "assembler",
        "products": {
            "small_carrier_rocket": 1
        },
        "raws": {
            "dyson_sphere_component": 2,
            "deuteron_fuel_rod": 4,
            "quantum_chip": 2
        },
        "time": 6.0
    },
    {
        "name": "electric_motor",
        "machine": "assembler",
        "products": {
            "electric_motor": 1
        },
        "raws": {
            "iron_ingot": 2,
            "gear": 1,
            "magnetic_coil": 1
        },
        "time": 2.0
    },
    {
        "name": "electromagnetic_turbine",
        "machine": "assembler",
        "products": {
            "electromagnetic_turbine": 1
        },
        "raws": {
            "electric_motor": 2,
            "magnetic_coil": 2
        },
        "time": 2.0
    },
    {
        "name": "particle_container",
        "machine": "assembler",
        "products": {
            "particle_container": 1
        },
        "raws": {
            "electromagnetic_turbine": 2,
            "copper_ingot": 2,
            "graphene": 2
        },
        "time": 4.0
    },
    {
        "name": "particle_container_plus",
        "machine": "assembler",
        "products": {
            "particle_container": 1
        },
        "raws": {
            "unipolar_magnet": 10,
            "copper_ingot": 2
        },
        "time": 4.0
    },
    {
        "name": "graviton_lens",
        "machine": "assembler",
        "products": {
            "graviton_lens": 1
        },
        "raws": {
            "diamond": 4,
            "strange_matter": 1
        },
        "time": 6.0
    },
    {
        "name": "super_magnetic_ring",
        "machine": "assembler",
        "products": {
            "super_magnetic_ring": 1
        },
        "raws": {
            "electromagnetic_turbine": 2,
            "magnet": 3,
            "energetic_graphite": 1
        },
        "time": 3.0
    },
    {
        "name": "iron_ingot",
        "machine": "smelter",
        "products": {
            "iron_ingot": 1
        },
        "raws": {
            "iron_ore": 1
        },
        "time": 1.0
    },
    {
        "name": "magnet",
        "machine": "smelter",
        "products": {
            "magnet": 1
        },
        "raws": {
            "iron_ore": 1
        },
        "time": 1.5
    },
    {
        "name": "copper_ingot",
        "machine": "smelter",
        "products": {
            "copper_ingot": 1
        },
        "raws": {
            "copper_ore": 1
        },
        "time": 1.0
    },
    {
        "name": "stone_brick",
        "machine": "smelter",
        "products": {
            "stone_brick": 1
        },
        "raws": {
            "stone": 1
        },
        "time": 1.0
    },
    {
        "name": "energetic_graphite",
        "machine": "smelter",
        "products": {
            "energetic_graphite": 1
        },
        "raws": {
            "coal": 2
        },
        "time": 2.0
    },
    {
        "name": "silicon_ore",
        "machine": "smelter",
        "products": {
            "silicon_ore": 1
        },
        "raws": {
            "stone": 10
        },
        "time": 10.0
    },
    {
        "name": "crystal_silicon",
        "machine": "smelter",
        "products": {
            "crystal_silicon": 1
        },
        "raws": {
            "high_purity_silicon": 1
        },
        "time": 2.0
    },
    {
        "name": "glass",
        "machine": "smelter",
        "products": {
            "glass": 1
        },
        "raws": {
            "stone": 2
        },
        "time": 2.0
    },
    {
        "name": "high_purity_silicon",
        "machine": "smelter",
        "products": {
            "high_purity_silicon": 1
        },
        "raws": {
            "silicon_ore": 2
        },
        "time": 2.0
    },
    {
        "name": "diamond",
        "machine": "smelter",
        "products": {
            "diamond": 1
        },
        "raws": {
            "energetic_graphite": 1
        },
        "time": 2.0
    },
    {
        "name": "diamond_plus",
        "machine": "smelter",
        "products": {
            "diamond": 2
        },
        "raws": {
            "kimberlite_ore": 1
        },
        "time": 1.5
    },
    {
        "name": "steel",
        "machine": "smelter",
        "products": {
            "steel": 1
        },
        "raws": {
            "iron_ingot": 3
        },
        "time": 3.0
    },
    {
        "name": "titanium_ingot",
        "machine": "smelter",
        "products": {
            "titanium_ingot": 1
        },
        "raws": {
            "titanium_ore": 2
        },
        "time": 1.0
    },
    {
        "name": "titanium_alloy",
        "machine": "smelter",
        "products": {
            "titanium_alloy": 4
        },
        "raws": {
            "titanium": 4,
            "steel": 4,
            "sulfric_acid": 8
        },
        "time": 12.0
    },
    {
        "name": "refining",
        "machine": "oil_refinery",
        "products": {
            "hydrogen": 1,
            "refined_oil": 2
        },
        "raws": {
            "crude_oil": 2,
        },
        "time": 4.0
    },
    {
        "name": "x_ray_cracking",
        "machine": "oil_refinery",
        "products": {
            "hydrogen": 3,
            "energetic_graphite": 2
        },
        "raws": {
            "refined_oil": 1,
            "hydrogen": 2,
        },
        "time": 4.0
    },
    {
        "name": "deuterium",
        "machine": "particle_collider",
        "products": {
            "deuterium": 5,
        },
        "raws": {
            "hydrogen": 10,
        },
        "time": 2.0
    },
    {
        "name": "antimatter",
        "machine": "particle_collider",
        "products": {
            "antimatter": 2,
            "hydrogen": 2,
        },
        "raws": {
            "critical_photon": 2,
        },
        "time": 2.0
    },
    {
        "name": "strange_matter",
        "machine": "particle_collider",
        "products": {
            "strange_matter": 1,
        },
        "raws": {
            "patricle_container": 2,
            "iron_ingot": 2,
            "deuterium": 10
        },
        "time": 8.0
    },
    {
        "name": "plastic",
        "machine": "chemical_plant",
        "products": {
            "plastic": 1,
        },
        "raws": {
            "refined_oil": 2,
            "energetic_graphite": 1,
        },
        "time": 3.0
    },
    {
        "name": "sulfuric_acid",
        "machine": "chemical_plant",
        "products": {
            "sulfuric_acid": 4,
        },
        "raws": {
            "refined_oil": 6,
            "stone": 8,
            "water": 4,
        },
        "time": 6.0
    },
    {
        "name": "organic_crystal",
        "machine": "chemical_plant",
        "products": {
            "organic_crystal": 1,
        },
        "raws": {
            "plastic": 2,
            "refined_oil": 1,
            "water": 1,
        },
        "time": 6.0
    },
    {
        "name": "graphene",
        "machine": "chemical_plant",
        "products": {
            "graphene": 2,
        },
        "raws": {
            "energetic_graphite": 3,
            "sulfric_acid": 1,
        },
        "time": 3.0
    },
    {
        "name": "graphene_plus",
        "machine": "chemical_plant",
        "products": {
            "graphene": 2,
            "hydrogen": 1,
        },
        "raws": {
            "fire_ice": 2,
        },
        "time": 2.0
    },
    {
        "name": "carbon_nanotube",
        "machine": "chemical_plant",
        "products": {
            "carbon_nanotube": 2,
        },
        "raws": {
            "graphene": 3,
            "titanium_ingot": 1,
        },
        "time": 4.0
    },
    {
        "name": "carbon_nanotube_plus",
        "machine": "chemical_plant",
        "products": {
            "carbon_nanotube": 2,
        },
        "raws": {
            "spiniform_stalagmite_crystal": 2,
        },
        "time": 4.0
    },
    {
        "name": "blue_science",
        "machine": "matrix_lab",
        "products": {
            "blue_science": 1,
        },
        "raws": {
            "magnetic_coil": 1,
            "circuit_board": 1,
        },
        "time": 3.0
    },
    {
        "name": "red_science",
        "machine": "matrix_lab",
        "products": {
            "red_science": 1,
        },
        "raws": {
            "energetic_graphite": 2,
            "hydrogen": 2,
        },
        "time": 6.0
    },
    {
        "name": "yellow_science",
        "machine": "matrix_lab",
        "products": {
            "yellow_science": 1,
        },
        "raws": {
            "diamond": 1,
            "organic_crystal": 1,
        },
        "time": 8.0
    },
    {
        "name": "purple_science",
        "machine": "matrix_lab",
        "products": {
            "purple_science": 1,
        },
        "raws": {
            "processor": 2,
            "particle_broadband": 1,
        },
        "time": 10.0
    },
    {
        "name": "green_science",
        "machine": "matrix_lab",
        "products": {
            "green_science": 2,
        },
        "raws": {
            "graviton_lens": 1,
            "quantum_chip": 1,
        },
        "time": 24.0
    },
    {
        "name": "white_science",
        "machine": "matrix_lab",
        "products": {
            "white_science": 1,
        },
        "raws": {
            "blue_science": 1,
            "red_science": 1,
            "yellow_science": 1,
            "purple_science": 1,
            "green_science": 1,
            "antimatter": 1,
        },
        "time": 15.0
    },
]


class RecipeBook:

    def __init__(self):
        self.recipes: Dict[str, Recipe] = {}

    def add(self, recipe: Recipe) -> None:
        if recipe.name in self.recipes:
            raise Exception(f"Duplicate recipe name {recipe.name}")
        self.recipes[recipe.name] = recipe

    def get(self, name):
        return self.recipes[name]


def load_recipes() -> RecipeBook:
    rb = RecipeBook()
    for product in mine_recipes_txt:
        rb.add(MineRecipe(name=product + "_vein", product=product))
    for recipe_txt in factory_recipes_txt:
        recipe = FactoryRecipe(name=recipe_txt["name"], machine=recipe_txt["machine"], products=copy.deepcopy(recipe_txt["products"]),
                               raws=copy.deepcopy(recipe_txt["raws"]), time=recipe_txt["time"])
        rb.add(recipe)
    rb.add(FractinatorRecipe())
    rb.add(PumpRecipe(name="water_pump", product="water"))
    rb.add(PumpRecipe(name="sulfric_acid_pump", product="sulfric_acid"))
    rb.add(CollectorRecipe())
    return rb


recipes = load_recipes()


if __name__ == '__main__':
    from dsp_be.logic.factory import Factory
    config = Config(veins_utilization=2)
    planet = Planet(name="Jupiter", resources={"fire_ice": 0.04, "hydrogen": 0.85, "deuterium": 0.0}, exports=[], imports=[], star=None)
    factory = Factory(name="Collector #1", machine_name="orbital_collector", recipe_name="orbital_collector", count=40, planet=planet, config=config)
    print("Fire ice:9.24, Hydrogen:196.4", factory.production())
