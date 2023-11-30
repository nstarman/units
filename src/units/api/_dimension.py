from __future__ import annotations

from collections.abc import Mapping  # noqa: TCH003
from typing import Protocol, runtime_checkable


@runtime_checkable
class Dimension(Protocol):
    """Dimension API."""


@runtime_checkable
class DimensionSystem(Protocol):
    """Dimension system API."""

    base_dimensions: tuple[Dimension, ...]
    derived_dimensions: Mapping[Dimension, Mapping[Dimension, int]]
    cache: bool = True

    @property
    def names(self) -> tuple[str, ...]:
        """Names of the base dimensions."""
        ...

    def __len__(self) -> int:
        return len(self.base_dimensions)

    def __iter__(self) -> Dimension:
        yield from self.base_dimensions
