from dataclasses import dataclass, field
from typing import Optional

from dsp_be.logic.planet import Planet
from dsp_be.logic.recipe import Recipe, recipes
from dsp_be.logic.machine import Machine, machines
from dsp_be.logic.stack import Stack


@dataclass
class Factory:
    name: str
    recipe_name: str
    machine_name: str
    count: int
    planet: Optional[Planet]
    _planet: Planet = field(init=False, repr=False, default=None)

    def production(self) -> Stack:
        return self.recipe.production(self.count, self.machine, self.planet)

    @property
    def planet_name(self) -> str:
        return getattr(self._planet, 'name', None)

    @property
    def planet(self) -> Optional[Planet]:
        return self._planet

    @planet.setter
    def planet(self, planet: Optional[Planet]) -> None:
        if self._planet is not None:
            self._planet.factories.remove(self)
        self._planet = planet
        if self._planet is not None:
            self._planet.factories.append(self)

    @property
    def recipe(self) -> Recipe:
        return recipes.get(self.recipe_name)

    @recipe.setter
    def recipe(self, recipe: Recipe) -> None:
        self.recipe_name = recipe.name

    @property
    def machine(self) -> Machine:
        return machines[self.machine_name]

    @machine.setter
    def machine(self, machine: Machine) -> None:
        self.machine_name = machine.name


if __name__ == '__main__':
    from dsp_be.logic.star import Star
    sun = Star(name='Sun', exports=["circuit_board", "copper_ingot"], imports=["iron_ore"])
    earth = Planet(name='Sun 3', resources={}, exports=["circuit_board", "copper_ingot"], imports=["iron_ore"], star=sun)
    factory1 = Factory(name="Circuit Board #1", machine_name='assembler1', recipe_name='circuit_board', count=6, planet=earth)
    factory2 = Factory(name="Iron Ingot #1", machine_name='arc_smelter', recipe_name='iron_ingot', count=9, planet=earth)
    print("Sun production: ", sun.production())
    print("Earth production: ", earth.production())
    print("Sun trade: ", sun.trade())
    print("Earth trade: ", earth.trade())
