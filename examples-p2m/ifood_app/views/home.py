from p2m.ui import Column, Row, Text, Input, ScrollView
from p2m.i18n import t
from state.store import store, RESTAURANTS
from components.header import header
from components.category_carousel import category_carousel
from components.restaurant_card import restaurant_card
from components.restaurant_modal import restaurant_modal
from components.cart_bar import cart_bar


def home_view():
    root = Column(class_="bg-gray-50 min-h-screen")

    # Header: logo + locale switcher
    root.add(header())

    # Search bar
    search_row = Row(class_="px-4 py-3")
    search_row.add(
        Input(
            placeholder=t("search_placeholder"),
            class_="bg-white rounded-xl shadow-sm",
        )
    )
    root.add(search_row)

    # Category carousel
    root.add(category_carousel(store.selected_category))

    # Restaurants section title
    root.add(
        Text(
            t("nearby_restaurants"),
            class_="text-gray-800 font-bold text-lg px-4 pt-2 pb-1",
        )
    )

    # Restaurant list — filtered by selected_category
    for r in RESTAURANTS:
        if store.selected_category == "all" or r["category"] == store.selected_category:
            root.add(restaurant_card(r))

    # Cart bar (only shown when cart has items)
    if store.cart:
        root.add(cart_bar(store.cart))

    # Modal — always in tree; hidden when modal_visible=False
    restaurant = next(
        (r for r in RESTAURANTS if r["id"] == store.selected_restaurant_id),
        None,
    )
    root.add(restaurant_modal(restaurant, store.modal_visible))

    return root.build()
