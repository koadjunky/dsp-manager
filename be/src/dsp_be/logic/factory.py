from peewee import Field, CharField, IntegerField, ForeignKeyField

from dsp_be.logic import test_database, BaseModel
from dsp_be.logic.planet import Planet
from dsp_be.logic.recipe import Recipe, recipes
from dsp_be.logic.machine import Machine, machines
from dsp_be.logic.stack import Stack


class Factory(BaseModel):
    planet: Field = ForeignKeyField(Planet, backref="factories")
    recipe_name: Field = CharField()
    machine_name: Field = CharField()
    count: Field = IntegerField()

    def production(self) -> Stack:
        return self.recipe.production(self.count, self.machine, self.planet)

    def get_recipe(self) -> Recipe:
        return recipes.get(self.recipe_name)

    def set_recipe(self, recipe: Recipe) -> None:
        self.recipe_name = recipe.name
        self.save()

    def get_machine(self) -> Machine:
        return machines[self.machine_name]

    def set_machine(self, machine: Machine) -> None:
        self.machine_name = machine.name
        self.save()

    recipe: Recipe = property(get_recipe, set_recipe)
    machine: Machine = property(get_machine, set_machine)


if __name__ == '__main__':
    from dsp_be.logic.star import Star
    test_database([Star, Planet, Factory])
    sun = Star.create(name='Sun')
    earth = Planet.create(name='Earth', star=sun)
    factory1 = Factory.create(planet=earth, machine_name='assembler1', recipe_name='circuit_board', count=6)
    factory2 = Factory.create(planet=earth, machine_name='arc_smelter', recipe_name='iron_ingot', count=9)
    print(sun.production())
