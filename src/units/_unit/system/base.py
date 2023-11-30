"""Base UnitSystem class."""

from __future__ import annotations

__all__ = ["AbstractUnitSystem", "UNITSYSTEMS_REGISTRY"]

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import ClassVar, get_args, get_type_hints

from units._dimension.core import Dimension
from units._dimension.system import DimensionSystem
from units._dimension.utils import get_dimension_name
from units._unit.core import Unit
from units.api import UnitSystem as UnitSystemAPI

from .utils import is_annotated

_UNITSYSTEMS_REGISTRY: dict[tuple[Dimension, ...], type[AbstractUnitSystem]] = {}
UNITSYSTEMS_REGISTRY = MappingProxyType(_UNITSYSTEMS_REGISTRY)


@dataclass(frozen=True)
class AbstractUnitSystem(UnitSystemAPI):
    """Abstract base class for unit systems."""

    _base_field_names: ClassVar[tuple[str, ...]]
    _dimension_system: ClassVar[DimensionSystem]

    _registry: dict[Dimension, Unit] = field(init=False, repr=False)

    def __init_subclass__(cls) -> None:
        # Register class with a tuple of it's dimensions.
        # This requires processeing the type hints, not the dataclass fields
        # since those are made after the original class is defined.
        type_hints = get_type_hints(cls, include_extras=True)

        field_names = []
        dimensions_ = []
        for name, type_hint in type_hints.items():
            # Check it's Annotated
            if not is_annotated(type_hint):
                continue

            # Get the arguments to Annotated
            origin, *f_args = get_args(type_hint)

            # Check that the first argument is a UnitBase
            if not issubclass(origin, Unit):
                continue

            # Need for one of the arguments to be a PhysicalType
            f_dims = [x for x in f_args if isinstance(x, Dimension)]
            if not f_dims:
                msg = f"Field {name} must be an Annotated with a dimension."
                raise TypeError(msg)
            if len(f_dims) > 1:
                msg = f"Field {name} must be an Annotated with only one dimension."
                raise TypeError(msg)

            field_names.append(get_dimension_name(name))
            dimensions_.append(f_dims[0])

        dimensions = tuple(dimensions_)  # freeze

        # Check the unitsystem is not already registered
        if dimensions in _UNITSYSTEMS_REGISTRY:
            msg = f"Unit system with dimensions {dimensions} already exists."
            raise ValueError(msg)

        # check that the field names match the dimensions
        dimensionsystem = DimensionSystem(dimensions, {})
        if set(field_names) != set(dimensionsystem.names):
            msg = f"Field names {field_names} do not match dimensions {dimensionsystem.names}."
            raise ValueError(msg)

        # Add attributes to the class
        cls._base_field_names = tuple(field_names)
        cls._dimension_system = dimensionsystem

        # Register the class
        _UNITSYSTEMS_REGISTRY[dimensions] = cls

    def __post_init__(self) -> None:
        registry = {unit.dimensions: unit for unit in self.base_units}
        object.__setattr__(self, "_registry", registry)

    @property
    def base_units(self) -> tuple[Unit, ...]:
        """List of core units."""
        return tuple(getattr(self, k) for k in self._base_field_names)

    @property
    def dimension_system(self) -> DimensionSystem:
        """Dimension system."""
        return self._dimension_system

    @property
    def _dimensions(self) -> tuple[Dimension, ...]:
        """Dimensions of the unit system."""
        return tuple(self._registry.keys())
