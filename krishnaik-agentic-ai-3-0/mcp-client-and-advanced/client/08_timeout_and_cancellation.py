"""
08 -- TIMEOUT, WHICH TRIGGERS A REAL CANCELLATION
====================================================
main.py's "slow_tool" deliberately takes about 5 seconds. Here, we
connect with a much shorter timeout on purpose, so it actually times
out -- and watch what that triggers.

NOTE: "timeout" is set when you CREATE the Client, not as an argument
to call_tool() itself -- verified against FastMCP's own current
documentation.

RUN:
    python3 08_timeout_and_cancellation.py
"""
import asyncio
from fastmcp import Client


async def main():
    print("--- Connecting with a 1-second timeout, calling a ~5-second tool ---")
    async with Client("../main.py", timeout=1.0) as client:
        try:
            await client.call_tool("slow_tool", {})
        except Exception as e:
            print("Timed out and was cancelled, exactly as expected:", e)


if __name__ == "__main__":
    asyncio.run(main())
