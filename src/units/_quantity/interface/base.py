from __future__ import annotations

__all__ = ["AbstractQuantityInterface"]

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, Any, Generic, TypeVar, cast
from weakref import ReferenceType  # noqa: TCH003

from array_api import Array as ArrayAPI, ArrayAPINamespace

from units._quantity import array_namespace
from units._quantity.base import AbstractQuantity, NumPyMixin
from units._quantity.interface.funcs import get_interface
from units.api import Quantity as QuantityAPI

if TYPE_CHECKING:
    from numbers import Number

    from units._unit.core import Unit

Array = TypeVar("Array", bound=ArrayAPI)
T = TypeVar("T")


@dataclass(frozen=True)
class Registrant(Generic[T]):
    """Registrant."""

    value: type[T]

    def __call__(self, *_: Any, **__: Any) -> type[T]:
        return self.value


@dataclass(frozen=False, slots=True)
class AbstractQuantityInterface(NumPyMixin, Generic[Array], metaclass=ABCMeta):
    quantity_ref: ReferenceType[AbstractQuantity[Array]]
    value: Array

    # ------------------
    # Class construction

    def __init_subclass__(cls, register: type | tuple[type, ...]) -> None:
        # TODO: raises "TypeError: super(type, obj): obj must be an instance or
        # subtype of type" super().__init_subclass__()

        # Register the interface
        registers = register if isinstance(register, tuple) else (register,)
        for typ in registers:
            get_interface.register(typ, Registrant(cls))

    # ------------------

    @abstractmethod
    def __wrapped_array_namespace__(
        self, *, api_version: str | None = None
    ) -> ArrayAPINamespace:
        ...

    @property
    def quantity(self) -> AbstractQuantity[Array]:
        out = self.quantity_ref()
        if out is None:
            msg = "Quantity has been deleted."
            raise ReferenceError(msg)
        return out

    # --- Quantity API ---

    @property
    def unit(self) -> Unit:
        return self.quantity.unit

    def to_unit(self, unit: Unit) -> AbstractQuantity[Array]:
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

    # --- Array API ---

    def __array_namespace__(self, api_version: str | None = None) -> ArrayAPINamespace:
        return array_namespace

    # --- Wrapper API ---

    @property
    def _wrapped_(self) -> Array:
        """Wrapped."""
        return self.value

    def __getattr__(self, name: str) -> Any:
        return getattr(self._wrapped_, name)

    # --- Arithmetic ---
    # TODO: altneratively, this could be supported in the `xp` functions?

    def __add__(self, other: AbstractQuantity[Array]) -> AbstractQuantity[Array]:
        return replace(
            self.quantity,
            value=self.value + other.to_unit_value(self.unit),
            unit=self.unit,
        )

    def __sub__(self, other: AbstractQuantity[Array]) -> AbstractQuantity[Array]:
        return replace(
            self.quantity,
            value=self.value - other.to_unit_value(self.unit),
            unit=self.unit,
        )

    def __mul__(
        self, other: Array | AbstractQuantity[Array]
    ) -> AbstractQuantity[Array]:
        if not isinstance(other, QuantityAPI):
            return replace(self.quantity, value=self.value * other, unit=self.unit)
        return replace(
            self.quantity,
            value=self.value * other.value,
            unit=cast("Unit", self.unit * other.unit),
        )

    def __truediv__(
        self, other: Array | AbstractQuantity[Array]
    ) -> AbstractQuantity[Array]:
        if not isinstance(other, QuantityAPI):
            return replace(self.quantity, value=self.value / other, unit=self.unit)
        return replace(
            self.quantity,
            value=self.value / other.value,
            unit=cast("Unit", self.unit / other.unit),
        )

    def __pow__(self, other: Number) -> AbstractQuantity[Array]:
        return replace(
            self.quantity, value=self.value**other, unit=self.unit**other
        )


@get_interface.register(AbstractQuantityInterface)
def _get_interface_qi(
    obj: AbstractQuantityInterface[Any], /
) -> type[AbstractQuantityInterface[Any]]:
    return obj.__class__  # allows user overrides of the type.
