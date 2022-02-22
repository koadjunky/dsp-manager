import uuid
import weakref
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from dsp_be.logic.stack import Stack
from dsp_be.logic.star import Star

if False:
    from dsp_be.logic.factory import Factory  # To make mypy happy


@dataclass
class Planet:
    name: str
    resources: Dict[str, float]
    imports: List[str]
    exports: List[str]
    star: Optional[Star]
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    _star: Star = field(init=False, repr=False, default=None)
    factories: List["Factory"] = field(default_factory=list)

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
    def star_id(self) -> str:
        return getattr(self._star, "id", None)

    @property
    def star_name(self) -> str:
        return getattr(self._star, "name", None)

    @property  # type: ignore[no-redef]
    def star(self) -> Optional[Star]:
        return self._star

    @star.setter
    def star(self, star: Optional[Star]) -> None:
        if self._star is not None:
            self._star.planets.remove(self)
        self._star = weakref.proxy(star) if star else None
        if self._star is not None:
            self._star.planets.append(self)
