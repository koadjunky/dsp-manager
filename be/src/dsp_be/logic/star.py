import uuid
from dataclasses import dataclass, field
from typing import List

from dsp_be.logic.stack import Stack


@dataclass
class Star:
    name: str
    imports: List[str]
    exports: List[str]
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    planets: List['Planet'] = field(default_factory=list)

    def production(self) -> Stack:
        result = Stack()
        for planet in self.planets:
            result.combine(planet.trade())
        return result

    def trade(self) -> Stack:
        result = Stack()
        for k, v in self.production():
            if k in self.imports and v < 0:
                result.add(k, v)
            elif k in self.exports and v > 0:
                result.add(k, v)
        return result
