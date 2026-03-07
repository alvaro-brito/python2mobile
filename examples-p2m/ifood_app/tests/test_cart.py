"""
Tests for the iFood app cart logic.
"""

import sys
import importlib
from pathlib import Path

import pytest

APP_DIR = Path(__file__).parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from p2m.testing import render_test, render_html, dispatch
from p2m.core import events


@pytest.fixture(autouse=True)
def reset():
    for mod_name in list(sys.modules.keys()):
        if mod_name in ("main", "state.store", "state", "views.home", "views",
                        "components.header", "components.category_carousel",
                        "components.restaurant_card", "components.restaurant_modal",
                        "components.cart_bar", "components"):
            del sys.modules[mod_name]

    events.clear()

    import main  # noqa: F401
    from state.store import store
    store.selected_category = "all"
    store.selected_restaurant_id = None
    store.modal_visible = False
    store.cart = []
    store.locale = "pt"

    yield

    events.clear()


class TestCart:
    def test_cart_empty_initially(self):
        from state.store import store
        assert store.cart == []

    def test_add_item_to_cart(self):
        from state.store import store
        dispatch("add_to_cart", 1)
        assert len(store.cart) == 1

    def test_add_item_has_correct_name(self):
        from state.store import store
        dispatch("add_to_cart", 1)
        assert store.cart[0]["name"] == "Pepperoni Grande"

    def test_add_item_has_qty_one(self):
        from state.store import store
        dispatch("add_to_cart", 1)
        assert store.cart[0]["qty"] == 1

    def test_add_same_item_increments_qty(self):
        from state.store import store
        dispatch("add_to_cart", 1)
        dispatch("add_to_cart", 1)
        assert len(store.cart) == 1
        assert store.cart[0]["qty"] == 2

    def test_add_different_items(self):
        from state.store import store
        dispatch("add_to_cart", 1)
        dispatch("add_to_cart", 4)
        assert len(store.cart) == 2

    def test_clear_cart(self):
        from state.store import store
        dispatch("add_to_cart", 1)
        dispatch("add_to_cart", 4)
        dispatch("clear_cart")
        assert store.cart == []

    def test_cart_bar_visible_when_items(self):
        mod = sys.modules["main"]
        dispatch("add_to_cart", 1)
        html = render_html(mod.create_view)
        assert "clear_cart" in html

    def test_cart_bar_hidden_when_empty(self):
        mod = sys.modules["main"]
        html = render_html(mod.create_view)
        assert "clear_cart" not in html

    def test_cart_total_calculation(self):
        from state.store import store
        dispatch("add_to_cart", 1)  # Pepperoni Grande 42.90
        dispatch("add_to_cart", 1)  # qty=2 → 85.80
        total = sum(i["price"] * i["qty"] for i in store.cart)
        assert abs(total - 85.80) < 0.01

    def test_add_item_from_different_restaurant(self):
        from state.store import store
        dispatch("add_to_cart", 4)  # Combo 30 peças from Sushi Nagoya
        assert len(store.cart) == 1
        assert store.cart[0]["name"] == "Combo 30 peças"
