"""
main.py -- the COMPLETE TimeTrack server used by every file in client/.

This is one file with everything already in it: the four original tools,
the resource, the prompt, and the two "advanced" tools (summarize_week and
log_time_with_confirmation) plus one deliberately slow tool for the
timeout/progress demos. You do not need to copy anything into this file --
it already has it all.

Run it on its own to sanity-check it starts:
    python3 main.py
(it will just sit there waiting for a client -- that's correct. Ctrl+C to stop.)
"""
import os
from fastmcp import FastMCP, Context
from anthropic import Anthropic
import database as db

# Make sure the database file and its table exist before anything else runs
db.init_db()

mcp = FastMCP("TimeTrack")
anthropic_client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))


# ============================================================
# THE ORIGINAL FOUR TOOLS -- unchanged from the Persistence video
# ============================================================

@mcp.tool
def log_time(employee_name: str, project: str, entry_date: str, hours: float, description: str = "") -> dict:
    """Log a time entry. entry_date must be YYYY-MM-DD."""
    return db.log_time(employee_name, project, entry_date, hours, description)


@mcp.tool
def get_timesheet(employee_name: str, start_date: str = "", end_date: str = "") -> list[dict]:
    """Get one employee's logged entries, optionally filtered to a date range (YYYY-MM-DD)."""
    return db.get_timesheet(employee_name, start_date or None, end_date or None)


@mcp.tool
def get_project_summary(project: str) -> dict:
    """Get total hours logged against a project, broken down by employee."""
    return db.get_project_summary(project)


@mcp.tool
def list_projects() -> list[str]:
    """List every project that has at least one logged time entry."""
    return db.list_projects()


@mcp.resource("timesheet://projects")
def known_projects() -> list[str]:
    """The current set of projects with logged time."""
    return db.list_projects()


@mcp.prompt
def generate_weekly_report(employee_name: str, week_start: str) -> str:
    """Guides the AI to build a structured weekly hours report."""
    return f"""Build a weekly report for {employee_name}, starting {week_start}.

1. Call get_timesheet with employee_name='{employee_name}', start_date='{week_start}'
2. Group the results by project
3. Present it as a clean report with a total

If no entries are found for that week, say so plainly instead of inventing data.
"""


# ============================================================
# NEW: a tool that generates a natural-language summary by
# calling an LLM provider directly. (MCP client-side "sampling"
# -- where the server borrows the CONNECTED CLIENT's LLM via
# ctx.sample() -- was deprecated in the MCP spec (SEP-2577) and
# FastMCP 4.x removed Context.sample() entirely. Tools now talk
# to a provider themselves instead of routing through the client.)
# ============================================================

@mcp.tool
async def summarize_week(employee_name: str, week_start: str) -> str:
    """Summarize one employee's week in plain language, using an LLM."""
    # Step 1: get the real data, same as any other tool would
    entries = db.get_timesheet(employee_name, start_date=week_start)
    if not entries:
        return f"No entries found for {employee_name} starting {week_start}."

    # Step 2: turn the raw rows into readable lines for the prompt
    entries_text = "\n".join(
        f"- {e['project']}: {e['hours']}h ({e['description']})" for e in entries
    )

    # Step 3: call the LLM provider directly to generate the text.
    response = anthropic_client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=256,
        messages=[{
            "role": "user",
            "content": f"Summarize this week's work for {employee_name} in two friendly sentences:\n\n{entries_text}",
        }],
    )
    text = "".join(block.text for block in response.content if block.type == "text")
    return text or "Could not generate a summary."


# ============================================================
# NEW: a tool that uses ELICITATION -- the server pauses and
# asks the human, through the client, before doing something
# that looks unusual.
# ============================================================

@mcp.tool
async def log_time_with_confirmation(
    employee_name: str, project: str, entry_date: str, hours: float, description: str, ctx: Context
) -> dict:
    """Log time, but pause to confirm first if the hours look unusually high."""
    # Only ask when something actually looks worth double-checking --
    # this is a deliberate choice, not every tool call should interrupt
    if hours > 10:
        # This PAUSES the tool and waits for a real answer from whoever
        # is on the other end of the connection.
        result = await ctx.elicit(
            f"{hours} hours in one day is unusually high -- log it anyway?",
            response_type=bool,
        )
        if result.action != "accept" or not result.data:
            # The user said no (or didn't answer) -- stop here, log nothing
            return {"status": "cancelled", "reason": "not confirmed by user"}
    return db.log_time(employee_name, project, entry_date, hours, description)


# ============================================================
# NEW: one deliberately slow tool, used ONLY to demonstrate
# timeouts, cancellation, and progress notifications for real.
# ============================================================

@mcp.tool
async def slow_tool(ctx: Context) -> str:
    """Takes about 5 seconds on purpose, reporting progress the whole way -- for demoing timeouts and progress."""
    import asyncio
    total_steps = 5
    for step in range(1, total_steps + 1):
        await asyncio.sleep(1)
        await ctx.report_progress(progress=step, total=total_steps, message=f"Step {step} of {total_steps}")
    return "Finished all 5 steps."


if __name__ == "__main__":
    mcp.run()
