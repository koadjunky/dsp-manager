from peewee import Field, CharField

from dsp_be.logic import test_database, BaseModel
from dsp_be.logic.stack import Stack


class Planet(BaseModel):
    name: Field = CharField()

    def production(self) -> Stack:
        result = Stack()
        for factory in self.factories:
            result.combine(factory.production())
        return result


if __name__ == '__main__':
    from dsp_be.logic.factory import Factory
    test_database([Planet, Factory])
    earth = Planet.create(name='Earth')
    factory1 = Factory.create(planet=earth, machine_name='assembler1', recipe_name='circuit_board', count=6)
    #factory2 = Factory.create(planet=earth, machine_name='arc_smelter', recipe_name='iron_ingot', count=10)
    #print(factory1.production())
    #print(earth.production())
