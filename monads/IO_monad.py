import sys
from typing import Any, Union, List, Callable, IO


class IO_monad:

    def __init__(self, io_funcs: Any = None, teardowns=None):
        self.io_calls: List[Callable[..., Any]] = [] if io_funcs is None else io_funcs if isinstance(io_funcs,
                                                                                                     list) else [
            io_funcs]
        self.teardowns: List[Callable[..., Any]] = [] if teardowns is None else teardowns if isinstance(teardowns,
                                                                                                        list) else [
            teardowns]

    def __ge__(self, other):
        return bind_io(self, other)

    def __gt__(self, other):
        return pass_io(self, other)


def bind_io(x: IO_monad, func: Callable[[Any], IO_monad]) -> IO_monad:
    io_monad_to_append: IO_monad = func(x.io_calls[-1]())
    return IO_monad(x.io_calls[:-1] + io_monad_to_append.io_calls, x.teardowns + io_monad_to_append.teardowns)


def pass_io(x: IO_monad, y: IO_monad) -> IO_monad:
    return IO_monad(x.io_calls + y.io_calls, x.teardowns + y.teardowns)


def eval_io(x: IO_monad):
    for func in x.io_calls:
        func()
    for func in x.teardowns:
        func()


def readline_IO(file: IO) -> IO_monad:
    def return_line():
        try:
            return file.__next__()
        except StopIteration:
            file.close()
            return None

    return IO_monad(return_line, file.close)


def get_file_descipter_from_string(filename: str) -> IO_monad:
    try:
        return IO_monad(lambda: open(filename))
    except FileNotFoundError:
        return IO_monad()


def get_file_descripter_from_stdin() -> IO_monad:
    return IO_monad(lambda: sys.stdin)


def get_file_descripter() -> IO_monad:
    if len(sys.argv) > 1:
        return get_file_descipter_from_string(sys.argv[1])
    else:
        return get_file_descripter_from_stdin()


def print_string(input_str: str) -> IO_monad:
    return IO_monad(lambda: print(input_str))


def close_IO(file: IO) -> IO_monad:
    return IO_monad(lambda: file.close())


def runtime(func: Callable[..., IO_monad]) -> None:
    io: IO_monad = func()
    eval_io(io)
