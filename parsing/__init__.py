from typing import List

from custrom_types import Command
from state import add, charge, credit
from utils import string_to_list_of_strings, compose, get_lines

COMMANDS = {
    "Add": lambda *args, **kwargs: add(*args, **kwargs),
    "Charge": lambda *args, **kwargs: charge(*args, **kwargs),
    "Credit": lambda *args, **kwargs: credit(*args, **kwargs)
}


def string_to_command(string: str) -> Command:
    list_of_strings = string_to_list_of_strings(string)
    command = list_of_strings[0]
    if command in COMMANDS:
        args = list_of_strings[1:]
        return lambda: COMMANDS[command](*args)
    else:
        return lambda: None


def list_of_strings_to_commands(strings: List[str]) -> List[Command]:
    return [string_to_command(i) for i in strings]

#IO
def get_commands() -> List[Command]:
    return compose(list_of_strings_to_commands, get_lines)()