"""Make unit systems."""

from __future__ import annotations

__all__ = ["unitsystem"]


from dataclasses import make_dataclass
from typing import cast

from astropy.units import UnitBase as APYUnit  # noqa: TCH002

from units._dimension.utils import get_dimension_name
from units._unit.core import Unit

from .base import UNITSYSTEMS_REGISTRY, AbstractUnitSystem


def unitsystem(*units: AbstractUnitSystem | Unit | APYUnit) -> AbstractUnitSystem:
    """Create a new unit system from the given units.

    Parameters
    ----------
    *units
        The units to use. Can be a single UnitSystem or a list of units.

    Returns
    -------
    AbstractUnitSystem
        The unit system.
    """
    if isinstance(units[0], AbstractUnitSystem):
        if len(units) > 1:
            msg = "If passing in a UnitSystem, cannot pass in additional units."
            raise ValueError(msg)

        return units[0]

    # Validate the units
    if not all(isinstance(x, Unit) for x in units):
        msg = "All units must be a `UnitBase` instances."
        raise TypeError(msg)

    units = cast("tuple[Unit, ...]", units)

    # Check if the unit system is already registered
    base_dimensions = tuple(x.dimensions for x in units)
    if base_dimensions in UNITSYSTEMS_REGISTRY:
        return UNITSYSTEMS_REGISTRY[base_dimensions](*units)

    # Otherwise, create a new unit system
    # dimension names of all the units
    dim_names = tuple(get_dimension_name(x) for x in units)
    # name: physical types joined by underscores
    cls_name = "".join(x.capitalize() for x in dim_names) + "UnitSystem"
    # fields: name, unit
    fields = [(n, Unit) for n in dim_names]
    # make the dataclass
    unitsystem_cls: type[AbstractUnitSystem] = make_dataclass(
        cls_name,
        fields,
        bases=(AbstractUnitSystem,),
        frozen=True,
    )

    return unitsystem_cls(*units)
