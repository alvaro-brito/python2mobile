"""Cart screen"""
from p2m.ui import Container, Column, Row, Text, Button, Card, Badge
from p2m.core import events


def _register_cart_handlers(store):
    for item in store.cart:
        pid = item["product_id"]

        def _inc(id=pid):
            for i in store.cart:
                if i["product_id"] == id:
                    i["qty"] += 1

        def _dec(id=pid):
            for i in store.cart:
                if i["product_id"] == id:
                    i["qty"] -= 1
                    if i["qty"] <= 0:
                        store.cart[:] = [x for x in store.cart if x["product_id"] != id]
                    return

        events.register(f"cart_inc_{pid}", _inc)
        events.register(f"cart_dec_{pid}", _dec)


def cart_view(store) -> Column:
    _register_cart_handlers(store)
    screen = Column(class_="flex flex-col min-h-screen bg-gray-50")

    # Header
    hdr = Container(class_="bg-white px-4 pt-8 pb-4 border-b border-gray-200")
    top = Row(class_="flex items-center gap-3 mb-1")
    top.add(Button("← Voltar", class_="text-blue-600 text-sm font-medium", on_click="nav_catalog"))
    top.add(Text("🛒 Carrinho", class_="text-gray-800 text-xl font-bold flex-1"))
    hdr.add(top)

    body = Column(class_="flex-1 p-4")

    if not store.cart:
        empty = Column(class_="items-center justify-center py-16")
        empty.add(Text("🛒", class_="text-5xl mb-3"))
        empty.add(Text("Carrinho vazio", class_="text-gray-500 text-base"))
        empty.add(Button(
            "Ver produtos",
            class_="bg-blue-600 text-white px-6 py-2 rounded-xl mt-4 font-semibold text-sm",
            on_click="nav_catalog",
        ))
        body.add(empty)
    else:
        # Cart items
        for item in store.cart:
            product = next((p for p in store.products if p["id"] == item["product_id"]), None)
            if not product:
                continue
            pid = product["id"]
            card = Card(class_="bg-white rounded-2xl p-4 mb-3 shadow-sm border border-gray-100")
            row = Row(class_="flex items-center gap-3")
            row.add(Text(product["emoji"], class_="text-3xl flex-shrink-0"))
            info = Column(class_="flex-1")
            info.add(Text(product["name"], class_="text-gray-800 font-semibold text-sm"))
            info.add(Text(f"R$ {product['price']:.2f}", class_="text-green-600 font-bold text-base"))
            row.add(info)
            qty_row = Row(class_="flex items-center gap-2")
            qty_row.add(Button("-", class_="bg-gray-200 text-gray-700 font-bold w-7 h-7 rounded-full text-base", on_click=f"cart_dec_{pid}"))
            qty_row.add(Text(str(item["qty"]), class_="text-gray-800 font-bold text-base w-4 text-center"))
            qty_row.add(Button("+", class_="bg-blue-600 text-white font-bold w-7 h-7 rounded-full text-base", on_click=f"cart_inc_{pid}"))
            row.add(qty_row)
            card.add(row)
            body.add(card)

        # Total + checkout
        total = sum(
            p["price"] * i["qty"]
            for i in store.cart
            for p in store.products
            if p["id"] == i["product_id"]
        )
        summary = Card(class_="bg-white rounded-2xl p-4 shadow-sm")
        summary.add(Row(class_="flex justify-between mb-3").add(
            Text("Total:", class_="text-gray-700 font-semibold")).add(
            Text(f"R$ {total:.2f}", class_="text-green-600 font-bold text-xl")))
        summary.add(Button(
            "Finalizar Compra →",
            class_="bg-green-600 text-white font-bold py-3 w-full rounded-xl text-base",
            on_click="nav_checkout",
        ))
        body.add(summary)

    screen.add(hdr).add(body)
    return screen
