"""Reporting and withdrawal calculations."""
from typing import List, Tuple

from .models import CashRegister, Currency


def get_withdrawable(currency_list: List[Tuple[float, int]], change: float) -> Tuple[float, List[Tuple[float, int]], List[Tuple[float, int]]]:
    """Calculate withdrawable money and remaining change.

    Parameters
    ----------
    currency_list: list of tuples ``(value, count)`` sorted by value descending.
    change: amount of money that must remain in the register.
    """
    total = round(sum(value * count for value, count in currency_list), 2)
    withdraw_value = round(total - change, 2)

    withdraw_list: List[Tuple[float, int]] = []
    change_list: List[Tuple[float, int]] = []

    remaining = withdraw_value
    for value, count in currency_list:
        if value <= remaining:
            max_q = int(remaining // value)
            withdraw_count = min(max_q, count)
            count -= withdraw_count
        else:
            withdraw_count = 0
        remaining = round(remaining - withdraw_count * value, 2)
        withdraw_list.append((value, withdraw_count))
        change_list.append((value, count))

    return withdraw_value, withdraw_list, change_list


def calc_withdrawal(register: CashRegister, change: float) -> Tuple[float, List[Tuple[float, int]], List[Tuple[float, int]]]:
    """Wrapper around :func:`get_withdrawable` using the registers current counts."""
    currency_list = [(c.value, c.count) for c in register.as_list()]
    # sort by value descending so larger denominations are preferred
    currency_list.sort(key=lambda x: x[0], reverse=True)
    return get_withdrawable(currency_list, change)


def generate_report(register: CashRegister, change: float) -> Tuple[float, List[Tuple[float, int]], List[Tuple[float, int]]]:
    """Return a tuple with total value, withdraw list and change list."""
    total = register.total()
    withdraw_value, withdraw_list, change_list = calc_withdrawal(register, change)
    return total, withdraw_list, change_list
