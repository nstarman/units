"""Base UnitSystem class."""

from __future__ import annotations

__all__ = ["Dimension"]


from dataclasses import dataclass
from typing import final

from astropy.units import PhysicalType, get_physical_type

from units.api import Dimension as DimensionAPI
from units.api._wrapper import Wrapper

from .utils import get_dimension_name

_DIMENSIONS_CACHE: dict[str, Dimension] = {}


@final
@dataclass(frozen=True)
class Dimension(DimensionAPI, Wrapper[PhysicalType]):
    """System of dimensions.

    .. todo::

        Remove the ``Wrapper`` when decouple from Astropy.
    """

    name: str

    def __new__(cls, name: str | PhysicalType | Dimension, /) -> Dimension:
        # Dimension is a singleton based on the name, so we cache it.
        name_ = name if isinstance(name, str) else get_dimension_name(name)
        if name_ in _DIMENSIONS_CACHE:
            return _DIMENSIONS_CACHE[name_]
        return super().__new__(cls)

    def __init__(self, name: str | PhysicalType | Dimension, /) -> None:
        object.__setattr__(  # TODO: this with `converter` arg to `field`
            self, "name", name if isinstance(name, str) else get_dimension_name(name)
        )
        object.__setattr__(self, "_wrapped", get_physical_type(self.name))

    @property
    def _wrapped_(self) -> PhysicalType:
        return self._wrapped


@get_dimension_name.register  # type: ignore[misc]
def _get_dimension_name_from_dimension(pt: Dimension, /) -> str:
    return pt.name
