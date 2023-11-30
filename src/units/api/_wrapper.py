from __future__ import annotations

from typing import Any, Protocol, TypeVar, runtime_checkable

T = TypeVar("T", covariant=True)


@runtime_checkable
class Wrapper(Protocol[T]):
    @property
    def _wrapped_(self) -> T:
        ...

    def __getattr__(self, name: str) -> Any:
        return getattr(self._wrapped_, name)
