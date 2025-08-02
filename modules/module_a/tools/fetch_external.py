from ..server import mcp
from ..internal.core import repository


@mcp.tool("fetch_external_data")
async def fetch_external_data(item_id: str) -> dict:
    """Fetch data by ``item_id`` using the shared repository."""
    return await repository.get_or_fetch(item_id)
