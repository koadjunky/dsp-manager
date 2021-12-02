from peewee import Field, CharField, ForeignKeyField

from dsp_be.logic import test_database, BaseModel
from dsp_be.logic.stack import Stack
from dsp_be.logic.star import Star


class Planet(BaseModel):
    name: Field = CharField()
    star: Field = ForeignKeyField(Star, backref="planets")

    def production(self) -> Stack:
        result = Stack()
        for factory in self.factories:
            result.combine(factory.production())
        return result

