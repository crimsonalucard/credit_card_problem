#!/usr/bin/env python3

from parsing import get_commands
from state import get_state
from display import state_to_str, print_state_string
from utils import compose


# IO
def main() -> None:
    for i in get_commands():
        i()
    compose(print_state_string, state_to_str, get_state)()
    return None


if __name__ == "__main__":
    main()
