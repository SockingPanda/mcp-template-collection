import asyncio
import pathlib
import sys

import pytest

sys.path.append(str(pathlib.Path(__file__).resolve().parents[4]))

from modules.common.db import SQLAlchemyDatabase  # type: ignore
from sqlalchemy.pool import StaticPool


def test_sqlalchemy_database_crud():
    async def run():
        db = await SQLAlchemyDatabase.create(
            "sqlite+aiosqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        await db.set("a", {"v": 1})
        assert await db.exists("a") is True
        assert await db.get("a") == {"v": 1}
        await db.delete("a")
        assert await db.exists("a") is False

    asyncio.run(run())
