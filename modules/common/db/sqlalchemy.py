"""SQLAlchemy-based implementation of :class:`AbstractAsyncDatabase`."""

from __future__ import annotations

from typing import Any

from sqlalchemy import Column, String, JSON
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from .base import AbstractAsyncDatabase

Base = declarative_base()


class KeyValue(Base):
    """Simple key-value table."""

    __tablename__ = "key_value"

    key = Column(String, primary_key=True)
    value = Column(JSON)


class SQLAlchemyDatabase(AbstractAsyncDatabase):
    """Async key-value store backed by SQLAlchemy."""

    def __init__(self, engine: AsyncEngine) -> None:
        self._engine = engine
        self._sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    @classmethod
    async def create(cls, url: str, **engine_kwargs: Any) -> "SQLAlchemyDatabase":
        """Create a database for ``url`` and initialize tables."""
        engine = create_async_engine(url, **engine_kwargs)
        self = cls(engine)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        return self

    async def get(self, key: str) -> Any:
        async with self._sessionmaker() as session:
            obj = await session.get(KeyValue, key)
            return obj.value if obj else None

    async def set(self, key: str, value: Any) -> None:
        async with self._sessionmaker() as session:
            await session.merge(KeyValue(key=key, value=value))
            await session.commit()

    async def exists(self, key: str) -> bool:
        async with self._sessionmaker() as session:
            obj = await session.get(KeyValue, key)
            return obj is not None

    async def delete(self, key: str) -> None:
        async with self._sessionmaker() as session:
            obj = await session.get(KeyValue, key)
            if obj is not None:
                await session.delete(obj)
                await session.commit()
