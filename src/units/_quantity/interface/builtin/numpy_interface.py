from __future__ import annotations

__all__ = ["LegacyNumPyQuantityInterface"]

from numbers import Number
from typing import Any, TypeVar

import numpy as np
from array_api import Array as ArrayAPI, ArrayAPINamespace
from array_api_compat import numpy as numpy_compat
from numpy import array_api

from units._quantity.interface.base import AbstractQuantityInterface

Array = TypeVar("Array", bound=ArrayAPI)


class LegacyNumPyQuantityInterface(
    AbstractQuantityInterface[Array], register=(Number, np.ndarray)
):
    """Interface for pre-Array-API numpy arrays."""

    def __wrapped_array_namespace__(
        self, *, api_version: Any = None
    ) -> ArrayAPINamespace:
        return numpy_compat


class NumPyQuantityInterface(
    AbstractQuantityInterface[Array], register=array_api._array_object.Array
):
    """Interface for Array-API compatible numpy arrays."""

    def __wrapped_array_namespace__(
        self, *, api_version: Any = None
    ) -> ArrayAPINamespace:
        return array_api
