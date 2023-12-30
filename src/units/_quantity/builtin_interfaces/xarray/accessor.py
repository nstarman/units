from __future__ import annotations

__all__: list[str] = []

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from xarray import register_dataarray_accessor

if TYPE_CHECKING:
    from xarray.core.dataarray import DataArray

    from units._unit.core import Unit


@register_dataarray_accessor("units")
@dataclass
class PintDataArrayAccessor:
    """Access methods for DataArrays with units using Pint.

    Methods and attributes can be accessed through the `.pint` attribute.
    """

    da: DataArray

    # def quantify(self, units=None, unit_registry=None, **unit_kwargs):
    #     return self.da.pipe(conversion.strip_unit_attributes).pipe(
    #         conversion.attach_units, new_units
    #     )

    @property
    def value(self) -> Any:
        """The magnitude of the data or the data itself if not a quantity."""
        data = self.da.data
        return getattr(data, "value", data)

    @property
    def unit(self) -> Unit | Any:
        """The magnitude of the data or the data itself if not a quantity."""
        data = self.da.data
        return getattr(data, "unit", None)

    @unit.setter
    def unit(self, unit: Unit) -> None:
        raise NotImplementedError
        # self.da.data = conversion.array_attach_unit(self.da.data, unit)

    def to_unit(self, unit: Unit) -> DataArray:
        """Convert to a new unit."""
        raise NotImplementedError
        # return conversion.convert_units(self.da, unit)

    # def to_unit_value(self, unit):
    #     return conversion.convert_units(self.da, unit).data
