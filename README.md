# TMV (Type Model Visitor)

Visitor for type models using typing annotations.

## What's inside?

The package contains an *abstract* `Visitor` class which needs by-type methods implementation. Only (some of) the standard types are supported:
- primitives (`int`, `str`, `float`, `bool`)
- iterables (`List` --> `list`, `Set` --> `set`, `Sequence` --> `tuple`, `AbstractSet` --> `frozenset)
- mappings (`Mapping`, `Dict`)
- tuples (`tuple`)
- dataclasses (`@dataclass`)
- `Enum`, `Any`, `Union`, `Optional`, `Literal`, `NewType`
- *soon* `TypedDict` (PEP 589), `Annotated` (PEP 593), etc.

Unsupported types are handled in `unsupported` method, of which default implementation raises `Unsupported` exception.

`Visitor` offers support for custom types through 2 methods `ìs_custom` and `custom`. Customs types are handled before others classes like dataclasses or enumerations (to enable custom handling for them, which would be impossible if they were handled in `unsupported`).

See [apischema](https://github.com/wyfo/apischema/) for concrete use of the package

## Comments
- If an abstract class was at first considered for `Visitor` implementation, raising `NotImplementedError` has been chosen because it enable an easier use, especially in case of partial implementation (which would imply to overwrite with `NotImplementedError` in case of `ABC` inheritance)
- For now, in a matter of simplicity, only a subset of iterables types are handled (and `Iterable` is not!).