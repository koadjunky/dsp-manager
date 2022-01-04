from dataclasses import dataclass, field
from typing import Dict, List, Optional
import weakref

from dsp_be.logic.stack import Stack
from dsp_be.logic.star import Star


@dataclass
class Planet:
    name: str
    resources: Dict[str, float]
    imports: List[str]
    exports: List[str]
    star: Optional[Star]
    _star: Star = field(init=False, repr=False, default=None)
    factories: List['Factory'] = field(default_factory=list)

    def production(self) -> Stack:
        result = Stack()
        for factory in self.factories:
            result.combine(factory.production())
        return result

    def trade(self) -> Stack:
        result = Stack()
        for k, v in self.production():
            if k in self.imports and v < 0:
                result.add(k, v)
            elif k in self.exports and v > 0:
                result.add(k, v)
        return result

    @property
    def star_name(self) -> str:
        return getattr(self._star, 'name', None)

    @property
    def star(self) -> Optional[Star]:
        return self._star

    @star.setter
    def star(self, star: Optional[Star]) -> None:
        if self._star is not None:
            self._star.planets.remove(self)
        self._star = weakref.proxy(star)
        if self._star is not None:
            self._star.planets.append(self)
