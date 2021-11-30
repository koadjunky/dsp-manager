from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Stack:

    products: Dict[str, float] = field(default_factory=dict)

    def add(self, name, value):
        if name in self.products:
            self.products[name] += value
        else:
            self.products[name] = value
