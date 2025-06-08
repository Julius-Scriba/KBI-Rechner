"""Core calculation logic for the cash register."""
from typing import List, Tuple

from .models import CashRegister, Currency

# Weight of each coin in grams. Keys match the string representation of the value
WEIGHT_PER_COIN = {
    '2.00': 8.5,
    '1.00': 7.5,
    '0.50': 7.8,
    '0.20': 5.74,
    '0.10': 4.1,
    '0.05': 3.92,
    '0.02': 3.06,
    '0.01': 2.3,
}


def coin_value_from_weight(weight: float, coin_value: float, extra_weight: float = 0) -> Tuple[float, int]:
    """Return value and amount of coins based on a measured weight.

    Parameters
    ----------
    weight: float
        Measured weight in grams including possible extra weight.
    coin_value: float
        Monetary value of the analysed coin.
    extra_weight: float, optional
        Weight that should be subtracted from the measurement before
        performing the calculation.
    """
    key = f"{coin_value:.2f}"
    if key not in WEIGHT_PER_COIN:
        raise ValueError(f"Unsupported coin value: {coin_value}")

    mass = WEIGHT_PER_COIN[key]
    count = int(round((weight - extra_weight) / mass))
    total = round(count * coin_value, 2)
    return total, count


class CashCalculator:
    """Utility to accumulate values and keep track of counts."""

    def __init__(self, register: CashRegister):
        self.register = register
        self.values: List[float] = []
        self.total: float = 0.0

    def add_operand(self, amount: float, count: int, currency_value: float) -> float:
        """Add a monetary amount to the calculation and update counts."""
        self.total = round(self.total + amount, 2)
        self.values.append(self.total)

        # update available pieces
        for currency in self.register.as_list():
            if currency.value == currency_value:
                currency.count += count
                break
        return self.total
