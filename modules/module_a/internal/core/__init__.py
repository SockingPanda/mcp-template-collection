"""Core setup for module A."""

import asyncio
import os

from ....common.core import DataRepository
from ....common.db import SQLAlchemyDatabase
from ..api.client import fetch_data

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///module_a.db")
_db = asyncio.run(SQLAlchemyDatabase.create(DATABASE_URL))

# Repository exposed for module tools
repository = DataRepository(_db, fetch_data)

__all__ = ["repository"]
