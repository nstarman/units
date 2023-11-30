from dataclasses import dataclass

from xarray import register_dataarray_accessor
from xarray.core.dataarray import DataArray

__all__: list[str] = []


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
    def value(self):
        """The magnitude of the data or the data itself if not a quantity."""
        data = self.da.data
        return getattr(data, "value", data)

    @property
    def unit(self):
        """The magnitude of the data or the data itself if not a quantity."""
        data = self.da.data
        return getattr(data, "unit", None)

    @unit.setter
    def unit(self, unit):
        self.da.data = conversion.array_attach_unit(self.da.data, unit)

    def to_unit(self, unit):
        """Convert to a new unit."""
        return conversion.convert_units(self.da, unit)

    # def to_unit_value(self, unit):
    #     return conversion.convert_units(self.da, unit).data
