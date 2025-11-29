# usecases/uc0_hello_agent/main.py
"""
CLI entrypoint for UC0: Hello Agent.

This is a developer-facing interface for local testing only.
"""

from __future__ import annotations

import sys

from air_agent.logging_utils import get_logger, configure_root_logger
from air_agent.workflows_uc0_hello import init_conversation, add_user_and_respond

logger = get_logger(__name__)


def main() -> None:
    """
    Run an interactive CLI session for UC0.
    """
    configure_root_logger()

    logger.info("Starting UC0 Hello Agent CLI")
    history = init_conversation()

    print("=== UC-0: Hello Agent (CLI) ===")
    print("You are talking to 'Hotel Service Assistant'.")
    print("Type 'exit' or 'quit' to exit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye 👋")
            logger.info("UC0 CLI terminated by user")
            break

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye 👋")
            logger.info("UC0 CLI session ended by user command")
            break

        try:
            history = add_user_and_respond(history, user_input)
        except RuntimeError as exc:
            # We keep the message user-friendly and log the details separately.
            logger.error("UC0 CLI encountered an error: %s", exc, exc_info=exc)
            print("Assistant: Sorry, I ran into a problem talking to the AI backend.")
            print("          Please check your logs and configuration.\n")
            continue

        reply = history[-1]["content"]
        print(f"Assistant: {reply}\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # Last-resort safety net
        logger = get_logger(__name__)
        logger.exception("Fatal error in UC0 CLI: %s", exc)
        sys.exit(1)
