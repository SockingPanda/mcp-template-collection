from ..server import mcp

@mcp.prompt("summary")
def summary(text: str) -> str:
    """Get a summary prompt."""
    return f"请用 2 句话概述以下内容：\n\n{text}" 