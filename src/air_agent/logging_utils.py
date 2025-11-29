# src/air_agent/logging_utils.py
"""
Logging utilities for the Air Agent PoC.

UC0 only requires minimal logging, but we still:
- Use a consistent log format.
- Avoid reconfiguring logging if the host (e.g. uvicorn) already did.
"""

from __future__ import annotations

import logging
from typing import Optional


def configure_root_logger(level: int = logging.INFO) -> None:
    """
    Configure the root logger with a sensible default format.

    This is safe to call multiple times:
    - If handlers already exist, we only adjust the level.
    - If no handlers exist, we configure basicConfig.
    """
    root = logging.getLogger()
    if not root.handlers:
        logging.basicConfig(
            level=level,
            format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        )
    else:
        root.setLevel(level)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger configured for this project.

    :param name: Module / logical name. If None, root logger is returned.
    """
    configure_root_logger()
    return logging.getLogger(name)
