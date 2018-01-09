from typing import Tuple, Callable, Any

from main import Card
from monads.Maybe_monad import Just, Error, Maybe_monad


def validate_charge(card: Card, amount: int, *args) -> bool:
    return card.balance + amount <= card.limit


def validate_number(card: Card, *args) -> bool:
    even_indexed_numbers: Tuple[int] = tuple(i for idx, i in enumerate(reversed(card.number)) if idx % 2 == 0)
    odd_indexed_numbers: Tuple[int] = tuple(i for idx, i in enumerate(reversed(card.number)) if idx % 2 != 0)
    doubled_odd_indexed_numbers: Tuple[int] = tuple(i * 2 for i in odd_indexed_numbers)
    summed_digits_doubled_odd_indexed_numbers: Tuple[int] = tuple(sum_digits(i) for i in doubled_odd_indexed_numbers)
    sum_of_even_indexed_numbers: int = sum(even_indexed_numbers)
    sum_of_summed_digits_doubled_odd_indexed_numbers: int = sum(summed_digits_doubled_odd_indexed_numbers)
    return (sum_of_summed_digits_doubled_odd_indexed_numbers + sum_of_even_indexed_numbers) % 10 == 0


def validate_decorator(validator_func: Callable[..., bool], success_handler: Callable[..., Any], failure_handler: Callable[..., Any]) -> Callable[..., Any]:
    def inner(func: Callable[..., Any]) -> Callable[..., Any]:
        def inner_inner(*args, **kwargs) -> Any:
            return success_handler(func(*args, **kwargs)) if validator_func(*args, **kwargs) else failure_handler(*args,
                                                                                                                  **kwargs)

        return inner_inner

    return inner


def card_pass_decorator(validator_func: Callable[..., bool]) -> Callable[..., Maybe_monad]:
    return validate_decorator(validator_func, lambda *args, **kwargs: Just(args[0]),
                              lambda *args, **kwargs: Just(args[0]))


def card_stop_decorator(validator_func: Callable[..., bool]) -> Callable[..., Maybe_monad]:
    return validate_decorator(validator_func, lambda *args, **kwargs: Just(args[0]),
                              lambda *args, **kwargs: Error(args[0]))


def sum_digits(number: int) -> int:
    return number % 10 + sum_digits(number // 10) if number != 0 else 0