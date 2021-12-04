from peewee import Field, CharField, ForeignKeyField, FloatField

from dsp_be.logic import BaseModel
from dsp_be.logic.stack import Stack
from dsp_be.logic.star import Star


class Planet(BaseModel):
    name: Field = CharField()
    hydrogen: Field = FloatField(default=0.0)
    deuterium: Field = FloatField(default=0.0)
    fire_ice: Field = FloatField(default=0.0)
    star: Field = ForeignKeyField(Star, backref="planets")

    def production(self) -> Stack:
        result = Stack()
        for factory in self.factories:
            result.combine(factory.production())
        return result

