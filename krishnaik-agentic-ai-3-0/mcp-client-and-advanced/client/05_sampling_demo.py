"""
05 -- SUMMARIZE_WEEK: THE SERVER CALLS AN LLM DIRECTLY
=======================================================
main.py's "summarize_week" tool calls the Anthropic API itself to turn
raw timesheet rows into a friendly two-sentence summary, then returns
plain text like any other tool.

A NOTE WORTH KNOWING: MCP used to support "sampling" -- a server tool
could call ctx.sample(...) to PAUSE and ask the CONNECTED CLIENT to run
the LLM call on its behalf (the client would supply a sampling_handler
to answer it). That pattern is now deprecated in the MCP spec
(SEP-2577), and FastMCP 4.x removed Context.sample() entirely -- there
is no back-channel for it anymore. Tools are expected to call an LLM
provider directly, which is what summarize_week does now. This client
file is just a normal tool call; no sampling_handler needed.

SETUP:
    pip install fastmcp anthropic
    export ANTHROPIC_API_KEY=your-key-here   # needed by the SERVER now, not the client

RUN:
    python3 05_sampling_demo.py

A NOTE ON THE ENV VAR: the server runs as a stdio subprocess, and FastMCP's
default stdio transport only forwards a minimal safe set of environment
variables to it (PATH, HOME, etc.) -- NOT your whole shell environment. So
we build an explicit PythonStdioTransport here and pass ANTHROPIC_API_KEY
through by hand; just running Client("../main.py") would spawn the server
without the key and it would fail to authenticate with Anthropic.
"""
import asyncio
import os
from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport

from load_dotenv import load_dotenv

load_dotenv()

transport = PythonStdioTransport(
    "../main.py",
    env={"ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", "")},
)


async def main():
    async with Client(transport) as client:
        result = await client.call_tool(
            "summarize_week",
            {"employee_name": "Asha Patel", "week_start": "2026-09-08"},
        )
        print("Summary, written by the server's own LLM call:")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
