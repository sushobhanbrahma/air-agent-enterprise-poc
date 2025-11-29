# src/air_agent/__init__.py
"""
Air Agent Enterprise PoC package.

For now:
- Loads local .env on import (for developer convenience).
- Future: global initialisation, version, etc.
"""

from .env import load_local_env as _load_local_env

# Ensure .env (if present) is loaded whenever air_agent is imported.
_load_local_env()
