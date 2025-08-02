"""Internal API client stubs for module A."""

import asyncio
from typing import Any, Dict


async def fetch_data(item_id: str) -> Dict[str, Any]:
    """Simulate fetching data for ``item_id`` from an external API."""
    await asyncio.sleep(0)  # simulate I/O delay
    return {"id": item_id, "value": f"external-{item_id}"}
