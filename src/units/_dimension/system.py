"""Base UnitSystem class."""

from __future__ import annotations

__all__ = ["DimensionSystem"]


from dataclasses import KW_ONLY, dataclass, field
from types import MappingProxyType
from typing import TYPE_CHECKING, final

from units.api import DimensionSystem as DimensionSystemAPI

from .core import Dimension  # noqa: TCH001
from .utils import get_dimension_name

if TYPE_CHECKING:
    from collections.abc import Mapping


_DIMENSIONSYSTEM_REGISTRY: dict[tuple[Dimension, ...], DimensionSystem] = {}


# TODO: enforce immutability with a convert argument
@final
@dataclass(frozen=True)
class DimensionSystem(DimensionSystemAPI):
    """System of dimensions."""

    base_dimensions: tuple[Dimension, ...]
    # TODO: should this be in comparison?
    derived_dimensions: Mapping[
        Dimension,
        Mapping[Dimension, int],
    ] = field(
        default_factory=lambda: MappingProxyType({})
    )  # type: ignore[assignment]
    _: KW_ONLY
    cache: bool = True

    def __new__(
        cls: type[DimensionSystem],
        base_dimensions: tuple[Dimension, ...],
        derived_dimensions: Mapping[Dimension, Mapping[Dimension, int]],  # noqa: ARG003
        *,
        cache: bool = True,
    ) -> DimensionSystem:
        # Check if instance already exists
        if cache and (base_dimensions in _DIMENSIONSYSTEM_REGISTRY):
            return _DIMENSIONSYSTEM_REGISTRY[base_dimensions]
        # Create new instance and optionally cache it
        self = super().__new__(cls)
        if cache:
            _DIMENSIONSYSTEM_REGISTRY[base_dimensions] = self
        return self

    @property  # TODO: cached property
    def names(self) -> tuple[str, ...]:
        return tuple(get_dimension_name(dim) for dim in self.base_dimensions)
