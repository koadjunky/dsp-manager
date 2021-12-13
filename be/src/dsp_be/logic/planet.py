from peewee import Field, CharField, ForeignKeyField, FloatField

from dsp_be.logic import DspModel
from dsp_be.logic.stack import Stack
from dsp_be.logic.star import Star


class Planet(DspModel):
    name: Field = CharField()
    hydrogen: Field = FloatField(default=0.0)
    deuterium: Field = FloatField(default=0.0)
    fire_ice: Field = FloatField(default=0.0)
    star: Field = ForeignKeyField(Star, backref="planets")
    imports: Field = CharField(default="")
    exports: Field = CharField(default="")

    def production(self) -> Stack:
        result = Stack()
        for factory in self.factories:
            result.combine(factory.production())
        return result

    def trade(self) -> Stack:
        result = Stack()
        imports_list = self.get_imports()
        exports_list = self.get_exports()
        for k, v in self.production():
            if k in imports_list and v < 0:
                result.add(k, v)
            elif k in exports_list and v > 0:
                result.add(k, v)
        return result

    def get_imports(self):
        return [x for x in self.imports.split(",") if x]

    def get_exports(self):
        return [x for x in self.exports.split(",") if x]
