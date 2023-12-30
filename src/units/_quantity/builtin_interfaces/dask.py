from __future__ import annotations

__all__: list[str] = []

from dataclasses import replace
from typing import TYPE_CHECKING

from dask.array import Array  # pylint: disable=import-error
from dask.dataframe import DataFrame, Series  # pylint: disable=import-error

from units._quantity.interface import QuantityInterface

if TYPE_CHECKING:
    from units._quantity.core import Quantity


class DaskArrayInterface(QuantityInterface[Array], register=Array):
    """Dask :class:`~dask.array.Array` interface."""

    def to_dask_dataframe(self) -> Quantity[DataFrame]:
        """Convert dask Array to dask Dataframe."""
        return replace(self.quantity, value=self.value.to_dask_dataframe())


class DaskDataFrameInterface(
    QuantityInterface[DataFrame], register=(DataFrame, Series)
):
    """Dask :class:`~dask.dataframe.DataFrame` interface."""

    def to_dask_array(self) -> Quantity[Array]:
        """Convert dask Dataframe to dask Array."""
        return replace(self.quantity, value=self.value.to_dask_array())
