from typing import Callable, Sequence, TypeVar

T = TypeVar("T")


def convert_several(converter_fn: Callable[[T], str], items: Sequence[T]) -> str:
    return "\n".join(map(converter_fn, items))
