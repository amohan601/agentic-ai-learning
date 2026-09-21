# LangChain Examples

Practice notebooks and exercises from two different courses:

- **365 Careers (Udemy)** — [The AI Agent Engineer Course — Complete AI Agent Bootcamp](https://blue.udemy.com/course/the-ai-agent-engineer-course-complete-ai-gent-bootcamp)
- **Krish Naik Academy** — LangChain 3.0 examples from the [Krish Naik Academy](https://www.krishnaik.in/) Agentic AI curriculum

## Krish Naik Academy (Agentic AI 3.0)

| File | Description |
|------|-------------|
| `krishnaik-3-0-langchain-notes.md` | Course notes: models/messages, prompt templates, structured output, tools, `ToolRuntime`, middleware, HITL |
| `krishnaik-3-0-mcp-notes.md` | Course notes on MCP (host/client/server architecture, server types, MCP JAM, streamable HTTP) |
| `krishnaik-3-0-1-assignment-langchain.md` | Assignment Q&A covering agents/harness, messages, structured output, and tools |
| `krishnaik-3-0-langchain-tools.ipynb` | Defining and using LangChain tools with `init_chat_model` |
| `krishnaik-3-0-langchain-structured-schema.ipynb` | Structured output with `ToolStrategy`, `ProviderStrategy`, and agent `response_format` |
| `krishnaik-3-0-langchain-agentstate-runtime.ipynb` | Agent state, context/tool runtime, dynamic prompting, human-in-the-loop with `interrupt`/`Command` |
| `krishnaik-3-0-langchain-middleware.ipynb` | Prebuilt middleware (summarization, HITL, model/tool-call limits, PII, retry, tool selector, shell) and custom middleware |
| `images/` | Diagrams referenced from the two notes files above |

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
- MCP server types
- Connecting local tools/servers via MCP JAM
- Streamable HTTP transport

**`krishnaik-3-0-1-assignment-langchain.md`**
- Agent vs. harness, the Lang product family (LangChain/LangGraph/LangSmith/Deep Agents)
- Message types, prompt templates, structured output internals
- `ToolRuntime`, `Command`, tool gating, headless tools

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

## 365 Careers (Udemy Bootcamp)

| File | Description |
|------|-------------|
| `langchain_examples.ipynb` | Main notebook covering OpenAI API usage, LangChain fundamentals, and RAG |
| `gardening_doc.pdf` | Sample PDF used for the document loading / splitting / RAG examples |
| `gardening_docx.docx`, `gardening_doc2_md.docx` | Sample DOCX versions of the gardening doc, used for DOCX loading examples |
| `plant_care.docx` | Additional sample DOCX used for document loading and retrieval examples |

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
- Document embedding and vector stores (ChromaDB)
- Document retrieval (similarity search, MMR)
- LLM response generation from retrieved context

## Shared files

| File | Description |
|------|-------------|
| `requirements.txt` | Python dependencies and environment setup notes |
| `.env` | API keys (not committed); create locally with `OPENAI_API_KEY` |

## Setup

1. Create and activate a conda environment (Python 3.9 recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add your OpenAI API key to a `.env` file:

```
OPENAI_API_KEY=your-key-here
```

4. Launch Jupyter and open the notebook for the course you are following.
