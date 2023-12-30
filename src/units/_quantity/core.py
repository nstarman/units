from __future__ import annotations

__all__ = ["Quantity"]

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Generic, NoReturn, TypeVar, cast, overload
from weakref import ref

import numpy as np
from array_api import Array as ArrayAPI, ArrayAPINamespace

from units._unit.core import Unit

if TYPE_CHECKING:
    from typing_extensions import Self

    from .interface import QuantityInterface


Array = TypeVar("Array", bound=ArrayAPI)


@dataclass(frozen=True)
class ValueField(Generic[Array]):
    """Value field descriptor.

    Builds the Interface object.
    """

    @overload
    def __get__(self, obj: Quantity[Array], obj_cls: Any) -> Array:
        ...

    @overload
    def __get__(self, obj: None, obj_cls: Any) -> NoReturn:
        ...

    def __get__(self, obj: Quantity[Array] | None, obj_cls: Any) -> Array:
        if obj is None:
            msg = "can only be accessed through an instance."
            raise AttributeError(msg)
        return obj._interface.value

    def __set__(self, obj: Quantity[Array], value: Array) -> None:
        from .interface import get_interface

        interface: type[QuantityInterface[Array]] = get_interface(value)
        object.__setattr__(obj, "_interface", interface(ref(obj), value))


# ==========================================================================


@dataclass(frozen=True, slots=True)
class UnitField:
    """Unit field descriptor."""

    def __get__(self, obj: Quantity[Array] | None, obj_cls: Any) -> Unit:
        if obj is None:
            msg = "can only be accessed through an instance."
            raise AttributeError(msg)
        return cast("Unit", obj._unit)

    def __set__(self, obj: Quantity[Array], value: Unit) -> None:
        object.__setattr__(obj, "_unit", Unit(value))


# ==========================================================================


@dataclass(frozen=True)
class Quantity(Generic[Array]):
    value: ValueField[Array] = ValueField()
    unit: UnitField = UnitField()

    def __post_init__(self) -> None:
        self._interface: QuantityInterface[Array]

    def __get_namespace__(self, api_version: str | None = None) -> ArrayAPINamespace:
        from . import array_namespce

        return array_namespce

    # --- Wrapper API ---

    @property
    def _wrapped_(self: Self) -> QuantityInterface[Array]:
        """Wrapped."""
        return self._interface

    def __getattr__(self, name: str) -> Any:
        return getattr(self._interface, name)

    # ==========================================================================
    # Quantity API

    def to_unit(self, unit: Unit) -> Quantity[Array]:
        """Convert to a new unit."""
        return self._interface.to_unit(unit)

    def to_unit_value(self, unit: Unit) -> Array:
        return self._interface.to_unit_value(unit)

    # ==========================================================================
    # ArrayQuantity API

    # --- Arithmetic ---

    def __add__(self, other: Quantity[Array]) -> Quantity[Array]:
        return self._interface + other

    def __sub__(self, other: Quantity[Array]) -> Quantity[Array]:
        return self._interface - other

    def __mul__(self, other: Quantity[Array]) -> Quantity[Array]:
        return self._interface * other

    def __truediv__(self, other: Quantity[Array]) -> Quantity[Array]:
        return self._interface / other

    # ==========================================================================
    # NumPy Overloading
    # TODO: type hints

    def __array_ufunc__(
        self, ufunc: Any, method: Any, *inputs: Any, **kwargs: Any
    ) -> Any:
        if method != "__call__":
            # TODO: dispatch to something other than `xp`
            return NotImplemented

        from . import array_namespce

        return getattr(array_namespce, ufunc.__name__)(*inputs, **kwargs, _xp=np)

    def __array_function__(
        self, func: Any, types: Any, args: tuple[Any, ...], kwargs: dict[str, Any]
    ) -> Any:
        from . import array_namespce

        return getattr(array_namespce, func.__name__)(*args, **kwargs, _xp=np)
