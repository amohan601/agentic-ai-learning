# LangChain Examples

Practice notebooks and exercises from two different courses, each in its own folder:

| Folder | Course |
|--------|--------|
| [`udemy-365-ai-agent-engineer-bootcamp/`](udemy-365-ai-agent-engineer-bootcamp) | **365 Careers (Udemy)** — [The AI Agent Engineer Course — Complete AI Agent Bootcamp](https://blue.udemy.com/course/the-ai-agent-engineer-course-complete-ai-gent-bootcamp) |
| [`krishnaik-agentic-ai-3-0/`](krishnaik-agentic-ai-3-0) | **Krish Naik Academy** — LangChain 3.0 / Agentic AI 3.0 from the [Krish Naik Academy](https://www.krishnaik.in/) curriculum |

## Krish Naik Academy (Agentic AI 3.0)

Folder: `krishnaik-agentic-ai-3-0/`

| File / Folder | Description |
|------|-------------|
| `krishnaik-3-0-langchain-notes.md` | Course notes: models/messages, prompt templates, structured output, tools, `ToolRuntime`, middleware, HITL |
| `krishnaik-3-0-mcp-notes.md` | Course notes on MCP (host/client/server architecture, server types, MCP JAM, streamable HTTP) |
| `krishnaik-3-0-multi-agent-notes.md` | Short notes on multi-agent patterns (subagent, parallel, controller/router, reactive, hierarchical, planner-executor) |
| `krishnaik-3-0-1-assignment-langchain.md` | Assignment 1, Part A: written Q&A covering agents/harness, messages, structured output, and tools |
| `krishnaik-3-0-1-assignment-langchain-part-b.ipynb` | Assignment 1, Part B: my coding-exercise solutions (a `@tool`, a `ChatPromptTemplate`, a constrained-field Pydantic `FoodOrder` schema, and the Medium exercises) |
| `krishnaik-3-0-langchain-tools.ipynb` | Defining and using LangChain tools with `init_chat_model` |
| `krishnaik-3-0-langchain-structured-schema.ipynb` | Structured output with `ToolStrategy`, `ProviderStrategy`, and agent `response_format` |
| `krishnaik-3-0-langchain-agentstate-runtime.ipynb` | Agent state, context/tool runtime, dynamic prompting, human-in-the-loop with `interrupt`/`Command` |
| `krishnaik-3-0-langchain-middleware.ipynb` | Prebuilt middleware (summarization, HITL, model/tool-call limits, PII, retry, tool selector, shell) and custom middleware |
| `krishnaik-3-0-mcp-projects/` | Runnable MCP examples: `mcp-warmup`, `my-first-mcp` (recipe box), and `TimeTrackProject` (time-tracking MCP server + web app) |
| `mcp-client-and-advanced/` | Self-contained MCP *client*-side project: a full TimeTrack server plus 9 numbered client scripts covering raw `stdio_client`, FastMCP clients, an agent loop, sampling, elicitation, ping/errors, timeouts/cancellation, and progress notifications |
| `images/` | Diagrams and screenshots referenced from the notes files |

### Topics covered

**`krishnaik-3-0-langchain-notes.md`**
- Messages, `AIMessage`/`ToolMessage` fields, streaming chunks, `.batch()` vs `.batch_as_completed()`
- Prompt templates, `MessagesPlaceholder`, escaping literal `{}` in templates
- Structured output (`with_structured_output`, `model.profile`, `ToolStrategy` vs `ProviderStrategy`)
- Tools, `ToolRuntime` (`state`, `context`, `store`), `Command` returns, headless tools
- `ToolRuntime` and runtime state/context diagrams
- Middleware pipeline (`before_agent`/`before_model`/`wrap_model_call`/`wrap_tool_call`/`after_model`/`after_agent`), custom middleware
- Human-in-the-loop decision flow

**`krishnaik-3-0-mcp-notes.md`**
- MCP host/client/server architecture
- MCP server types and transports (stdio, streamable HTTP)
- Connecting local tools/servers via MCP JAM
- Using the time-tracking MCP server from Claude

**`krishnaik-3-0-multi-agent-notes.md`**
- Why hand a subtask to another agent: context isolation and reduced context overloading
- Multi-agent patterns: subagent, parallel agent, chain of agents, controller/router agent, reactive agent (evaluator + feedback loop), hierarchical agent, planner-executor agent

**`krishnaik-3-0-1-assignment-langchain.md`** (Part A)
- Agent vs. harness, the Lang product family (LangChain/LangGraph/LangSmith/Deep Agents)
- Message types, prompt templates, structured output internals
- `ToolRuntime`, `Command`, tool gating, headless tools

**`krishnaik-3-0-1-assignment-langchain-part-b.ipynb`** (Part B)
- Defining a tool with the `@tool` decorator
- A reusable `ChatPromptTemplate`
- A Pydantic schema with constrained fields (`FoodOrder`)
- Medium-level exercises building on the above

**`krishnaik-3-0-langchain-tools.ipynb`**
- LangChain 3.0 `init_chat_model` setup
- Tool definitions with Pydantic schemas and the `@tool` decorator
- Structured output alongside tool use

**`krishnaik-3-0-langchain-structured-schema.ipynb`**
- Structured output at model and agent levels (`with_structured_output`, `response_format`)
- `ToolStrategy` vs `ProviderStrategy` for structured schemas
- Union schemas, multi-format support, and validation error handling

**`krishnaik-3-0-langchain-agentstate-runtime.ipynb`**
- Agent state and how it's read/updated across a run
- Agent context vs. tool runtime
- Dynamic prompting
- Human-in-the-loop middleware with `interrupt`/`Command` (respond, edit, conditional interrupt)

**`krishnaik-3-0-langchain-middleware.ipynb`**
- Prebuilt middleware: summarization, HITL, model-call limit, model fallback, tool-call limit, PII (incl. regex checks), todo list, `LLMToolSelectorMiddleware`, `ToolErrorMiddleware`, `ToolRetryMiddleware`, `LLMToolEmulator`, `ShellToolMiddleware`
- Custom middleware, including dynamic model switching and class-based middleware

**`mcp-client-and-advanced/`**
- Building an MCP client from scratch: the raw low-level `stdio_client()` vs. FastMCP's `async with` client
- Connecting over stdio vs. to a live, deployed streamable-HTTP server
- A real agent loop built without a framework, driving MCP tool calls directly
- Advanced protocol features: sampling (server borrows the client's LLM), elicitation (server asks a mid-task question), ping/error handling, timeouts and cancellation, and progress notifications
- See [`mcp-client-and-advanced/README.md`](krishnaik-agentic-ai-3-0/mcp-client-and-advanced/README.md) for the full file layout and run order

### Running the MCP projects

Each project under `krishnaik-3-0-mcp-projects/mcp/quick-mcp/` is a [uv](https://docs.astral.sh/uv/) project. `.venv/` is not committed; `uv run` (or `uv sync`) recreates it from `pyproject.toml` and `uv.lock`.

`mcp-client-and-advanced/` is also a uv project (`uv sync`), with its own `.env` (git-ignored) for `ANTHROPIC_API_KEY` — see its own README for the numbered run order.

## 365 Careers (Udemy Bootcamp)

Folder: `udemy-365-ai-agent-engineer-bootcamp/`

| File | Description |
|------|-------------|
| `langchain_examples.ipynb` | Main notebook covering OpenAI API usage, LangChain fundamentals, and RAG |
| `langgraph_examples.ipynb` | LangGraph notebook: state graphs, conditional edges, reducers, summarization, checkpoints, and SQLite long-term memory (also published in [`amohan601/langgraph-examples`](https://github.com/amohan601/langgraph-examples)) |
| `gardening_doc.pdf` | Sample PDF used for the document loading / splitting / RAG examples |
| `gardening_docx.docx`, `gardening_doc2_md.docx` | Sample DOCX versions of the gardening doc, used for DOCX loading examples |
| `plant_care.docx` | Additional sample DOCX used for document loading and retrieval examples |
| `requirements.txt` | Python dependencies and environment setup notes |

### Topics covered

*OpenAI API*
- Chat completions (system/user messages)
- Sarcastic chatbot and sentiment classification examples
- `max_completion_tokens`, temperature, and streaming responses

*LangChain*
- `ChatOpenAI` model invocation
- Human/system messages and few-shot prompting
- Prompt templates and prompt values
- Output parsers (including comma-separated lists)
- LangChain Expression Language (LCEL): chaining, batching, streaming
- `RunnablePassThrough`, `RunnableParallel`, and `RunnableLambda`
- Chain visualization with the `grandalf` library

*Retrieval-Augmented Generation (RAG)*
- Document loading (PDF, DOCX) using the sample gardening/plant-care docs
- Text splitting (character and markdown splitters)
- Document embedding and vector stores (ChromaDB, written to `chromadb*/` next to the notebook and git-ignored)
- Document retrieval (similarity search, MMR)
- LLM response generation from retrieved context

**`langgraph_examples.ipynb`**

*LangGraph*
- Defining a state, a chatbot node, and compiling/invoking a `StateGraph`
- Conditional edges (three variants, differing in how the graph prints its conditions)
- Reducer functions to keep message history, and the built-in `MessagesState` / `add_messages`
- Removing messages with `RemoveMessage`
- Summarizing long conversations
- Persisting conversations with checkpoints (`InMemorySaver`)
- Long-term memory with SQLite (`SqliteSaver`, written to `langgraph.db` next to the notebook and git-ignored)

## Setup

1. Create and activate a conda environment (Python 3.9 recommended).
2. Add your OpenAI API key to a `.env` file (git-ignored) at the repo root or in the course folder:

```
OPENAI_API_KEY=your-key-here
```

3. Install dependencies for the course you are following:

```bash
cd udemy-365-ai-agent-engineer-bootcamp
pip install -r requirements.txt
```

   This also installs `langgraph` and `langgraph-checkpoint-sqlite` for `langgraph_examples.ipynb`.

4. Launch Jupyter from that course folder and open its notebook, so relative paths to the sample documents resolve.
