"""Product catalog screen"""
from p2m.ui import Container, Column, Row, Text, Input, Button, Badge
from components.product_card import product_card


def catalog_view(store) -> Column:
    screen = Column(class_="flex flex-col min-h-screen bg-gray-50")

    # Header
    hdr = Container(class_="bg-blue-600 px-4 pt-8 pb-5")
    cart_total = sum(i["qty"] for i in store.cart)
    top = Row(class_="flex items-center justify-between mb-3")
    top.add(Text("🛍️ P2M Shop", class_="text-white text-2xl font-bold"))
    cart_badge = Button(
        f"🛒 {cart_total}",
        class_="bg-white text-blue-700 font-bold px-3 py-1 rounded-full text-sm",
        on_click="nav_cart",
    )
    top.add(cart_badge)
    hdr.add(top)
    search = Input(
        placeholder="Buscar produto...",
        value=store.search_query,
        on_change="search_products",
        class_="bg-white rounded-xl px-3 py-2 text-sm w-full",
    )
    hdr.add(search)

    # Products
    body = Column(class_="flex-1 p-4")
    query = store.search_query.lower()
    filtered = [p for p in store.products if query in p["name"].lower()] if query else store.products
    for p in filtered:
        body.add(product_card(p, store))

    if not filtered:
        empty = Column(class_="items-center justify-center py-12")
        empty.add(Text("🔍", class_="text-4xl mb-2"))
        empty.add(Text("Nenhum produto encontrado", class_="text-gray-400 text-sm"))
        body.add(empty)

    screen.add(hdr).add(body)
    return screen
