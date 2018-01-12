from typing import NamedTuple, List, Callable, Dict


class Card(NamedTuple):
    name: str
    balance: int
    limit: int
    number: List[int]


Command = Callable[[], None]

State = Dict[str, Card]