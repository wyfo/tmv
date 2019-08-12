import collections.abc
from typing import Type, Union

PRIMITIVE_TYPES = (str, int, bool, float)

Primitive = Type[Union[str, int, bool, float]]

ITERABLE_TYPES = (collections.abc.Sequence, list,
                  collections.abc.Set, set)

MAPPING_TYPES = (collections.abc.Mapping, dict)


def iterable_type(cls: Type) -> Type:
    assert issubclass(cls, collections.abc.Iterable)
    if cls is list:
        return list
    if cls is collections.abc.Sequence:
        return tuple
    if cls is set:
        return set
    if cls is collections.abc.Set:
        return frozenset
    raise NotImplementedError()


def type_name(cls: Type) -> str:
    for attr in ("__name__", "name", "_name"):
        if hasattr(cls, attr):
            return getattr(cls, attr)
    return str(cls)
