"""Unit utils."""
from __future__ import annotations

__all__: list[str] = []

from functools import singledispatch
from typing import Any

from astropy.units import PhysicalType, UnitBase, get_physical_type

_apy_speed = get_physical_type("speed")


@singledispatch
def get_dimension_name(pt: Any, /) -> str:
    msg = f"Cannot get dimension name from {pt!r}."
    raise TypeError(msg)


@get_dimension_name.register
def _get_dimension_name_from_str(pt: str, /) -> str:
    return "_".join(pt.split("_"))


@get_dimension_name.register
def _get_dimension_name_from_astropy_dimension(pt: PhysicalType, /) -> str:
    # TODO: this is not deterministic b/c ``_physical_type`` is a set
    #       that's why the `if` statement is needed.
    if pt == _apy_speed:
        return "speed"
    return _get_dimension_name_from_str(next(iter(pt._physical_type)))


@get_dimension_name.register
def _get_dimension_name_from_unit(pt: UnitBase, /) -> str:
    return _get_dimension_name_from_astropy_dimension(pt.physical_type)
