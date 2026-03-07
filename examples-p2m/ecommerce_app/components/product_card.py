"""Product card component"""
from p2m.ui import Card, Row, Column, Text, Button, Badge
from p2m.core import events


def product_card(product: dict, store) -> Card:
    pid = product["id"]

    def _add(id=pid):
        for item in store.cart:
            if item["product_id"] == id:
                item["qty"] += 1
                return
        store.cart.append({"product_id": id, "qty": 1})

    events.register(f"add_to_cart_{pid}", _add)

    card = Card(class_="bg-white rounded-2xl p-4 shadow-sm border border-gray-100 mb-3")

    top = Row(class_="flex items-center justify-between mb-3")
    top.add(Text(product["emoji"], class_="text-4xl"))
    top.add(Badge(product["cat"], class_="bg-blue-100 text-blue-700 text-xs rounded-full px-3 py-1"))

    card.add(top)
    card.add(Text(product["name"], class_="text-gray-800 font-bold text-base mb-1"))
    card.add(Text(f"R$ {product['price']:.2f}", class_="text-green-600 font-bold text-xl mb-1"))
    card.add(Text(f"Estoque: {product['stock']}", class_="text-gray-400 text-xs mb-3"))

    # Check if already in cart
    in_cart = sum(i["qty"] for i in store.cart if i["product_id"] == pid)
    btn_label = f"🛒 No carrinho ({in_cart})" if in_cart else "🛒 Adicionar"
    btn_style = "bg-green-600" if in_cart else "bg-blue-600"
    card.add(Button(
        btn_label,
        class_=f"{btn_style} text-white font-semibold py-2 px-4 rounded-xl w-full text-sm",
        on_click=f"add_to_cart_{pid}",
    ))
    return card
