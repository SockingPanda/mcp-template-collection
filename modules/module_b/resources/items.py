from ..server import mcp
 
@mcp.resource("details/{id}")
def details(id: str) -> str:
    """Get an item by its ID."""
    return f"Item {id} from Module B"
