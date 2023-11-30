"""Unit utils."""
from __future__ import annotations

__all__: list[str] = ["equivalent"]

from .base import AbstractUnitSystem


# TODO: make this singledispatch. Would prefer multiple dispatch.
def equivalent(a: AbstractUnitSystem, b: AbstractUnitSystem, /) -> bool:
    """Check if two units are equivalent."""
    if not isinstance(a, AbstractUnitSystem) or not isinstance(b, AbstractUnitSystem):  # type: ignore[redundant-expr]
        msg = f"Expected `AbstractUnitSystem`, got {type(a)}, {type(b)}."  # type: ignore[unreachable]
        raise TypeError(msg)

    return set(a._dimensions) == set(b._dimensions)
