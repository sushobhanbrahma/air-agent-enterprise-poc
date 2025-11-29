# src/air_agent/config.py
"""
Configuration loading for the Air Agent PoC.

For UC0 we only load:
- LLM settings (provider, model, temperature)
- System prompt persona

All config is YAML-based and lives under config/.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml

from air_agent.logging_utils import get_logger

logger = get_logger(__name__)

# repo_root / src / air_agent / config.py -> repo_root
_REPO_ROOT = Path(__file__).resolve().parents[2]
_UC0_CONFIG_PATH = _REPO_ROOT / "config" / "uc0_hello_agent.yaml"

_cached_uc0_config: Dict[str, Any] | None = None


def load_uc0_config() -> Dict[str, Any]:
    """
    Load and cache the UC0 configuration.

    Raises:
        FileNotFoundError: if the UC0 config file is missing.
        ValueError: if the config file is empty or malformed.
    """
    global _cached_uc0_config

    if _cached_uc0_config is not None:
        return _cached_uc0_config

    if not _UC0_CONFIG_PATH.exists():
        logger.error("UC0 config file not found at %s", _UC0_CONFIG_PATH)
        raise FileNotFoundError(f"UC0 config not found at: {_UC0_CONFIG_PATH}")

    logger.info("Loading UC0 config from %s", _UC0_CONFIG_PATH)

    try:
        with _UC0_CONFIG_PATH.open("r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        logger.exception("Failed to parse UC0 config YAML: %s", exc)
        raise ValueError("Malformed UC0 configuration file") from exc

    if not isinstance(cfg, dict):
        logger.error("UC0 config is not a mapping object: %r", cfg)
        raise ValueError("UC0 configuration must be a mapping/object")

    _cached_uc0_config = cfg
    return _cached_uc0_config