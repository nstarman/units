"""Unit utils."""

from __future__ import annotations

__all__: list[str] = []

from typing import (  # type: ignore[attr-defined]
    Annotated,
    Any,
    TypeGuard,
    _AnnotatedAlias,
)

AnnotationType = type(Annotated[int, "_"])


def is_annotated(hint: Any) -> TypeGuard[_AnnotatedAlias]:
    """Check if a type hint is an `Annotated` type."""
    return type(hint) is AnnotationType  # pylint: disable=unidiomatic-typecheck
