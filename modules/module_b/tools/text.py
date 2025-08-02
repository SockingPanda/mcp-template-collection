from ..server import mcp

@mcp.tool("reverse")
def reverse(text: str) -> str:
    """Reverse a string and return the result."""
    print(f"Reversing string: {text}")
    return text[::-1]

@mcp.tool("uppercase")
def uppercase(text: str) -> str:
    """Convert a string to uppercase and return the result."""
    print(f"Converting to uppercase: {text}")
    return text.upper()

@mcp.tool("word_count")
def word_count(text: str) -> int:
    """Count the number of words in a string."""
    print(f"Counting words in: {text}")
    return len(text.split())
