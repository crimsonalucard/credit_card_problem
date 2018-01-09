from typing import List, Any, Callable


def string_to_list_of_strings(string: str) -> List[str]:
    return string.split(" ")


def compose(*args: Callable[[Any], Any]) -> Callable[[Any], Any]:
    if len(args) <= 0:
        return lambda x: x
    return lambda x: args[0](compose(*args[1:])(x))