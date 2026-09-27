# Building Your Own MCP Client — Complete, Numbered, Self-Contained

Every file here is complete on its own — nothing needs pasting into
another file. `main.py` already has every tool in it.

## Folder layout

```
client_project/
├── pyproject.toml    <- real uv project, run `uv sync` to install everything
├── database.py       <- persistence, shared by every tool
├── main.py            <- the COMPLETE TimeTrack server, all tools included
└── client/
    ├── 01_raw_client.py                  <- the verbose, three-layer way
    ├── 02_fastmcp_client_explained.py    <- builds up to "async with", step by step
    ├── 03_fastmcp_client_http.py         <- connects to the REAL deployed server, live on Vercel
    ├── 04_agent_loop.py                  <- a real agent, no framework
    ├── 05_sampling_demo.py               <- server borrows the client's LLM
    ├── 06_elicitation_demo.py            <- server asks a real question mid-task
    ├── 07_ping_and_errors.py             <- a real ping, a real error
    ├── 08_timeout_and_cancellation.py    <- a real timeout, triggering cancellation
    └── 09_progress_notifications.py      <- real progress updates, watched live
```

## Setup

```bash
uv sync
export ANTHROPIC_API_KEY=your-key-here   # needed for 04, 05
```

## Run order

From inside `client/`, in order:
```bash
cd client
uv run python3 01_raw_client.py                 # heads up: may hang on macOS, see below
uv run python3 02_fastmcp_client_explained.py
uv run python3 03_fastmcp_client_http.py         # needs internet -- connects to a live public server
uv run python3 04_agent_loop.py
uv run python3 05_sampling_demo.py
uv run python3 06_elicitation_demo.py
uv run python3 07_ping_and_errors.py
uv run python3 08_timeout_and_cancellation.py
uv run python3 09_progress_notifications.py
```

Every file except 03 launches `main.py` automatically as a subprocess —
you never run `python3 main.py` by hand. File 03 needs no local server
at all: it connects straight to `https://time-track-mcp-server.vercel.app/mcp`,
the real, already-deployed version of this exact server.

## A real, currently open bug — file 01 specifically

`01_raw_client.py` uses the official SDK's low-level `stdio_client()`,
which **hangs forever on macOS** (documented SDK issue #1452). If it
hangs, that's the known issue — move on to file 02.

## An honest note on sampling (file 05)

`ctx.sample()` — used inside `summarize_week` in `main.py` — triggers an
SDK deprecation warning. It still works, on the protocol version FastMCP
speaks today. It's a real transition in the ecosystem, not something broken.

## What's genuinely tested here

- `database.py`: full test suite against a real, on-disk SQLite file,
  including a genuine restart-and-recover check.
- `main.py`: every tool's exact logic — `summarize_week`,
  `log_time_with_confirmation` (all three outcomes), `slow_tool`'s
  progress sequence — tested by directly importing and executing the
  *actual shipped file*, not a rewritten copy.
- `04_agent_loop.py`: its two helper functions, same way — imported and
  executed directly from the real file.
- `02_fastmcp_client_explained.py`'s core claim — that manually calling
  `__aenter__`/`__aexit__` behaves identically to `async with`, including
  during an error — was verified with a dedicated test before writing
  the file.
- All 9 client files: confirmed to import without error.
- `03_fastmcp_client_http.py`: the URL it connects to was called for
  real before this file was written — `list_projects()` really does
  return `["Client Onboarding", "Internal Tools", "Website Redesign"]`,
  and `get_project_summary("Website Redesign")` really does return
  19.0 total hours (13.5 Asha Patel, 5.5 Rahul Mehta) — the exact same
  seed data as the local server, confirming this is genuinely the same
  TimeTrack code, live in production.
