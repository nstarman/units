from __future__ import annotations

__all__ = []

from dataclasses import replace
from typing import Any

from dask.array import Array
from dask.dataframe import DataFrame, Series

from units._quantity.interface import QuantityInterface


class DaskArrayInterface(QuantityInterface[Any, Array], register=Array):
    def to_dask_dataframe(self) -> DaskDataFrameInterface[DataFrame]:
        return replace(self.quantity, value=self.value.to_dask_dataframe())


class DaskDataFrameInterface(
    QuantityInterface[Any, DataFrame], register=(DataFrame, Series)
):
    def to_dask_array(self) -> DaskArrayInterface[Array]:
        return replace(self.quantity, value=self.value.to_dask_array())
