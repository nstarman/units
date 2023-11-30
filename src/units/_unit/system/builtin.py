"""Built-in unit systems."""

from __future__ import annotations

__all__ = ["DimensionlessUnitSystem", "LTMAUnitSystem", "LTMAVUnitSystem"]

from dataclasses import dataclass
from typing import Annotated, final

from astropy.units import dimensionless_unscaled as apy_dimensionless

from units._dimension.builtin_dimensions import (
    angle as _angle,  # noqa: TCH001
    dimensionless as _dimensionless,  # noqa: TCH001
    length as _length,  # noqa: TCH001
    mass as _mass,  # noqa: TCH001
    speed as _speed,  # noqa: TCH001
    time as _time,  # noqa: TCH001
)
from units._unit.core import Unit

from .base import AbstractUnitSystem

_dimless_insts: dict[type[DimensionlessUnitSystem], DimensionlessUnitSystem] = {}

dimensionless_unit = Unit(apy_dimensionless)


@final
@dataclass(frozen=True)
class DimensionlessUnitSystem(AbstractUnitSystem):
    """A unit system with only dimensionless units."""

    dimensionless: Annotated[Unit, _dimensionless] = dimensionless_unit

    def __new__(cls) -> DimensionlessUnitSystem:
        # Check if instance already exists
        if cls in _dimless_insts:
            return _dimless_insts[cls]
        # Create new instance and cache it
        self = super().__new__(cls)
        _dimless_insts[cls] = self
        return self

    def __post_init__(self) -> None:
        super().__post_init__()

        if self.dimensionless is not dimensionless_unit:
            msg = "DimensionlessUnitSystem must have a dimensionless unit"
            raise ValueError(msg)

    def __str__(self) -> str:
        return "UnitSystem(dimensionless)"


@dataclass(frozen=True)
class LTMAUnitSystem(AbstractUnitSystem):
    """Length, time, mass, angle unit system."""

    length: Annotated[Unit, _length]
    time: Annotated[Unit, _time]
    mass: Annotated[Unit, _mass]
    angle: Annotated[Unit, _angle]


@dataclass(frozen=True)
class LTMAVUnitSystem(AbstractUnitSystem):
    """Length, time, mass, angle, speed unit system."""

    length: Annotated[Unit, _length]
    time: Annotated[Unit, _time]
    mass: Annotated[Unit, _mass]
    angle: Annotated[Unit, _angle]
    speed: Annotated[Unit, _speed]
