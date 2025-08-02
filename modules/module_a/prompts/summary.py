from ..server import mcp

@mcp.prompt("summary")
def summary(text: str) -> str:
    """Get a prompt by its ID."""
    return f"请用 3 句话总结以下内容：\n\n{text}"
