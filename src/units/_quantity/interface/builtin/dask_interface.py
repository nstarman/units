from __future__ import annotations

__all__: list[str] = []

from dataclasses import replace
from typing import TYPE_CHECKING, Any

import dask.array as da  # pylint: disable=import-error
from dask.array import Array  # pylint: disable=import-error
from dask.dataframe import DataFrame, Series  # pylint: disable=import-error

from units._quantity.interface import AbstractQuantityInterface

if TYPE_CHECKING:
    from array_api import ArrayAPINamespace

    from units._quantity.base import AbstractQuantity


class LegacyDaskArrayInterface(AbstractQuantityInterface[Array], register=Array):
    """Interface for `dask.array.Array`."""

    def __wrapped_array_namespace__(
        self, *, api_version: Any = None
    ) -> ArrayAPINamespace:
        return da

    def to_dask_dataframe(self) -> AbstractQuantity[DataFrame]:
        """Convert to a `dask.dataframe.DataFrame`."""
        return replace(self.quantity, value=self.value.to_dask_dataframe())


class DaskDataFrameInterface(
    AbstractQuantityInterface[DataFrame], register=(DataFrame, Series)
):
    """Interface for `dask.dataframe.DataFrame`."""

    def __wrapped_array_namespace__(
        self, *, api_version: Any = None
    ) -> ArrayAPINamespace:
        return da

    def to_dask_array(self) -> AbstractQuantity[Array]:
        """Convert to a `dask.array.Array`."""
        return replace(self.quantity, value=self.value.to_dask_array())
