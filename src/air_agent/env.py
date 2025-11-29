# src/air_agent/env.py
"""
Environment bootstrap for Air Agent PoC.

- Loads variables from a local .env file (if present) using python-dotenv.
- Intended to be imported early by any entrypoint (CLI, API).

This keeps local developer setup easy without hardcoding secrets in code.
"""

from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv

from air_agent.logging_utils import get_logger

logger = get_logger(__name__)


def load_local_env() -> None:
    """
    Load environment variables from a .env file at the repository root.

    This function is safe to call multiple times.
    """
    repo_root = Path(__file__).resolve().parents[2]
    env_path = repo_root / ".env"

    if not env_path.exists():
        # Not an error – some environments will use system env vars instead.
        logger.info("No .env file found at %s, skipping local env load", env_path)
        return

    logger.info("Loading environment from %s", env_path)
    load_dotenv(env_path, override=False)
    logger.info("Environment variables loaded from %s", env_path)