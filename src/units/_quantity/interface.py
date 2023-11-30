from __future__ import annotations

__all__: list[str] = []

from dataclasses import dataclass, replace
from functools import singledispatch
from numbers import Number
from typing import Any, Generic, TypeVar, cast
from weakref import ReferenceType

import numpy as np
from array_api import Array as ArrayAPI, ArrayAPINamespace

from units._unit.core import Unit
from units.api import Quantity as QuantityAPI

from .core import Quantity

QT = TypeVar("QT", bound=Quantity)
T = TypeVar("T")
Array = TypeVar("Array", bound=ArrayAPI)


@dataclass(frozen=True)
class Registrant(Generic[T]):
    """Registrant."""

    value: type[T]

    def __call__(self, *_: Any, **__: Any) -> type[T]:
        return self.value


@dataclass(frozen=False)
class QuantityInterface(Generic[QT, Array]):
    quantity_ref: ReferenceType[Quantity[Array]]
    value: Array

    def __init_subclass__(cls, register: type | tuple[type, ...]) -> None:
        super().__init_subclass__()

        # Register the interface
        registers = register if isinstance(register, tuple) else (register,)
        for typ in registers:
            get_interface.register(typ, Registrant(cls))

    def __post_init__(self) -> None:
        self._unit: Unit

    @property
    def quantity(self) -> Quantity[Array]:
        out = self.quantity_ref()
        if out is None:
            msg = "Quantity has been deleted."
            raise ReferenceError(msg)
        return out

    @property
    def unit(self) -> Unit:
        return self.quantity.unit

    def to_unit(self, unit: Unit) -> Quantity[Array]:
        """Convert to a new unit."""
        # TODO: self.value * self.unit.to(unit) doesn't work for temperatures
        #       This is for illustration purposes only.
        return replace(
            self.quantity,
            value=self.value * self.unit.wrapped.to(unit.wrapped),
            unit=unit,
        )

    def to_unit_value(self, unit: Unit) -> Array:
        # TODO: self.value * self.unit.to(unit) doesn't work for temperatures
        #       This is for illustration purposes only.
        return cast(Array, self.value * self.unit.wrapped.to(unit.wrapped))

    def __get_namespace__(self, api_version: str | None = None) -> ArrayAPINamespace:
        from . import xp

        return xp

    # --- Wrapper API ---

    @property
    def _wrapped_(self) -> Array:
        """Wrapped."""
        return self.value

    def __getattr__(self, name: str) -> Any:
        return getattr(self._wrapped_, name)

    # --- Arithmetic ---

    def __add__(self, other: Quantity[Array]) -> Quantity[Array]:
        return replace(
            self.quantity,
            value=self.value + other.to_unit_value(self.unit),
            unit=self.unit,
        )

    def __sub__(self, other: Quantity[Array]) -> Quantity[Array]:
        return replace(
            self.quantity,
            value=self.value - other.to_unit_value(self.unit),
            unit=self.unit,
        )

    def __mul__(self, other: Array | Quantity[Array]) -> Quantity[Array]:
        if not isinstance(other, QuantityAPI):
            return replace(self.quantity, value=self.value * other, unit=self.unit)
        return replace(
            self.quantity, value=self.value * other.value, unit=self.unit * other.unit
        )

    def __truediv__(self, other: Array | Quantity[Array]) -> Quantity[Array]:
        if not isinstance(other, QuantityAPI):
            return replace(self.quantity, value=self.value / other, unit=self.unit)
        return replace(
            self.quantity, value=self.value / other.value, unit=self.unit / other.unit
        )

    # --- NumPy Overloading ---

    def __array_ufunc__(
        self, ufunc: Any, method: Any, *inputs: Any, **kwargs: Any
    ) -> Any:
        if method != "__call__":
            # TODO! dispatch to something other than `xp`
            return NotImplemented

        from . import xp

        return getattr(xp, ufunc.__name__)(*inputs, **kwargs, _xp=np)

    def __array_function__(
        self, func: Any, types: Any, args: tuple[Any, ...], kwargs: dict[str, Any]
    ) -> Any:
        from . import xp

        return getattr(xp, func.__name__)(*args, **kwargs, _xp=np)


##############################################################################


@singledispatch
def get_interface(obj: Any, /) -> type[QuantityInterface]:
    """Get the interface of an object."""
    msg = f"Cannot get interface of {obj.__class__.__name__!r}"
    raise TypeError(msg)


@get_interface.register(QuantityInterface)
def _get_interface_qi(obj: QuantityInterface, /) -> type[QuantityInterface]:
    return obj.__class__


@get_interface.register(Number)
def _get_interface_number(_: Number | np.ndarray, /) -> type[QuantityInterface]:
    return QuantityInterface


@get_interface.register(np.ndarray)
def _get_interface_ndarray(_: np.ndarray, /) -> type[QuantityInterface]:
    return QuantityInterface
