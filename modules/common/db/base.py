"""Async database interface for repositories.

This module defines :class:`AbstractAsyncDatabase`, an abstract base class
that outlines the minimal asynchronous CRUD operations used throughout the
project. Concrete database implementations must provide all of the methods
defined here.
"""

from abc import ABC, abstractmethod
from typing import Any


class AbstractAsyncDatabase(ABC):
    """Abstract base class for asynchronous key-value databases."""

    @abstractmethod
    async def get(self, key: str) -> Any:  # pragma: no cover - interface
        """Retrieve a value by *key*."""

    @abstractmethod
    async def set(self, key: str, value: Any) -> None:  # pragma: no cover - interface
        """Store ``value`` under ``key``."""

    @abstractmethod
    async def exists(self, key: str) -> bool:  # pragma: no cover - interface
        """Return ``True`` if ``key`` is present."""

    @abstractmethod
    async def delete(self, key: str) -> None:  # pragma: no cover - interface
        """Remove ``key`` and its value if present."""
