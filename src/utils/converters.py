from typing import Callable, List


def convert_several(converter_fn: Callable[[object], str], items: List[object]):
    return "\n".join(map(converter_fn, items))
