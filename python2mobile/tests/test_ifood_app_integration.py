"""
Integration tests for tests-p2m/ifood_app.

Uses the same module-isolation strategy as test_new_apps_integration.py.
"""

import sys
import importlib
from pathlib import Path
import pytest

# ── Paths ─────────────────────────────────────────────────────────────────────
FRAMEWORK_PATH = Path(__file__).parent.parent          # .../python2mobile/
TESTS_P2M_PATH = FRAMEWORK_PATH.parent / "tests-p2m"  # .../tests-p2m/
IFOOD_DIR = TESTS_P2M_PATH / "ifood_app"

if str(FRAMEWORK_PATH) not in sys.path:
    sys.path.insert(0, str(FRAMEWORK_PATH))

from p2m.core import events, Render
from p2m.core.render_engine import RenderEngine


# ── Helpers ───────────────────────────────────────────────────────────────────

def _render(create_view) -> str:
    tree = Render.execute(create_view)
    return RenderEngine().render_content(tree)


def _load_app():
    sys.modules.pop("main", None)
    return importlib.import_module("main")


# ── Fixture ───────────────────────────────────────────────────────────────────

@pytest.fixture()
def ifood_app():
    saved_path = list(sys.path)
    saved_module_keys = set(sys.modules.keys())
    events.clear()

    # Reset i18n state before each test
    import p2m.i18n.translator as _t
    _t._locale = "en"
    _t._translations = {}
    _t._locales_dir = None

    sys.path.insert(0, str(IFOOD_DIR))
    mod = _load_app()
    _render(mod.create_view)   # initial render registers event handlers

    from state.store import store
    yield mod, store

    for key in list(sys.modules.keys()):
        if key not in saved_module_keys:
            del sys.modules[key]
    sys.path[:] = saved_path
    events.clear()

    # Reset i18n again after test
    _t._locale = "en"
    _t._translations = {}
    _t._locales_dir = None


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestIFoodIntegration:
    def test_initial_render(self, ifood_app):
        mod, _ = ifood_app
        tree = Render.execute(mod.create_view)
        assert tree["type"] == "Column"

    def test_restaurants_visible_in_html(self, ifood_app):
        mod, _ = ifood_app
        html = _render(mod.create_view)
        assert "Domino" in html

    def test_all_restaurants_initially(self, ifood_app):
        mod, _ = ifood_app
        html = _render(mod.create_view)
        assert "Sushi Nagoya" in html
        assert "Bob" in html
        assert "Taco Loco" in html

    def test_category_filter_sushi(self, ifood_app):
        mod, _ = ifood_app
        events.dispatch("select_category", "sushi")
        html = _render(mod.create_view)
        assert "Sushi Nagoya" in html
        assert "Domino" not in html

    def test_category_filter_pizza(self, ifood_app):
        mod, _ = ifood_app
        events.dispatch("select_category", "pizza")
        html = _render(mod.create_view)
        assert "Domino" in html
        assert "Bob" not in html

    def test_open_restaurant_sets_modal(self, ifood_app):
        _, store = ifood_app
        events.dispatch("open_restaurant", 1)
        assert store.modal_visible is True
        assert store.selected_restaurant_id == 1

    def test_close_modal(self, ifood_app):
        _, store = ifood_app
        events.dispatch("open_restaurant", 1)
        events.dispatch("close_modal")
        assert store.modal_visible is False
        assert store.selected_restaurant_id is None

    def test_modal_content_visible_when_open(self, ifood_app):
        mod, _ = ifood_app
        events.dispatch("open_restaurant", 1)
        html = _render(mod.create_view)
        assert "Pepperoni" in html

    def test_modal_hidden_initially(self, ifood_app):
        mod, _ = ifood_app
        html = _render(mod.create_view)
        assert "display:none" in html

    def test_add_to_cart(self, ifood_app):
        _, store = ifood_app
        events.dispatch("add_to_cart", 1)
        assert len(store.cart) == 1

    def test_cart_qty_increments(self, ifood_app):
        _, store = ifood_app
        events.dispatch("add_to_cart", 1)
        events.dispatch("add_to_cart", 1)
        assert len(store.cart) == 1
        assert store.cart[0]["qty"] == 2

    def test_add_different_items(self, ifood_app):
        _, store = ifood_app
        events.dispatch("add_to_cart", 1)
        events.dispatch("add_to_cart", 4)
        assert len(store.cart) == 2

    def test_clear_cart(self, ifood_app):
        _, store = ifood_app
        events.dispatch("add_to_cart", 1)
        events.dispatch("add_to_cart", 4)
        events.dispatch("clear_cart")
        assert store.cart == []

    def test_locale_switch_to_en(self, ifood_app):
        mod, _ = ifood_app
        events.dispatch("switch_locale", "en")
        html = _render(mod.create_view)
        assert "Search" in html or "Nearby" in html

    def test_locale_switch_updates_store(self, ifood_app):
        _, store = ifood_app
        events.dispatch("switch_locale", "en")
        assert store.locale == "en"

    def test_cart_bar_shown_when_items(self, ifood_app):
        mod, _ = ifood_app
        events.dispatch("add_to_cart", 1)
        html = _render(mod.create_view)
        assert "clear_cart" in html

    def test_cart_bar_hidden_when_empty(self, ifood_app):
        mod, _ = ifood_app
        html = _render(mod.create_view)
        assert "clear_cart" not in html
