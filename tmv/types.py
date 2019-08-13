import collections.abc
from typing import Iterable, Mapping, Type, Union

PRIMITIVE_TYPES = (str, int, bool, float)

Primitive = Type[Union[str, int, bool, float]]

ITERABLE_TYPES: Mapping[Type[Iterable], Type[Iterable]] = {
    collections.abc.Iterable:   tuple,
    collections.abc.Collection: tuple,
    collections.abc.Sequence:   tuple,
    tuple:                      tuple,
    list:                       list,
    collections.abc.Set:        frozenset,
    set:                        set
}

MAPPING_TYPES = (collections.abc.Mapping, dict)


def type_name(cls: Type) -> str:
    for attr in ("__name__", "name", "_name"):
        if hasattr(cls, attr):
            return getattr(cls, attr)
    return str(cls)
