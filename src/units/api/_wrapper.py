from __future__ import annotations

from typing import Any, Protocol, TypeVar, runtime_checkable

T_co = TypeVar("T_co", covariant=True)


@runtime_checkable
class Wrapper(Protocol[T_co]):
    """Wrapper API."""

    @property
    def _wrapped_(self) -> T_co:
        ...

    def __getattr__(self, name: str) -> Any:
        return getattr(self._wrapped_, name)
