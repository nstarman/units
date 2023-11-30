"""Unit utils."""
from __future__ import annotations

__all__: list[str] = []

from typing import Annotated, Any, TypeGuard

_annot_type = type(Annotated[int, "_"])


def is_annotated(hint: Any, /, annot_type: Any = _annot_type) -> TypeGuard[_annot_type]:
    """Check if a type hint is an `Annotated` type."""
    return type(hint) is annot_type
