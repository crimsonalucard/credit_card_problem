from card import create_card, charge_card, credit_card
from custrom_types import Card
from typing import Dict
from utils import string_of_nums_to_list_of_ints, dollar_to_number

state: Dict[str, Card] = {}


# IO
def get_state():
    global state
    return state


# IO
def add(name: str, number: str, limit: str) -> None:
    card = create_card(name, string_of_nums_to_list_of_ints(number), dollar_to_number(limit))
    global state
    state[card.name] = card


# IO
def charge(name: str, amount: str) -> None:
    global state
    if name in state:
        card: Card = get_card(name)
        new_card: Card = charge_card(card, int(amount[1:]))
        set_card(new_card)


# IO
def credit(name: str, amount: int) -> None:
    global state
    if name in state:
        card: Card = get_card(name)
        new_card: Card = credit_card(card, int(amount[1:]))
        set_card(new_card)


# IO
def get_card(name: str) -> Card:
    global state
    if name not in state:
        raise KeyError
    else:
        return state[name]


# IO
def set_card(card: Card) -> None:
    global state
    state[card.name] = card
