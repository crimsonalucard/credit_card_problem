from typing import List, Any, Callable, IO
import sys


def string_to_list_of_strings(string: str) -> List[str]:
    return string.split(" ")


def compose(*args: Callable[..., Any]) -> Callable[..., Any]:
    if len(args) == 1:
        return lambda *inner_args: args[0](*inner_args)
    return lambda *inner_args: args[0](compose(*args[1:])(*inner_args))


def identity(*args) -> Any:
    return None if len(args) < 1 else args[0]

#IO
def get_file_from_stdin() -> IO:
    return sys.stdin

#IO
def get_file_from_string(string):
    return open(string)

#IO
def get_lines_from_file(fd: IO) -> List[str]:
    return [line for line in fd]

#IO
def get_file() -> IO:
    return get_file_from_string(sys.argv[1]) if len(sys.argv) > 1 else get_file_from_stdin()

#IO
def get_lines() -> List[str]:
    return compose(get_lines_from_file, get_file)()


def string_of_nums_to_list_of_ints(string) -> List[int]:
    return [int(i) for i in string]


def dollar_to_number(dollars: str) -> int:
    if dollars[0] == '$' and dollars[1:].strip().isnumeric():
        return int(dollars[1:].strip())
    else:
        print(dollars)
        raise ValueError