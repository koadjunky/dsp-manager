from peewee import Field, CharField, IntegerField, ForeignKeyField

from dsp_be.logic import test_database, BaseModel
from dsp_be.logic.planet import Planet
from dsp_be.logic.recipe import Recipe, recipes
from dsp_be.logic.machine import Machine, machines
from dsp_be.logic.stack import Stack


class Factory(BaseModel):
    planet: Field = ForeignKeyField(Planet, backref="planets")
    recipe_name: Field = CharField()
    machine_name: Field = CharField()
    count: Field = IntegerField()

    def production(self) -> Stack:
        stack = Stack()
        for name, value in self.recipe.products.items():
            stack.add(name, value * self.count * self.machine.speed / self.recipe.time)
        for name, value in self.recipe.raws.items():
            stack.add(name, -value * self.count * self.machine.speed / self.recipe.time)
        return stack

    def get_recipe(self) -> Recipe:
        return recipes[self.recipe_name]

    def set_recipe(self, recipe: Recipe):
        self.recipe_name = recipe.name
        self.save()

    def get_machine(self) -> Machine:
        return machines[self.machine_name]

    def set_machine(self, machine: Machine):
        self.machine_name = machine.name
        self.save()

    recipe: Recipe = property(get_recipe, set_recipe)
    machine: Machine = property(get_machine, set_machine)


if __name__ == '__main__':
    test_database([Planet, Factory])
    earth = Planet.create(name='Earth')
    factory = Factory.create(planet=earth, machine_name='assembler1', recipe_name='circuit_board', count=6)
    print(factory.production())
