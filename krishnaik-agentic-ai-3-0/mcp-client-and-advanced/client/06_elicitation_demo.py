"""
06 -- ELICITATION: THE SERVER ASKS A REAL QUESTION
=====================================================
main.py's "log_time_with_confirmation" tool calls ctx.elicit(...)
whenever hours look unusually high. That call PAUSES the tool, mid-way
through, and waits for a real answer from the client. This file
provides that answer.

A NOTE WORTH KNOWING: the newest MCP protocol revision (2026-07-28) is
stateless -- it has no back-channel at all for server-initiated requests,
so ctx.elicit() raises an error on a connection negotiated at that
version. Elicitation itself isn't gone (there's a modern "return an
InputRequiredResult and get re-invoked" pattern for it), but the simple
imperative ctx.elicit() this demo relies on only works on the classic,
session-based handshake. So we pin the client to mode="legacy" below to
force that older handshake and keep this demo working as written.

SETUP:
    pip install fastmcp

RUN:
    python3 06_elicitation_demo.py
"""
import asyncio
from fastmcp import Client


async def elicitation_handler(message: str, response_type, params, context):
    """
    Called BY the server, through the client, whenever a tool calls
    ctx.elicit(). In a real app with a UI, this is where you'd show a
    real dialog box. For this demo, we print the question and auto-confirm.
    """
    print(f"\n[The server is asking]: {message}")
    print("[Auto-confirming for this demo -- swap this for real input() or a UI in your own client]")
    user_input = input("Type 'True' to confirm, False cancel: ")
    return bool(user_input)


async def main():
    async with Client(
        "../main.py", elicitation_handler=elicitation_handler, mode="legacy"
    ) as client:
        print("--- Logging 4 hours (normal -- watch: NO question gets asked) ---")
        normal_result = await client.call_tool(
            "log_time_with_confirmation",
            {"employee_name": "Asha Patel", "project": "Website Redesign",
             "entry_date": "2026-09-12", "hours": 4.0, "description": "A normal day"},
        )
        print("Result:", normal_result)

        print("\n--- Logging 14 hours (unusual -- watch: a real question appears) ---")
        high_result = await client.call_tool(
            "log_time_with_confirmation",
            {"employee_name": "Asha Patel", "project": "Website Redesign",
             "entry_date": "2026-09-12", "hours": 14.0, "description": "Crunch day"},
        )
        print("Result:", high_result)


if __name__ == "__main__":
    asyncio.run(main())
