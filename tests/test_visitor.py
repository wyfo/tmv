from dataclasses import dataclass
from enum import Enum
from typing import (AbstractSet, Any, Dict, Generic, Iterable, List, Mapping,
                    NewType, Optional, Sequence, Set, Sized, Tuple, TypeVar,
                    Union)
from unittest.mock import Mock

from pytest import mark, raises
from typing_extensions import Literal

from src.errors import UNSUPPORTED_TYPE, Unsupported
from src.visitor import Visitor


class EnumExample(Enum):
    A = "a"
    B = "b"


@dataclass
class DataclassExample:
    a: int
    b: str


T = TypeVar("T")


@dataclass
class GenericExample(Generic[T]):
    attr: T


def func():
    pass


@mark.parametrize("cls, method, args", [
    (int, Visitor.primitive, (int,)),
    (str, Visitor.primitive, (str,)),
    (Tuple[str, int], Visitor.tuple, ((str, int),)),
    (List[int], Visitor.iterable, (list, int)),
    (Tuple[str, ...], Visitor.iterable, (tuple, str)),
    (Sequence[int], Visitor.iterable, (tuple, int)),
    (AbstractSet[int], Visitor.iterable, (frozenset, int)),
    (Iterable[int], Visitor.iterable, (tuple, int)),
    (Set[int], Visitor.iterable, (set, int)),
    (Mapping[str, int], Visitor.mapping, (str, int)),
    (Dict[str, int], Visitor.mapping, (str, int)),
    (EnumExample, Visitor.enum, (EnumExample,)),
    (Literal[1, 2], Visitor.literal, ((1, 2),)),
    (Optional[int], Visitor.optional, (int,)),
    (Union[int, str], Visitor.union, ((int, str),)),
    (Any, Visitor.any, ()),
    (DataclassExample, Visitor.dataclass, (DataclassExample,)),
    (GenericExample[int], Visitor.visit, (GenericExample,)),
    (NewType("int2", int), Visitor.visit, (int,)),
    (Generic, Visitor.unsupported, (Generic,)),
    (0, Visitor.unsupported, (0,)),
    (func, Visitor.unsupported, (func,)),
    (Sized, Visitor.unsupported, (Sized,)),
])
def test_native_types(cls, method, args):
    visitor = Mock()
    Visitor.__init__(visitor)
    visitor.is_custom.return_value = False
    Visitor.visit(visitor, cls, None)
    getattr(visitor, method.__name__) \
        .assert_called_once_with(*(*args, None))


def test_generic_types():
    visitor = Mock()
    Visitor.__init__(visitor)
    visitor.is_custom.return_value = False

    def visit(*args):
        assert visitor._generics == {T: int}

    visitor.visit = visit
    Visitor.visit(visitor, GenericExample[int], None)


def test_type_var():
    visitor = Mock()
    visitor.is_custom.return_value = False

    visitor._generics = {}
    Visitor.visit(visitor, T, None)
    visitor.unsupported.assert_called_once_with(T, None)

    visitor._generics = {T: int}
    Visitor.visit(visitor, T, None)
    visitor.visit.assert_called_once_with(int, None)


class Custom:
    pass


@mark.parametrize("is_custom, method", [
    (None, Visitor.unsupported),
    (Custom, Visitor.custom),
])
def test_custom_types(is_custom, method):
    visitor = Mock()
    visitor.is_custom.return_value = is_custom
    Visitor.visit(visitor, Custom, None)
    getattr(visitor, method.__name__) \
        .assert_called_once_with(Custom, None)


def test_unsupported():
    error = UNSUPPORTED_TYPE.format(type_name="Iterable")
    with raises(Unsupported, match=error):
        Visitor.unsupported(Mock(), Iterable[str], None)


def test_default_is_custom():
    assert Visitor.is_custom(Mock(), Mock(), Mock()) is False
