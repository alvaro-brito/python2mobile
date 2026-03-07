"""
iFood-style demo app — P2M Food
"""

import os
from pathlib import Path

from p2m.core import Render, events
from p2m.i18n import configure, set_locale

# ── Bootstrap i18n ────────────────────────────────────────────────────────────
_APP_DIR = Path(__file__).parent
configure(str(_APP_DIR / "locales"), default_locale="pt")

# ── Lazy import after i18n is ready ───────────────────────────────────────────
from state.store import store, RESTAURANTS
from views.home import home_view


# ── Event handlers ────────────────────────────────────────────────────────────

def select_category(cat: str):
    store.selected_category = cat


def open_restaurant(restaurant_id):
    store.selected_restaurant_id = int(restaurant_id)
    store.modal_visible = True


def close_modal():
    store.modal_visible = False
    store.selected_restaurant_id = None


def add_to_cart(item_id):
    item_id = int(item_id)
    # Find item across all restaurants
    item_data = None
    for restaurant in RESTAURANTS:
        for menu_item in restaurant["menu"]:
            if menu_item["id"] == item_id:
                item_data = menu_item
                break
        if item_data:
            break

    if item_data is None:
        return

    # Increment qty if already in cart
    for cart_item in store.cart:
        if cart_item["id"] == item_id:
            cart_item["qty"] += 1
            # Trigger reactivity by reassigning cart
            store.cart = list(store.cart)
            return

    store.cart = store.cart + [{
        "id": item_id,
        "name": item_data["name"],
        "price": item_data["price"],
        "qty": 1,
        "emoji": item_data["emoji"],
    }]


def clear_cart():
    store.cart = []


def switch_locale(locale: str):
    set_locale(locale)
    store.locale = locale


# ── Register handlers ─────────────────────────────────────────────────────────
events.register("select_category", select_category)
events.register("open_restaurant", open_restaurant)
events.register("close_modal", close_modal)
events.register("add_to_cart", add_to_cart)
events.register("clear_cart", clear_cart)
events.register("switch_locale", switch_locale)


# ── View ──────────────────────────────────────────────────────────────────────
def create_view():
    return home_view()


def main():
    Render.execute(create_view)


if __name__ == "__main__":
    main()
