from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from typing_extensions import Self

    from ._dimension import Dimension, DimensionSystem


@runtime_checkable
class Unit(Protocol):
    """Unit API."""

    @property
    def dimensions(self) -> Dimension:
        """Dimension of the unit."""
        ...

    # --- Arithmetic ---

    def __add__(self: Self, other: Self) -> Self:
        ...

    def __sub__(self: Self, other: Self) -> Self:
        ...

    def __mul__(self: Self, other: Self) -> Self:
        ...

    def __truediv__(self: Self, other: Self) -> Self:
        ...


@runtime_checkable
class UnitSystem(Protocol):
    """Unit system API."""

    @property
    def base_units(self) -> tuple[Unit, ...]:
        """List of core units."""
        ...

    @property
    def dimension_system(self) -> DimensionSystem:
        """Dimension system."""
        ...

    # def __getitem__(self, key: str | Unit | Dimension) -> Unit:
    #     ...

    def __len__(self) -> int:
        return len(self.base_units)

    def __iter__(self) -> Unit:
        yield from self.base_units
