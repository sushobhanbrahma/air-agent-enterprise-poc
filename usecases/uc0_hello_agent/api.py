# usecases/uc0_hello_agent/api.py
"""
FastAPI app for UC0: Hello Agent.

This is a minimal HTTP façade over the UC0 workflow:

- POST /uc0/chat
  - Request: history + latest user_input
  - Response: updated history including assistant reply

UC0 is intentionally simple:
- No auth.
- No rate limiting.
- No advanced telemetry.

Those concerns are deferred to later UCs.
"""

from __future__ import annotations

from typing import List, Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from air_agent.logging_utils import get_logger
from air_agent.workflows_uc0_hello import init_conversation, add_user_and_respond

logger = get_logger(__name__)


class Message(BaseModel):
    role: Literal["system", "user", "assistant"] = Field(
        ..., description="Role of the speaker in the conversation."
    )
    content: str = Field(..., description="Message content.")


class ChatRequest(BaseModel):
    history: List[Message] | None = Field(
        default=None,
        description=(
            "Existing conversation history. "
            "If null or empty, a new UC0 conversation is initialised."
        ),
    )
    user_input: str = Field(..., description="Latest user input to the agent.")


class ChatResponse(BaseModel):
    history: List[Message] = Field(
        ..., description="Updated conversation history including assistant reply."
    )


app = FastAPI(title="UC0 Hello Agent API", version="0.1.0")


@app.post("/uc0/chat", response_model=ChatResponse)
def chat_uc0(req: ChatRequest) -> ChatResponse:
    """
    UC0 chat endpoint.

    Returns:
        Updated conversation history with the assistant's response.

    Error handling:
    - If the LLM backend fails, returns HTTP 503 with a generic message.
    """
    if req.history is None or len(req.history) == 0:
        logger.info("UC0 API: starting new conversation")
        history = init_conversation()
    else:
        logger.info(
            "UC0 API: continuing existing conversation, history_len=%d",
            len(req.history),
        )
        history = [m.model_dump() for m in req.history]

    try:
        history = add_user_and_respond(history, req.user_input)
    except RuntimeError as exc:
        # Hide internal details from caller but log for operators.
        logger.error("UC0 API LLM failure: %s", exc, exc_info=exc)
        raise HTTPException(
            status_code=503,
            detail="UC0 backend is temporarily unavailable. Please try again later.",
        ) from exc

    messages = [Message(**m) for m in history]
    logger.info(
        "UC0 API: request processed successfully, history_len=%d", len(messages)
    )
    return ChatResponse(history=messages)
