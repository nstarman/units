"""Built-in unit systems."""

from __future__ import annotations

__all__ = ["dimensionless", "length", "mass", "speed", "time", "angle"]

from .core import Dimension

dimensionless = Dimension("dimensionless")
length = Dimension("length")
mass = Dimension("mass")
time = Dimension("time")
speed = Dimension("speed")
angle = Dimension("angle")
