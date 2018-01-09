from typing import NamedTuple, Callable, Any, List

from monads.IO_monad import IO_monad, pass_io
from validators import card_pass_decorator, validate_number, validate_charge
from functools import reduce

COMMANDS = {
    "Add": lambda *args, **kwargs: add(*args, **kwargs),
    "Charge": lambda *args, **kwargs: charge(*args, **kwargs),
    "Credit": lambda *args, **kwargs: credit(*args, **kwargs)
}


class Card(NamedTuple):
    name: str
    balance: int
    limit: int
    number: List[int]


def parse_string_to_command(line: str) -> Callable[[], IO_monad]:
    tokens = line.split(" ")
    command = tokens[0]
    args = tokens[1:]
    if command in COMMANDS:
        return lambda: COMMANDS[command](*args)
    else:
        return lambda: IO_monad()

def execute_commands(list_of_commands: List[List[str]]) -> IO_monad:
    return reduce(lambda acc, x: pass_io(acc, x), list_of_commands, IO_monad())


def add(name: str, number: str, limit: str) -> IO_monad():
    card = create_card(name, [int(i) for i in number], int(limit[1:]))
    global state
    state[card.name] = card
    return IO_monad()


def charge(name: str, amount: str) -> IO_monad():
    global state
    card = state[name]
    new_card = charge_card(card, int(amount[1:]))
    state[name] = new_card
    return IO_monad()


def credit(name: str, amount: int) -> IO_monad():
    global state
    card = state[name]
    new_card = credit_card(card, int(amount[1:]))
    state[name] = new_card
    return IO_monad()


def create_card(name: str, number: List[int], limit: int, balance: int = 0) -> Card:
    return Card(name=name, balance=balance, limit=limit, number=number)

@card_pass_decorator(validate_number)
def charge_card(card: Card, amount: int) -> Card:
    return create_card(Card.name, Card.number, card.limit, Card.balance + amount)


@card_pass_decorator(validate_number)
@card_pass_decorator(validate_charge)
def credit_card(card: Card, amount: int) -> Card:
    return create_card(Card.name, Card.number, card.limit, Card.balance - amount)


def cart_to_string(card: Card) -> str:
    return "{0}: ${1}".format(card.name, card.balance)


def id(x: Any, *args) -> Any:
    return x


# def guard_decorator(validator_func: Callable[..., bool]):
#     return validate_decorator(validator_func, )

def main() -> IO_monad:
    pass


