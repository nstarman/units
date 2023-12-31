"""Angle."""

__all__ = ["AbstractAngle", "Angle", "Longitude", "Latitude"]

from dataclasses import dataclass, field, replace
from typing import cast, final

import astropy.units as u

from units._dimension.core import Dimension
from units._unit.core import Unit

from .base import AbstractQuantity, Array
from .core import Quantity
from .fields import UnitField, ValueField


@dataclass(frozen=True)
class AbstractAngle(AbstractQuantity[Array]):
    """Abstract Angle."""

    wrap_angle: Quantity[Array | float]

    def __post_init__(self) -> None:
        super().__post_init__()

        if self.unit.dimensions != Dimension("angle"):
            msg = f"Angle must have angular units, not {self.unit}"
            raise ValueError(msg)
        if self.wrap_angle.unit.dimensions != Dimension("angle"):
            msg = f"wrap angle must have angular units, not {self.wrap_angle.unit}"
            raise ValueError(msg)

        # TODO: apply the wrap angle to the value

    def wrap_at(
        self, wrap_angle: Quantity[Array] | None = None
    ) -> "AbstractAngle[Array]":
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
        # Apply the wrap angle to the value
        return replace(
            self,
            value=self.value % wa.to_unit_value(self.unit),
            unit=self.unit,
            wrap_angle=wa,
        )


# TODO: re-implement as Scalar, a new Type for scalars with Array-API support.
default_wrap_angle = Quantity[float](360, unit=Unit(u.deg))


@final
@dataclass(frozen=True, slots=True)
class Angle(AbstractAngle[Array]):
    """Angle."""

    value: Array = ValueField()  # type: ignore[assignment]
    unit: Unit = UnitField()  # type: ignore[assignment]
    wrap_angle: Quantity[Array | float] = field(default=default_wrap_angle)


@final
@dataclass(frozen=True, slots=True)
class Longitude(AbstractAngle[Array]):
    """Longitude."""

    value: Array = ValueField()  # type: ignore[assignment]
    unit: Unit = UnitField()  # type: ignore[assignment]
    wrap_angle: Quantity[Array | float] = field(default=default_wrap_angle)


@final
@dataclass(frozen=True, slots=True)
class Latitude(AbstractAngle[Array]):
    """Latitude."""

    value: Array = ValueField()  # type: ignore[assignment]
    unit: Unit = UnitField()  # type: ignore[assignment]
    wrap_angle: Quantity[Array | float] = field(default=default_wrap_angle)
