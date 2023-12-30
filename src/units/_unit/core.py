from __future__ import annotations

__all__ = ["Unit"]

from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, overload

from astropy.units import UnitBase as APYUnit  # noqa: TCH002

from units._dimension.core import Dimension
from units._dimension.utils import get_dimension_name

if TYPE_CHECKING:
    from units._quantity.core import Quantity
    from units.api._unit import Array


@dataclass(frozen=True)
class Unit:
    """Unit.

    .. todo::

        Remove the ``Wrapper`` stuff when decouple from Astropy.

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

    # --- Arithmetic ---

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

    @overload
    def __mul__(self, other: Unit) -> Unit:
        ...

    @overload
    def __mul__(self, other: Array) -> Quantity[Array]:
        ...

    def __mul__(self, other: Unit | Array) -> Unit | Quantity[Array]:
        if isinstance(other, Unit):
            return replace(self, wrapped=self.wrapped * other.wrapped)

        from units._quantity.core import Quantity

        return Quantity(other, self.wrapped)

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

        return Quantity(1.0 / other, self.wrapped)
