# ADR-0001: UC0 – Local Single-Model Chat ("Hello Agent")

- **Status**: Accepted
- **Date**: 2025-11-29
- **Owner**: Sushobhan Brahma

## 1. Context

We need a minimal but realistic starting point for an enterprise agentic
platform. Before adding RAG, tools, RBAC, or observability, we must:

- Prove that local development with `uv` works.
- Validate that we can call an LLM reliably.
- Establish the basic repository layout (UC docs, ADRs, code, runbooks).

UC0 is the simplest possible use case: a Hotel Service Assistant persona that
can chat in a multi-turn conversation via CLI and HTTP API.

## 2. Decision

- Implement a **single-model chat agent** with:
  - A static **system prompt** describing the Hotel Service Assistant persona.
  - A simple in-memory conversation history.
- Use:
  - `openai` Python client for LLM calls.
  - `fastapi` + `uvicorn` for a small HTTP API.
  - `uv` for dependency and environment management.
- Expose:
  - CLI entrypoint at `usecases/uc0_hello_agent/main.py`.
  - API at `/uc0/chat` (stateless, caller passes history).

## 3. Alternatives Considered

### 3.1 Local LLM (Ollama / vLLM) only

- **Pros**
  - No external dependency on OpenAI.
  - Better for strict data residency.
- **Cons**
  - More infra work (model download, hardware constraints).
  - Slower to get the first UC running.

**Reason not chosen for UC0:**  
For speed and simplicity of the initial PoC, we start with OpenAI via API.
Local LLM integration is planned for later ADRs.

### 3.2 Use LangChain / LangGraph from UC0

- **Pros**
  - Directly aligned with later UCs (RAG, tools, multi-agent).
- **Cons**
  - Higher initial complexity.
  - Harder to explain UC0 as a “minimal” baseline.

**Reason not chosen:**  
UC0 is intentionally "LLM only" with minimal abstraction. LangGraph will be
introduced in later UCs (RAG, tools, multi-agent).

## 4. Consequences

### 4.1 Positive

- ✅ Very simple, fast path to a working agent.
- ✅ Validates:
  - `uv` + Python environment.
  - OpenAI API integration.
  - Basic project structure and import paths.
- ✅ Provides a clean baseline to compare later UCs against.

### 4.2 Negative / Trade-offs

- ❌ Requires external OpenAI API access for UC0.
- ❌ No enterprise features:
  - No RAG, no tools, no security, no observability.
- ❌ No local LLM yet.

## 5. Implementation Notes

- Conversation history is maintained in-memory in:
  - `src/air_agent/workflows_uc0_hello.py`
- Both CLI and API use the same workflow functions.
- API is stateless: clients must pass the full history if they want multi-turn
  continuity across requests.

## 6. Future Considerations

- Replace or complement OpenAI with local LLMs (Ollama/vLLM) in a future ADR.
- Add structured logging and basic telemetry in UC1/UC4.
- Extend the same pattern (UC doc + ADR + diagrams + code + runbook) to all
  future UCs.
