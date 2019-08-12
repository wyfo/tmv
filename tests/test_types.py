from typing import List, NewType, TypeVar

from pytest import mark

from src.types import type_name

T = TypeVar("T")


@mark.parametrize("cls, expected", [
    (int, "int"),
    (List[str], "List"),
    (T, "T"),
    (NewType("int2", int), "int2"),
    ("type", "type")
])
def test_type_name(cls, expected):
    assert type_name(cls) == expected
