from __future__ import annotations

__all__ = ["AbstractQuantity"]

from abc import ABCMeta
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Generic, Protocol, TypeVar

import numpy as np
from array_api import Array as ArrayAPI, ArrayAPINamespace
from mypy_extensions import trait

from units._unit.core import Unit

from . import array_namespace

if TYPE_CHECKING:
    from numbers import Number

    from typing_extensions import Self

    from units._quantity.interface import AbstractQuantityInterface
    from units.api import Quantity as QuantityAPI


Array = TypeVar("Array", bound=ArrayAPI)


#####################################################################


@trait
class NumPyMixin(Protocol):  # TODO: proper type hints
    """Mixin for NumPy NEP13,18-style overloading."""

    def __array_ufunc__(
        self: ArrayAPI, ufunc: Any, method: Any, *inputs: Any, **kwargs: Any
    ) -> Any:
        if method != "__call__":
            # TODO: dispatch to something other than `xp`
            return NotImplemented

        xp = self.__array_namespace__()
        func = getattr(xp, ufunc.__name__)
        return func(*inputs, **kwargs, _xp=np)  # TODO: allow general xp

    def __array_function__(
        self: ArrayAPI,
        func: Any,
        types: Any,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> Any:
        xp = self.__array_namespace__()
        func = getattr(xp, func.__name__)
        return func(*args, **kwargs, _xp=np)  # TODO: allow general xp


# ======================================================================


@trait
class LegacyQuantityMixin(Protocol[Array]):
    """Indefinite support for non-API methods."""

    def to(self: QuantityAPI[Array], unit: Unit) -> QuantityAPI[Array]:
        return self.to_unit(unit)

    def to_value(self: QuantityAPI[Array], unit: Unit) -> Array:
        return self.to_unit_value(unit)


# ======================================================================


@dataclass(frozen=True)
class AbstractQuantity(
    Generic[Array],
    LegacyQuantityMixin[Array],
    NumPyMixin,
    metaclass=ABCMeta,
):
    value: Array
    unit: Unit

    def __post_init__(self) -> None:
        self.interface: AbstractQuantityInterface[Array]
        return  # just for super.

    # --- Wrapper API ---

    @property
    def _wrapped_(self: Self) -> AbstractQuantityInterface[Array]:
        """Wrapped."""
        return self.interface

    def __getattr__(self, name: str) -> Any:
        return getattr(self.interface, name)

    # ==========================================================================
    # Quantity API

    def to_unit(self, unit: Unit | str) -> AbstractQuantity[Array]:
        """Convert to a new unit."""
        return self.interface.to_unit(
            Unit(unit) if not isinstance(unit, Unit) else unit
        )

    def to_unit_value(self, unit: Unit | str) -> Array:
        return self.interface.to_unit_value(
            Unit(unit) if not isinstance(unit, Unit) else unit
        )

    # ==========================================================================
    # Array API

    def __array_namespace__(self, api_version: str | None = None) -> ArrayAPINamespace:
        return array_namespace

    # ==========================================================================
    # ArrayQuantity API

    # --- Arithmetic ---

    def __add__(self, other: AbstractQuantity[Array]) -> AbstractQuantity[Array]:
        return self.interface + other

    def __sub__(self, other: AbstractQuantity[Array]) -> AbstractQuantity[Array]:
        return self.interface - other

    def __mul__(self, other: AbstractQuantity[Array]) -> AbstractQuantity[Array]:
        return self.interface * other

    def __truediv__(self, other: AbstractQuantity[Array]) -> AbstractQuantity[Array]:
        return self.interface / other

    def __pow__(self, other: Number) -> AbstractQuantity[Array]:
        return self.interface**other
