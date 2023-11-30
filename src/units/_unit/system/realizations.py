"""Realizations of unit systems."""

from __future__ import annotations

__all__ = ["dimensionless", "galactic", "solarsystem"]

import astropy.units as u

from units._unit.core import Unit

from .builtin import DimensionlessUnitSystem, LTMAUnitSystem, LTMAVUnitSystem

# Dimensionless. This is a singleton.
dimensionless = DimensionlessUnitSystem()

# Galactic unit system
galactic = LTMAVUnitSystem(
    Unit(u.kpc), Unit(u.Myr), Unit(u.Msun), Unit(u.radian), Unit(u.km / u.s)
)

# Solar system units
solarsystem = LTMAUnitSystem(Unit(u.au), Unit(u.Msun), Unit(u.yr), Unit(u.radian))
