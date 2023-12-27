from __future__ import annotations

__all__ = ["get_wrapped_namespace", "cos", "sin"]

from dataclasses import replace
from typing import TYPE_CHECKING, Any

from astropy.units import rad as _apy_rad

from units._quantity.up import result_unit
from units._unit.core import Unit

if TYPE_CHECKING:
    from array_api import Array as ArrayAPI, ArrayAPINamespace

    from units._quantity.base import AbstractQuantity


def get_wrapped_namespace(
    *xs: AbstractQuantity[ArrayAPI], api_version: str | None = None
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
        namespaces.add(x.interface.__wrapped_array_namespace__(api_version=api_version))

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
