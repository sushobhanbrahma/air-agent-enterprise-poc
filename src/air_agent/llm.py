# src/air_agent/llm.py
"""
LLM integration for UC0.

Responsibilities:
- Read persona + model settings from UC0 config.
- Validate that OPENAI_API_KEY is present.
- Call OpenAI Chat Completions API.
- Provide clear errors and basic logging.

UC0 is intentionally simple:
- Single provider (OpenAI).
- Single model per environment.
- No advanced routing or retries (those come in later UCs).
"""

from __future__ import annotations

import os
from typing import Dict, List, Any

from openai import OpenAI

from air_agent.config import load_uc0_config
from air_agent.logging_utils import get_logger

logger = get_logger(__name__)

_client: OpenAI | None = None


def _get_uc0_llm_config() -> Dict[str, Any]:
    """
    Read UC0-specific LLM and prompt settings from config.

    Returns:
        Dict containing model, temperature, persona.
    """
    cfg = load_uc0_config()
    llm_cfg = cfg.get("llm", {}) or {}
    prompt_cfg = cfg.get("prompt", {}) or {}

    model = llm_cfg.get("model") or os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    temperature = float(llm_cfg.get("temperature", 0.2))
    persona = prompt_cfg.get("persona", "")

    return {
        "model": model,
        "temperature": temperature,
        "persona": persona,
    }


def _get_client() -> OpenAI:
    """
    Lazily construct an OpenAI client, validating API key presence.

    Raises:
        RuntimeError: if OPENAI_API_KEY is missing.
    """
    global _client
    if _client is not None:
        return _client

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY is not set; UC0 cannot call the LLM")
        raise RuntimeError(
            "OPENAI_API_KEY environment variable is not set; "
            "cannot contact LLM provider."
        )

    logger.info("Initialising OpenAI client for UC0")
    _client = OpenAI(api_key=api_key)
    return _client


def get_system_prompt_uc0() -> str:
    """
    UC0 system prompt: Hotel Service Assistant persona.

    Loaded from the UC0 config so it can be tuned without code changes.
    """
    cfg = _get_uc0_llm_config()
    persona = cfg["persona"]
    if not persona:
        logger.warning(
            "UC0 persona is empty in config; falling back to a very basic prompt."
        )
        return (
            "You are 'Hotel Service Assistant', a polite assistant for a hotel group. "
            "Answer concisely and say you don't know if unsure."
        )
    return persona


def chat_completion_uc0(messages: List[Dict[str, str]]) -> str:
    """
    Call the configured LLM for UC0.

    Args:
        messages: Conversation history in OpenAI-style format:
                  [{"role": "system"|"user"|"assistant", "content": "..."}]

    Returns:
        Assistant's reply content as a string.

    Raises:
        RuntimeError: if the LLM call fails for any reason.
    """
    cfg = _get_uc0_llm_config()
    client = _get_client()

    logger.debug(
        "UC0 LLM call: model=%s temperature=%s history_len=%d",
        cfg["model"],
        cfg["temperature"],
        len(messages),
    )

    try:
        response = client.chat.completions.create(
            model=cfg["model"],
            temperature=cfg["temperature"],
            messages=messages,
        )
    except Exception as exc:  # Broad by design; we log details server-side.
        logger.exception("UC0 LLM call failed: %s", exc)
        raise RuntimeError("Failed to get a response from the LLM provider.") from exc

    choice = response.choices[0].message
    content = (choice.content or "").strip()
    logger.debug("UC0 LLM reply length=%d", len(content))
    return content