"""Generic data repository for async fetch-and-cache workflows."""

from typing import Any, Awaitable, Callable

from ..db import SQLAlchemyDatabase

FetchFn = Callable[[str], Awaitable[Any]]


class DataRepository:
    """High-level helper that consults a SQLAlchemy database before fetching.

    Parameters
    ----------
    db:
        Instance of :class:`SQLAlchemyDatabase` used for persistence.
    fetch_fn:
        Coroutine function used to retrieve data when it is missing from the
        database.
    """

    def __init__(self, db: SQLAlchemyDatabase, fetch_fn: FetchFn) -> None:
        self._db = db
        self._fetch_fn = fetch_fn

    async def get_or_fetch(self, key: str) -> Any:
        """Return cached value for ``key`` or fetch and store it."""
        if await self._db.exists(key):
            return await self._db.get(key)
        value = await self._fetch_fn(key)
        await self._db.set(key, value)
        return value
