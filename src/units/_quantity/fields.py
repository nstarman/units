from __future__ import annotations

__all__ = ["ValueField", "UnitField"]

from dataclasses import dataclass, is_dataclass
from typing import TYPE_CHECKING, Any, Generic, TypeVar, cast, overload
from weakref import ref

from array_api import Array as ArrayAPI
from astropy.units import Unit as APYUnit

from units._quantity.interface.funcs import get_interface
from units._unit.core import Unit

if TYPE_CHECKING:
    from typing_extensions import Self

    from units._quantity.interface.base import AbstractQuantityInterface

    from .base import AbstractQuantity

Array = TypeVar("Array", bound=ArrayAPI)

#####################################################################


@dataclass(frozen=True, slots=True)
class ValueField(Generic[Array]):
    """Value field descriptor.

    Builds the Interface object.
    """

    @overload
    def __get__(self, obj: AbstractQuantity[Array], obj_cls: Any) -> Array:
        ...

    @overload
    def __get__(self, obj: None, obj_cls: Any) -> Self:
        ...

    def __get__(
        self, obj: AbstractQuantity[Array] | None, obj_cls: Any
    ) -> Array | Self:
        # Get from class
        if obj is None:
            # If this is being set as part of a dataclass constructor, then we
            # raise an AttributeError. This is to prevent the Field from being
            # set as the default value of the dataclass field and erroneously
            # included in the class' ``__init__`` signature.
            if not is_dataclass(obj_cls) or "value" not in obj_cls.__dataclass_fields__:
                raise AttributeError
            return self

        # Get from instance
        return obj.interface.value

    def __set__(self, obj: AbstractQuantity[Array], value: Array) -> None:
        interface: type[AbstractQuantityInterface[Array]] = get_interface(value)
        object.__setattr__(
            obj, "interface", interface(ref(obj), value)  # pylint: disable=not-callable
        )


@dataclass(frozen=True)
class UnitField:
    """Unit field descriptor."""

    @overload
    def __get__(self, obj: AbstractQuantity[Array], obj_cls: Any) -> Unit:
        ...

    @overload
    def __get__(self, obj: None, obj_cls: Any) -> Self:
        ...

    def __get__(self, obj: AbstractQuantity[Array] | None, obj_cls: Any) -> Unit | Self:
        # Get from class
        if obj is None:
            # If this is being set as part of a dataclass constructor, then we
            # raise an AttributeError. This is to prevent the Field from being
            # set as the default value of the dataclass field and erroneously
            # included in the class' ``__init__`` signature.
            if not is_dataclass(obj_cls) or "unit" not in obj_cls.__dataclass_fields__:
                raise AttributeError
            return self

        return cast(Unit, obj._unit)

    def __set__(self, obj: AbstractQuantity[Array], unit: Unit | str) -> None:
        if not isinstance(unit, Unit):
            unit = Unit(APYUnit(unit))
        object.__setattr__(obj, "_unit", unit)
