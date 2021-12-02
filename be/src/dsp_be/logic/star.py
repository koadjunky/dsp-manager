from dataclasses import Field

from peewee import CharField

from dsp_be.logic import BaseModel
from dsp_be.logic.stack import Stack


class Star(BaseModel):
    name: Field = CharField()

    def production(self) -> Stack:
        result = Stack()
        for planet in self.planets:
            result.combine(planet.production())
        return result

