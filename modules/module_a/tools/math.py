from ..server import mcp

@mcp.tool("add")
def add(a: int, b: int) -> int:
    """Add two integers and return their sum."""
    print(f"Adding {a} and {b}")
    return a + b

@mcp.tool("subtract")
def subtract(a: int, b: int) -> int:
    """Subtract two integers and return their difference."""
    print(f"Subtracting {b} from {a}")
    return a - b
