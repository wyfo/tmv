# TMV (Type Model Visitor)

Visitor for type models using typing annotations.

## What's inside?

The package contains an *abstract* `Visitor` class which needs by-type methods implementation. Only (some of) the standard types are supported:
- primitives (`int`, `str`, `float`, `bool`)
- iterables
- mappings
- tuples
- dataclasses
- `Enum`, `Any`, `Tuple`, `Union`, `Optional`, `Literal`, `NewType`
- *soon* `TypedDict` (PEP 589), `Annotated` (PEP 593), etc.

Unsupported types are handled in `unsupported` method, of which default implementation raises `Unsupported` exception.

`Visitor` offers support for custom types through 2 methods `ìs_custom` and `custom`. The return value of `is_custom` is passed to `custom` when evaluated to `True`; it's thus convenient to use an optional return type. Customs types are handled before others classes like dataclasses or enumerations (to enable custom handling for them).

See [apischema](https://github.com/wyfo/apischema/) for concrete use of the package

## Comments
- If an abstract class was at first considered for `Visitor` implementation, raising `NotImplementedError` has been chosen because it enable an easier use, especially in case of partial implementation (which would imply to overwrite with `NotImplementedError` in case of `ABC` inheritance)
- For convenience, inheritance is not handled in this project. In fact, if `__bases__` and even `__orig_bases__` could be used, this would raises other issues like multiple inheritance. Moreover, some implementation could rely on `__init__` method (it's the case *apischema* from which this project was originally extracted), and inheritance makes things fuzzy on this point.
- Customs type could be handled in an overwrite of `unsupported` method, but this would make impossible to handle *custom* dataclasses, that's why a dedicated method is used