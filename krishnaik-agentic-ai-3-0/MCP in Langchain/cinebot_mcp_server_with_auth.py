from fastmcp import FastMCP
from mcp.types import ToolAnnotations

from fastmcp.server.auth import TokenVerifier
from mcp.server.auth.provider import AccessToken
from mcp.types import ToolAnnotations


class CineBotTokenVerifier(TokenVerifier):

    async def verify_token(self, token: str) -> AccessToken | None:
        if token != "cinebot-secret-123":
            return None

        return AccessToken(
            token=token,
            client_id="cinebot-client",
            scopes=[],
        )


auth = CineBotTokenVerifier()

mcp = FastMCP(
    "CineBot",
    auth=auth,
)


@mcp.tool()
def check_showtimes(movie_title: str) -> str:
    """Check available showtimes for a movie."""
    fake_showtimes = {
        "interstellar": "7:00 PM and 10:15 PM",
        "dune part two": "9:30 PM",
    }
    return fake_showtimes.get(movie_title.lower(), "No showtimes found.")

@mcp.tool(annotations=ToolAnnotations(destructiveHint=True, requireAuthentication=True))
def cancel_booking(booking_id: str) -> str:
    """Cancel an existing booking. Irreversible."""
    return f"Booking {booking_id} cancelled."


@mcp.tool()
def get_seat_map(movie_title: str) -> dict:
    """Get the seat map for a movie -- returns structured data, not just text."""
    return {
        "movie": movie_title,
        "available_rows": ["A", "B", "C"],
        "sold_out_rows": ["D"]
    }
if __name__ == "__main__":
    mcp.run()
