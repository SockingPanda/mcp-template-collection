import asyncio
import pathlib
import sys

import pytest
from sqlalchemy.pool import StaticPool

sys.path.append(str(pathlib.Path(__file__).resolve().parents[4]))

from modules.common.core import DataRepository
from modules.common.db import SQLAlchemyDatabase


def test_get_or_fetch_uses_cache():
    async def run():
        db = await SQLAlchemyDatabase.create(
            "sqlite+aiosqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        calls = {"count": 0}

        async def fetch(key: str):
            calls["count"] += 1
            return {"id": key}

        repo = DataRepository(db, fetch)

        result1 = await repo.get_or_fetch("x")
        result2 = await repo.get_or_fetch("x")

        assert result1 == {"id": "x"}
        assert result2 == {"id": "x"}
        assert calls["count"] == 1

    asyncio.run(run())
