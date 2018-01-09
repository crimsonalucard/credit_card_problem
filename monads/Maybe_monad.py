from typing import Any, Union, Callable


class Just:
    def __init__(self, value: Any) -> None:
        self.__value: Any = value


class Error:
    def __init__(self, error: Any) -> None:
        self.__value: Any = error


Maybe_monad = Union[Just, Error]


def bind_maybe(x: Maybe_monad, func: Callable[[Any], Maybe_monad]) -> Maybe_monad:
    return x if isinstance(x, Error) else func(x.__value)


def pass_maybe(x: Maybe_monad, func: Callable[[Any], Maybe_monad]) -> Maybe_monad:
    return Error(x.__value)