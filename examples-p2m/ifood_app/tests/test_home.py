"""
Tests for the iFood app home view.
"""

import sys
import importlib
from pathlib import Path

import pytest

# Ensure app root is on sys.path
APP_DIR = Path(__file__).parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from p2m.testing import render_test, render_html, dispatch
from p2m.core import events


@pytest.fixture(autouse=True)
def reset():
    """Reset store + events, then re-import main to re-register handlers."""
    # Remove cached modules
    for mod_name in list(sys.modules.keys()):
        if mod_name in ("main", "state.store", "state", "views.home", "views",
                        "components.header", "components.category_carousel",
                        "components.restaurant_card", "components.restaurant_modal",
                        "components.cart_bar", "components"):
            del sys.modules[mod_name]

    events.clear()

    # Re-import fresh
    import main  # noqa: F401
    from state.store import store
    store.selected_category = "all"
    store.selected_restaurant_id = None
    store.modal_visible = False
    store.cart = []
    store.locale = "pt"

    yield

    events.clear()


def _get_main():
    return sys.modules["main"]


class TestHomeRendering:
    def test_initial_render_type(self):
        mod = _get_main()
        tree = render_test(mod.create_view)
        assert tree["type"] == "Column"

    def test_restaurants_visible_in_html(self):
        mod = _get_main()
        html = render_html(mod.create_view)
        assert "Domino" in html

    def test_all_restaurants_shown_initially(self):
        mod = _get_main()
        html = render_html(mod.create_view)
        assert "Sushi Nagoya" in html
        assert "Bob" in html

    def test_search_placeholder_present(self):
        mod = _get_main()
        html = render_html(mod.create_view)
        assert "Buscar" in html

    def test_category_buttons_present(self):
        mod = _get_main()
        html = render_html(mod.create_view)
        assert "select_category" in html

    def test_category_filter_sushi(self):
        mod = _get_main()
        dispatch("select_category", "sushi")
        html = render_html(mod.create_view)
        assert "Sushi Nagoya" in html
        assert "Domino" not in html

    def test_category_filter_pizza(self):
        mod = _get_main()
        dispatch("select_category", "pizza")
        html = render_html(mod.create_view)
        assert "Domino" in html
        assert "Bob" not in html

    def test_select_all_shows_all(self):
        mod = _get_main()
        dispatch("select_category", "sushi")
        dispatch("select_category", "all")
        html = render_html(mod.create_view)
        assert "Domino" in html
        assert "Sushi Nagoya" in html

    def test_modal_hidden_initially(self):
        mod = _get_main()
        html = render_html(mod.create_view)
        assert "display:none" in html

    def test_open_restaurant_makes_modal_visible(self):
        from state.store import store
        dispatch("open_restaurant", 1)
        assert store.modal_visible is True
        assert store.selected_restaurant_id == 1

    def test_close_modal_hides_it(self):
        from state.store import store
        dispatch("open_restaurant", 1)
        dispatch("close_modal")
        assert store.modal_visible is False
        assert store.selected_restaurant_id is None

    def test_modal_shows_menu_when_open(self):
        mod = _get_main()
        dispatch("open_restaurant", 1)
        html = render_html(mod.create_view)
        assert "Pepperoni" in html

    def test_locale_switch_changes_text(self):
        mod = _get_main()
        dispatch("switch_locale", "en")
        html = render_html(mod.create_view)
        assert "Search" in html or "Nearby" in html
