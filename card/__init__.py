from typing import List

from custrom_types import Card
from validators import card_pass_decorator, validate_charge, validate_number


def create_card(name: str, number: List[int], limit: int, balance: int = 0) -> Card:
    return Card(name=name, balance=balance, limit=limit, number=number)


@card_pass_decorator(validate_charge)
def charge_card(card: Card, amount: int) -> Card:
    return credit_card(card, -amount)


@card_pass_decorator(validate_number)
def credit_card(card: Card, amount: int) -> Card:
    return create_card(card.name, card.number, card.limit, card.balance - amount)