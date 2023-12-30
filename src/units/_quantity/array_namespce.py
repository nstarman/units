from __future__ import annotations

__all__ = ["get_wrapped_namespace", "cos", "sin"]

import math
from collections.abc import Sequence
from dataclasses import replace
from numbers import Number
from typing import Any

import numpy as np
from array_api import Array as ArrayAPI, ArrayAPINamespace
from astropy.units import rad as _apy_rad

from units._unit.core import Unit

from .up import result_unit


def get_wrapped_namespace(
    *xs: Any, api_version: str | None = None
) -> ArrayAPINamespace:
    """Get the namespace of the wrapped array.

    Parameters
    ----------
    xs : Any
        Quantity-like objects.
    api_version : str or None, optional
        Array API version, by default `None`.

    Returns
    -------
    ArrayAPINamespace
        Array API namespace.
    """
    # `xs` contains one or more arrays.
    namespaces = set()
    for x in xs:
        if isinstance(x.value, ArrayAPI):
            namespaces.add(x.value.__array_namespace__(api_version=api_version))
        # Backwards compatibility
        elif isinstance(x.value, (np.ndarray, np.generic, Sequence)):
            namespaces.add(np)
        elif isinstance(x.value, Number):  # type: ignore[unreachable]
            namespaces.add(math)

    if not namespaces:
        msg = "Unrecognized array input"
        raise ValueError(msg)
    if len(namespaces) != 1:
        msg = f"Multiple namespaces for array inputs: {namespaces}"
        raise ValueError(msg)

    return namespaces.pop()


_rad = Unit(_apy_rad)


def cos(x: Any, /, *, _xp: ArrayAPINamespace | None = None) -> Any:
    """Cosine."""
    xp = get_wrapped_namespace(x) if _xp is None else _xp
    return replace(
        x, value=xp.cos(x.to_unit_value(_rad)), unit=result_unit("cos", x.unit)
    )


def sin(x: Any, /, *, _xp: ArrayAPINamespace | None = None) -> Any:
    """Sine."""
    xp = get_wrapped_namespace(x) if _xp is None else _xp
    return replace(
        x, value=xp.sin(x.to_unit_value(_rad)), unit=result_unit("sin", x.unit)
    )
