from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Stack:

    products: Dict[str, float] = field(default_factory=dict)

    def add(self, name: str, value: float) -> None:
        if name in self.products:
            self.products[name] += value
        else:
            self.products[name] = value

    def combine(self, stack: 'Stack') -> None:
        for name, value in stack.products.items():
            self.add(name, value)
