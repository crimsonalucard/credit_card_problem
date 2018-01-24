from typing import Tuple, Callable, Any, List

from custrom_types import Card


def validate_charge(card: Card, amount: int, *args) -> bool:
    return card.limit >= (card.balance + amount)


def validate_card(card: Card, *args) -> bool:
    return validate_number(card.number)

def validate_number(numbers: List[int]) -> bool:
    even_indexed_numbers: Tuple[int, ...] = tuple(i for idx, i in enumerate(reversed(numbers)) if idx % 2 == 0)
    odd_indexed_numbers: Tuple[int, ...] = tuple(i for idx, i in enumerate(reversed(numbers)) if idx % 2 != 0)
    doubled_odd_indexed_numbers: Tuple[int, ...] = tuple(i * 2 for i in odd_indexed_numbers)
    summed_digits_doubled_odd_indexed_numbers: Tuple[int, ...] = tuple(
        sum_digits(i) for i in doubled_odd_indexed_numbers)
    sum_of_even_indexed_numbers: int = sum(even_indexed_numbers)
    sum_of_summed_digits_doubled_odd_indexed_numbers: int = sum(summed_digits_doubled_odd_indexed_numbers)
    return (sum_of_summed_digits_doubled_odd_indexed_numbers + sum_of_even_indexed_numbers) % 10 == 0



def validate_decorator(validator_func: Callable[..., bool], success_handler: Callable[..., Any],
                       failure_handler: Callable[..., Any]) -> Callable[..., Any]:
    def inner(func: Callable[..., Any]) -> Callable[..., Any]:
        def inner_inner(*args, **kwargs) -> Any:
            if validator_func(*args, **kwargs):
                return success_handler(*(func(*args, **kwargs), *args[1:]), **kwargs)
            else:
                return failure_handler(*args, **kwargs)

        return inner_inner

    return inner


# validates functions that have a card as a first parameter and returns a card
def card_pass_decorator(validator_func: Callable[..., bool]) -> Callable[..., Any]:
    def success(*args: Any) -> Card:
        return args[0]

    def fail(*args: Any) -> Card:
        return args[0]

    return validate_decorator(validator_func, success, fail)


def sum_digits(number: int) -> int:
    return number % 10 + sum_digits(number // 10) if number != 0 else 0
