# UC00 – Hello Agent (Design)

## 1. Overview

**Goal:**  
Create a minimal “Hotel Service Assistant” chat agent that runs locally via:
- CLI
- HTTP API (`/uc0/chat`)

This is a baseline UC with:
- Single LLM
- No RAG
- No tools
- No security/observability

## 2. Actors & Channels

- **Actor:** Developer / tester on local machine
- **Channels:**
  - CLI (terminal)
  - HTTP API (FastAPI)

## 3. Functional Requirements

1. The agent must respond to user input in natural language.
2. The agent must preserve conversation context within a single session.
3. The agent must use a fixed “Hotel Service Assistant” persona.
4. The HTTP API must expose a `/uc0/chat` endpoint that:
   - Accepts a history + user input
   - Returns updated history with assistant reply

## 4. Non-Functional Requirements

- **Simplicity:** Minimal dependencies and code size.
- **Local-first:** Runs fully from developer laptop.
- **Latency:** Reasonable for human chat (< 5s per call under normal conditions).
- **Reliability:** No unhandled exceptions for normal inputs.

## 5. Out of Scope

- Policy / document grounding (RAG)
- Tools / actions (PMS, pricing, etc.)
- RBAC, auth, security controls
- Observability, logging, metrics

## 6. Success Criteria

- CLI and API both start without errors.
- Sending a message returns a coherent assistant reply.
- UC0 design + code + tests are clear enough to use as a template for UC1.

## 7. Architecture References

- ADR: [ADR-0001 – UC0 Hello Agent](../docs/adr/ADR-0001-uc0-hello-agent.md)
-  Structurizr workspace: `architecture/uc0/structurizr/workspace.dsl`
  - System Context view ID: `uc0-system-context`
  - Container view ID: `uc0-containers`
- Sequence: `../architecture/uc0/sequence/ask-flow.puml`
