from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, TypeVar, runtime_checkable

from array_api import Array as ArrayAPI

from ._wrapper import Wrapper

if TYPE_CHECKING:
    from ._unit import Unit as UnitAPI

Value = TypeVar("Value")
Array = TypeVar("Array", bound=ArrayAPI)


@runtime_checkable
class Quantity(Wrapper[Value], Protocol[Value]):
    """Quantity API."""

    @property
    def value(self) -> Value:
        """Value of the quantity."""

    @property
    def unit(self) -> UnitAPI:
        """Unit of the quantity."""

    @property
    def _wrapped_(self) -> Value:
        return self.value

    def to_unit(self, unit: UnitAPI) -> Quantity[Value]:
        """Convert to a new unit."""

    def to_unit_value(self, unit: UnitAPI) -> Value:
        """Convert to a new unit and return the value."""
        return self.to_unit(unit).value

    # --- Arithmetic ---

    def __add__(self, other: Quantity[Value]) -> Quantity[Value]:
        ...

    # TODO: how to type this?
    def __radd__(self, other: Quantity[Value]) -> Quantity[Value]:
        ...

    def __sub__(self, other: Quantity[Value]) -> Quantity[Value]:
        ...

    # TODO: how to type this?
    def __rsub__(self, other: Quantity[Value]) -> Quantity[Value]:
        ...

    def __mul__(self, other: Value | float) -> Quantity[Value]:
        ...

    def __rmul__(self, other: Value | float) -> Quantity[Value]:
        ...

    def __truediv__(self, other: Value | float) -> Quantity[Value]:
        ...

    def __rtruediv__(self, other: Value | float) -> Quantity[Value]:
        ...

    def __pow__(self, other: Value | float) -> Quantity[Value]:
        ...

    def __rpow__(self, other: Value | float) -> Quantity[Value]:
        ...


@runtime_checkable
class ArrayQuantity(Quantity[Array], ArrayAPI, Protocol):  # type: ignore[misc]  # pylint: disable=duplicate-bases
    """Array quantity API."""

    # --- Comparison ---

    def __eq__(self, other: Quantity[Array]) -> Array:  # type: ignore[override]
        ...

    def __ne__(self, other: Quantity[Array]) -> Array:  # type: ignore[override]
        ...

    def __lt__(self, other: Quantity[Array]) -> Array:
        ...
