from __future__ import annotations

__all__: list[str] = []

from dataclasses import replace
from typing import TYPE_CHECKING

from dask.array import Array
from dask.dataframe import DataFrame, Series

from units._quantity.interface import QuantityInterface

if TYPE_CHECKING:
    from units._quantity.core import Quantity


class DaskArrayInterface(QuantityInterface[Array], register=Array):
    def to_dask_dataframe(self) -> Quantity[DataFrame]:
        return replace(self.quantity, value=self.value.to_dask_dataframe())


class DaskDataFrameInterface(
    QuantityInterface[DataFrame], register=(DataFrame, Series)
):
    def to_dask_array(self) -> Quantity[Array]:
        return replace(self.quantity, value=self.value.to_dask_array())
