from typing import Type

from src import type_name

UNSUPPORTED_TYPE = "Unsupported '{type_name}' type"


class Unsupported(Exception):
    def __init__(self, cls: Type):
        self.cls = cls

    def __str__(self) -> str:
        return UNSUPPORTED_TYPE.format(type_name=type_name(self.cls))
