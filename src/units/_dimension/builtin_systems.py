"""Built-in unit systems."""

from __future__ import annotations

__all__ = ["dimensionless_system", "ltma_system", "ltmav_system"]


from .builtin_dimensions import angle, dimensionless, length, mass, speed, time
from .system import DimensionSystem

dimensionless_system = DimensionSystem((dimensionless,), {}, cache=True)
ltma_system = DimensionSystem((length, time, mass, angle), {}, cache=True)
ltmav_system = DimensionSystem((length, time, mass, angle, speed), {}, cache=True)
