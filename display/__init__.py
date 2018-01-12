from custrom_types import Card, State
from utils import identity
from validators import validate_decorator, validate_number
from typing import List
from functools import reduce

def display_card_error(card: Card) -> str:
    return "{0}: error".format(card.name)


@validate_decorator(validate_number, identity, display_card_error)
def card_to_string(card: Card) -> str:
    return "{0}: ${1}".format(card.name, card.balance)

def state_to_str(state: State) -> List[str]:
    return reduce(lambda acc, key: acc + [card_to_string(state[key])], state, [])

#IO
def print_state_string(state_strings: List[str]) -> None:
    for string in state_strings:
        print(string)