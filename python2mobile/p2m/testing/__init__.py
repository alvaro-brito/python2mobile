"""
P2M Testing Helpers — utilities for writing in-app tests.

Usage:
    from p2m.testing import render_test, render_html, dispatch

    def test_my_view():
        tree = render_test(create_view)
        assert tree["type"] == "Column"

    def test_html():
        html = render_html(create_view)
        assert "Hello" in html

    def test_event():
        assert dispatch("my_handler")
"""

from typing import Any, Callable, Dict

from p2m.core import Render, events
from p2m.core.render_engine import RenderEngine


def render_test(create_view: Callable) -> Dict[str, Any]:
    """Execute *create_view* and return the raw component tree dict."""
    return Render.execute(create_view)


def render_html(create_view: Callable) -> str:
    """Execute *create_view* and return the rendered inner HTML string."""
    tree = Render.execute(create_view)
    return RenderEngine().render_content(tree)


def dispatch(event_name: str, *args) -> bool:
    """Dispatch a named event. Returns True if a handler was found."""
    return events.dispatch(event_name, *args)


__all__ = ["render_test", "render_html", "dispatch"]
