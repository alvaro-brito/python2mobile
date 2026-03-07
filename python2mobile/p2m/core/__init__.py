"""
P2M Core Engine - Runtime, rendering, event dispatch, and state management
"""

from p2m.core.runtime import Render, Runtime
from p2m.core.render_engine import RenderEngine
from p2m.core.ast_walker import ASTWalker
from p2m.core import events
from p2m.core.state import AppState

__all__ = [
    "Render",
    "Runtime",
    "RenderEngine",
    "ASTWalker",
    "events",
    "AppState",
]
