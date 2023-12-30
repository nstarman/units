from __future__ import annotations

__all__ = ["Unit"]

from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, Any, TypeVar, cast, overload

from astropy.units import UnitBase as APYUnit  # noqa: TCH002

from units._dimension.core import Dimension
from units._dimension.utils import get_dimension_name
from units.api._unit import Array as ArrayAPI

if TYPE_CHECKING:
    from units._quantity.core import Quantity


Array = TypeVar("Array", bound=ArrayAPI)


@dataclass(frozen=True)
class Unit:
    """Unit.

    .. todo::

        Remove the ``Wrapper`` stuff when this is part of Astropy.

    """

    wrapped: APYUnit

    @property
    def _wrapped_(self) -> APYUnit:
        return self.wrapped

    @property
    def dimensions(self) -> Dimension:
        """Dimension of the unit."""
        return Dimension(get_dimension_name(self._wrapped_))

    def __repr__(self) -> str:
        return f"{type(self).__name__}({repr(self.wrapped)[5:-1]})"

    # --- Addition ---

    def __add__(self, other: Unit) -> Unit:
        if not other.wrapped.is_equivalent(self.wrapped):
            msg = f"Cannot add units {self} and {other}."
            raise ValueError(msg)
        return self

    def __sub__(self, other: Unit) -> Unit:
        if not other.wrapped.is_equivalent(self.wrapped):
            msg = f"Cannot subtract units {self} and {other}."
            raise ValueError(msg)
        return self

    # --- Multiplication ---

    @overload
    def __mul__(self, other: Unit) -> Unit:  # type: ignore[overload-overlap]
        ...

    @overload
    def __mul__(self, other: Array) -> Quantity[Array]:
        ...

    def __mul__(self, other: Unit | Array) -> Unit | Quantity[Array]:
        if isinstance(other, Unit):
            return replace(self, wrapped=self.wrapped * other.wrapped)

        from units._quantity.core import Quantity

        return Quantity(other, unit=self.wrapped)

    # --- Division ---

    @overload
    def __truediv__(self, other: Unit) -> Unit:
        ...

    @overload
    def __truediv__(self, other: Array) -> Quantity[Array]:
        ...

    def __truediv__(self, other: Unit | Array) -> Unit | Quantity[Array]:
        if isinstance(other, Unit):
            return replace(self, wrapped=self.wrapped / other.wrapped)

        from units._quantity.core import Quantity

        return Quantity(cast("Array", 1.0 / other), self.wrapped)

    # --- Power ---

    def __pow__(self, other: Any) -> Unit:
        return replace(self, wrapped=self.wrapped**other)
