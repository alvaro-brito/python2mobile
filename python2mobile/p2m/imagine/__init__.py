"""
P2M Imagine — Generate complete multi-file P2M projects from natural language.

Two modes:
- Agent mode (default): uses Agno + LLM to create full project structure
- Legacy mode (--no-agent): generates a single Python file via direct LLM call
"""

import os
from typing import Optional


def agent_available(provider: str = "openai", api_key: Optional[str] = None) -> bool:
    """
    Return True when agent-based generation is possible.

    Requires:
    - `agno` installed
    - A valid API key (argument, env var, or config)
    """
    try:
        import agno  # noqa: F401
    except ImportError:
        return False

    if provider.lower() == "anthropic":
        return bool(api_key or os.environ.get("ANTHROPIC_API_KEY"))
    # openai / openai-compatible / default
    return bool(api_key or os.environ.get("OPENAI_API_KEY"))


from p2m.imagine.legacy import imagine_command  # noqa: E402
from p2m.imagine.agent import run_imagine_agent  # noqa: E402

__all__ = ["imagine_command", "run_imagine_agent", "agent_available"]
