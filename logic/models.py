from dataclasses import dataclass, field
from typing import List

@dataclass
class Currency:
    """Represents a single currency denomination (coin or bill)."""
    value: float
    count: int = 0

    def total(self) -> float:
        """Return the total monetary value of this currency."""
        return round(self.value * self.count, 2)

@dataclass
class CashRegister:
    """Container for all available coins and bills."""
    coins: List[Currency] = field(default_factory=list)
    bills: List[Currency] = field(default_factory=list)

    def total(self) -> float:
        """Calculate the overall monetary value of all currencies."""
        return round(sum(c.total() for c in self.coins + self.bills), 2)

    def as_list(self) -> List[Currency]:
        """Return all currencies as a single list ordered bills then coins."""
        return self.bills + self.coins
