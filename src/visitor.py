from dataclasses import is_dataclass
from enum import Enum
from types import FunctionType
from typing import (Any, Generic, Iterable, Mapping, Sequence, Tuple, Type,
                    TypeVar, Union, cast)

from src import Unsupported
from src.types import (ITERABLE_TYPES, MAPPING_TYPES, PRIMITIVE_TYPES,
                       Primitive)

try:
    from typing_extensions import Literal
except ImportError:
    Literal = None  # type: ignore

Path = Tuple[str, ...]

ReturnType = TypeVar("ReturnType")
Context = TypeVar("Context")


class Visitor(Generic[ReturnType, Context]):
    def __init__(self):
        self._generics: Mapping[TypeVar, Type] = {}

    def unsupported(self, cls: Type, ctx: Context):
        raise Unsupported(cls)

    def primitive(self, cls: Primitive, ctx: Context) -> ReturnType:
        raise NotImplementedError()

    def optional(self, value: Type, ctx: Context) -> ReturnType:
        raise NotImplementedError()

    def union(self, alternatives: Iterable[Type], ctx: Context) -> ReturnType:
        raise NotImplementedError()

    def iterable(self, cls: Type[Iterable], value_type: Type,
                 ctx: Context) -> ReturnType:
        raise NotImplementedError()

    def mapping(self, key_type: Type, value_type: Type,
                ctx: Context) -> ReturnType:
        raise NotImplementedError()

    def tuple(self, types: Sequence[Type], ctx: Type):
        raise NotImplementedError()

    def literal(self, values: Sequence[Any], ctx: Context) -> ReturnType:
        raise NotImplementedError()

    def is_custom(self, cls: Type, ctx: Context) -> Any:
        """
        `Visitor.custom` will be called with the result of this method
        if it returns a truthy value
        """
        return False

    def custom(self, custom: Any, ctx: Context) -> ReturnType:
        raise NotImplementedError()

    def dataclass(self, cls: Type, ctx: Context) -> ReturnType:
        raise NotImplementedError()

    def enum(self, cls: Type[Enum], ctx: Context) -> ReturnType:
        raise NotImplementedError()

    def any(self, ctx: Context) -> ReturnType:
        raise NotImplementedError()

    def visit(self, cls: Type, ctx: Context) -> ReturnType:
        # 'Optimization' for more current types
        if cls in PRIMITIVE_TYPES:
            return self.primitive(cast(Primitive, cls), ctx)
        if hasattr(cls, "__origin__"):
            origin = cls.__origin__  # type: ignore
            # noinspection PyUnresolvedReferences
            args = cls.__args__  # type: ignore
            if origin is Union:
                if len(args) == 2 and type(None) in args:
                    return self.optional(args[0], ctx)
                else:
                    return self.union(args, ctx)
            if Literal is not None and origin is Literal:
                return self.literal(args, ctx)
            if origin is tuple and (not len(args) == 2 or args[1] is not ...):
                return self.tuple(args, ctx)
            if origin in ITERABLE_TYPES:
                return self.iterable(ITERABLE_TYPES[origin], args[0], ctx)
            if origin in MAPPING_TYPES:
                return self.mapping(args[0], args[1], ctx)
            try:
                generics_items = zip((p for p in origin.__parameters__), args)
            except AttributeError:
                return self.unsupported(cls, ctx)
            # Use stack save to not overwhelm the visitor calls
            generics_save = self._generics
            self._generics = {}
            for tv, value in generics_items:
                self._generics[tv] = generics_save.get(value, value)
            res = self.visit(origin, ctx)
            self._generics = generics_save
            return res
        # customs are handled before other classes
        # (dataclass could has to handled as custom for example)
        custom = self.is_custom(cls, ctx)
        if custom:
            return self.custom(custom, ctx)
        if is_dataclass(cls):
            return self.dataclass(cls, ctx)
        if isinstance(cls, TypeVar):  # type: ignore
            if cls not in self._generics:
                return self.unsupported(cls, ctx)
            return self.visit(self._generics[cls], ctx)
        try:
            if issubclass(cls, Enum):
                # noinspection PyTypeChecker
                return self.enum(cls, ctx)
        except TypeError:
            pass
        if cls is Any:
            return self.any(ctx)
        # NewType handling
        if isinstance(cls, FunctionType):
            if hasattr(cls, "__supertype__"):
                return self.visit(cls.__supertype__, ctx)
            else:
                return self.unsupported(cls, ctx)
        return self.unsupported(cls, ctx)
