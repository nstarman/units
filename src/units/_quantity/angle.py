from __future__ import annotations

from typing import cast

__all__ = ["Angle"]

from dataclasses import KW_ONLY, dataclass, replace

import astropy.units as u

from units._dimension.core import Dimension
from units._unit.core import Unit

from .core import Array, Quantity

_deg = Unit(u.deg)


@dataclass(frozen=True)
class Angle(Quantity[Array]):
    """Angle."""

    _: KW_ONLY
    wrap_angle: Quantity[Array | float] = Quantity[Array | float](360, unit=_deg)

    def __post_init__(self) -> None:
        super().__post_init__()

        if self.unit.dimensions != Dimension("angle"):
            msg = f"Angle must have angular units, not {self.unit}"
            raise ValueError(msg)
        if self.wrap_angle.unit.dimensions != Dimension("angle"):
            msg = f"wrap angle must have angular units, not {self.wrap_angle.unit}"
            raise ValueError(msg)

        # TODO: apply the wrap angle to the value

    def wrap_at(self, wrap_angle: Quantity[Array] | None = None) -> Angle[Array]:
        """Wrap the angle at the given value.

        Parameters
        ----------
        wrap_angle : Quantity[Array], optional
            Wrap angle, by default None.

        Returns
        -------
        Angle[Array]
            Wrapped angle.
        """
        wa = cast(
            "Quantity[Array | float]",
            self.wrap_angle if wrap_angle is None else wrap_angle,
        )
        return replace(
            self,
            value=self.value % wa.to_unit_value(self.unit),
            unit=self.unit,
            wrap_angle=wa,
        )
