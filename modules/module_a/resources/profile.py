from ..server import mcp

@mcp.resource("profile/{id}")
def profile(id: str) -> str:
    """Get a resource by its ID."""
    return f"Resource {id} from Module A"
