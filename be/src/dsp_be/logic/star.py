from dataclasses import Field

from peewee import CharField

from dsp_be.logic import DspModel
from dsp_be.logic.stack import Stack


class Star(DspModel):
    name: Field = CharField()
    imports: Field = CharField(default="")
    exports: Field = CharField(default="")

    def production(self) -> Stack:
        result = Stack()
        for planet in self.planets:
            result.combine(planet.trade())
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
