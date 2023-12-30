"""Unit utils."""

from __future__ import annotations

__all__: list[str] = []

from typing import Any, ClassVar, TypeVar

T = TypeVar("T")


# ============================================================================


class SingletonMeta(type):
    """Metaclass for Singleton classes."""

    _instances: ClassVar[dict[type, type]] = {}

    def __call__(cls: type[T], *args: Any, **kwargs: Any) -> T:
        # Check if instance already exists
        instances: dict[type[T], T] = cls._instances  # type: ignore[attr-defined]

        if cls not in instances:
            instance = super().__call__(*args, **kwargs)  # type: ignore[misc]
            instances[cls] = instance

        return instances[cls]
