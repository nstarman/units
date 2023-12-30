from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, overload, runtime_checkable

if TYPE_CHECKING:
    from collections.abc import Iterator

    from array_api import ArrayAPINamespace
    from typing_extensions import Self

    from ._dimension import Dimension, DimensionSystem
    from ._quantity import Quantity


class Array(Protocol):
    """Array API."""

    def __array_namespace__(self, *, api_version: str | None) -> ArrayAPINamespace:
        ...

    def __mul__(self, other: Array | float) -> Array:
        ...

    def __truediv__(self, other: Array | float) -> Array:
        ...

    def __rtruediv__(self, other: Array | float) -> Array:
        ...


@runtime_checkable
class Unit(Protocol):
    """Unit API."""

    @property
    def dimensions(self) -> Dimension:
        """Dimension of the unit."""

    # --- Arithmetic ---

    def __add__(self: Self, other: Self) -> Self:
        ...

    def __sub__(self: Self, other: Self) -> Self:
        ...

    @overload
    def __mul__(self: Self, other: Self) -> Self:
        ...

    @overload
    def __mul__(self: Self, other: Array) -> Quantity[Array]:
        ...

    def __mul__(self: Self, other: Self | Array) -> Self | Quantity[Array]:
        ...

    @overload
    def __truediv__(self: Self, other: Self) -> Self:
        ...

    @overload
    def __truediv__(self: Self, other: Array) -> Quantity[Array]:
        ...

    def __truediv__(self: Self, other: Self | Array) -> Self | Quantity[Array]:
        ...


# ============================================================================


@runtime_checkable
class UnitSystem(Protocol):
    """Unit system API."""

    @property
    def base_units(self) -> tuple[Unit, ...]:
        """Tuple of core units."""

    @property
    def dimension_system(self) -> DimensionSystem:
        """Dimension system."""

    # def __getitem__(self, key: str | Unit | Dimension) -> Unit:
    #     ...

    def __len__(self) -> int:
        return len(self.base_units)

    def __iter__(self) -> Iterator[Unit]:
        yield from self.base_units
