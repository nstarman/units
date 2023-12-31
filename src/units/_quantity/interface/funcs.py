from __future__ import annotations

__all__ = ["get_interface"]

from functools import singledispatch
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .base import AbstractQuantityInterface


@singledispatch
def get_interface(obj: Any, /) -> type[AbstractQuantityInterface[Any]]:
    """Get the interface of an object."""
    msg = f"Cannot get interface of {obj.__class__.__name__!r}"
    raise TypeError(msg)
