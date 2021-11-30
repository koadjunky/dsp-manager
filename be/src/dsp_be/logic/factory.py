from peewee import Model, Field, CharField, IntegerField, SqliteDatabase, DatabaseProxy

from dsp_be.logic.recipe import Recipe, recipes
from dsp_be.logic.machine import Machine, machines
from dsp_be.logic.stack import Stack


db_proxy = DatabaseProxy()


class Factory(Model):
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

    class Meta:
        database = db_proxy

if __name__ == '__main__':
    db = SqliteDatabase(':memory:')
    db_proxy.initialize(db)
    db_proxy.connect()
    db_proxy.create_tables([Factory])
    factory = Factory(machine_name='assembler1', recipe_name='circuit_board', count=6)
    factory.save()
    print(factory.production())
