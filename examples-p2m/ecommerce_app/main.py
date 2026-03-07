"""
Ecommerce App — Entry point
Screens: Catalog | Cart | Checkout | Confirmation
"""
from p2m.core import Render, events
from p2m.ui import Column
from state.store import store


# ------------------------------------------------------------------ #
# Handlers
# ------------------------------------------------------------------ #

def search_products(value: str):
    store.search_query = value

def nav_cart():
    store.current_screen = "cart"

def nav_catalog():
    store.current_screen = "catalog"
    store.search_query = ""

def nav_checkout():
    if store.cart:
        store.current_screen = "checkout"

def update_checkout_name(value: str):
    store.checkout_name = value

def update_checkout_email(value: str):
    store.checkout_email = value

def confirm_order():
    if store.checkout_name.strip():
        store.current_screen = "confirm"
        store.cart.clear()

events.register("search_products", search_products)
events.register("nav_cart", nav_cart)
events.register("nav_catalog", nav_catalog)
events.register("nav_checkout", nav_checkout)
events.register("update_checkout_name", update_checkout_name)
events.register("update_checkout_email", update_checkout_email)
events.register("confirm_order", confirm_order)


# ------------------------------------------------------------------ #
# View
# ------------------------------------------------------------------ #

def create_view():
    from views.catalog import catalog_view
    from views.cart import cart_view
    from views.checkout import checkout_view, confirm_view

    if store.current_screen == "catalog":
        return catalog_view(store).build()
    elif store.current_screen == "cart":
        return cart_view(store).build()
    elif store.current_screen == "checkout":
        return checkout_view(store).build()
    else:
        return confirm_view(store).build()


def main():
    Render.execute(create_view)


if __name__ == "__main__":
    main()
