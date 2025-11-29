# src/air_agent/workflows_uc0_hello.py
"""
UC0: Hello Agent - Local chat with a static system prompt.

This module contains the pure Python workflow logic used by:
- CLI client (usecases/uc0_hello_agent/main.py)
- HTTP API (usecases/uc0_hello_agent/api.py)

It is deliberately simple for UC0:
- No RAG.
- No tools.
- No persistence beyond in-memory history.
"""

from __future__ import annotations

from typing import Dict, List

from air_agent.llm import get_system_prompt_uc0, chat_completion_uc0
from air_agent.logging_utils import get_logger

logger = get_logger(__name__)


def init_conversation() -> List[Dict[str, str]]:
    """
    Initialize a new UC0 conversation with the system prompt.

    Returns:
        A list with a single system message.
    """
    system_prompt = get_system_prompt_uc0()
    logger.info(
        "UC0 conversation initialised with system prompt of length=%d",
        len(system_prompt),
    )
    return [{"role": "system", "content": system_prompt}]


def add_user_and_respond(
    history: List[Dict[str, str]],
    user_input: str,
) -> List[Dict[str, str]]:
    """
    Append a user message to the conversation and generate a reply.

    Args:
        history: Existing conversation messages.
        user_input: Latest user input.

    Returns:
        Updated history, including the assistant's reply.

    Raises:
        RuntimeError: If the underlying LLM call fails.
    """
    trimmed = user_input.strip()
    if not trimmed:
        logger.info("UC0 received empty/whitespace input; ignoring.")
        return history

    logger.info(
        "UC0 conversation step: history_len_before=%d user_input_length=%d",
        len(history),
        len(trimmed),
    )

    # Avoid logging full content to reduce PII risk; only lengths.
    history.append({"role": "user", "content": trimmed})

    reply = chat_completion_uc0(history)
    history.append({"role": "assistant", "content": reply})

    logger.info(
        "UC0 conversation step complete: history_len_after=%d reply_length=%d",
        len(history),
        len(reply),
    )

    return history