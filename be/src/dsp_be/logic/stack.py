from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class Stack:

    products: Dict[str, float] = field(default_factory=dict)

    def add(self, name: str, value: float) -> None:
        if name in self.products:
            self.products[name] += value
        else:
            self.products[name] = value

    def combine(self, stack: "Stack") -> None:
        for name, value in stack.products.items():
            self.add(name, value)

    def to_dict(self) -> Dict[str, float]:
        return self.products

    def to_list(self) -> List[Tuple[str, float]]:
        return [(k, v) for k, v in self.products.items()]

    def __iter__(self):
        for k, v in self.products.items():
            yield k, v
