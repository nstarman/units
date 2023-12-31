from __future__ import annotations

__all__ = ["Quantity"]

from dataclasses import dataclass
from typing import TypeVar

from array_api import Array as ArrayAPI

from units._quantity.base import AbstractQuantity
from units._quantity.fields import UnitField, ValueField
from units._unit.core import Unit  # noqa: TCH001

Array = TypeVar("Array", bound=ArrayAPI)


@dataclass(frozen=True)
class Quantity(AbstractQuantity[Array]):
    """Quantity."""

    value: Array = ValueField()  # type: ignore[assignment]
    unit: Unit = UnitField()  # type: ignore[assignment]
