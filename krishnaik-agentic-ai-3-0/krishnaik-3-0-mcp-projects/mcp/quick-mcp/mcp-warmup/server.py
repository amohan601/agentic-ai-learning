from fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("My Simple Server")

# Expose a simple function as a tool
@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

def main():
    print("Hello from mcp-warmup!")
    return add_numbers(2,3)


if __name__ == "__main__":
    mcp.run()
