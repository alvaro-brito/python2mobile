"""Checkout + Confirmation screens"""
from p2m.ui import Container, Column, Row, Text, Button, Input, Card


def checkout_view(store) -> Column:
    screen = Column(class_="flex flex-col min-h-screen bg-gray-50")

    hdr = Container(class_="bg-white px-4 pt-8 pb-4 border-b border-gray-200")
    top = Row(class_="flex items-center gap-3")
    top.add(Button("← Voltar", class_="text-blue-600 text-sm", on_click="nav_cart"))
    top.add(Text("Checkout", class_="text-gray-800 text-xl font-bold"))
    hdr.add(top)

    body = Column(class_="flex-1 p-4 space-y-4")

    form = Card(class_="bg-white rounded-2xl p-5 shadow-sm")
    form.add(Text("📦 Dados de entrega", class_="text-gray-700 font-bold text-base mb-4"))
    form.add(Text("Nome completo", class_="text-gray-600 text-sm font-medium mb-1"))
    form.add(Input(
        placeholder="Seu nome",
        value=store.checkout_name,
        on_change="update_checkout_name",
        class_="border border-gray-300 rounded-xl px-3 py-2 text-sm mb-3 w-full",
    ))
    form.add(Text("E-mail", class_="text-gray-600 text-sm font-medium mb-1"))
    form.add(Input(
        placeholder="seu@email.com",
        value=store.checkout_email,
        on_change="update_checkout_email",
        class_="border border-gray-300 rounded-xl px-3 py-2 text-sm w-full",
    ))

    total = sum(
        p["price"] * i["qty"]
        for i in store.cart
        for p in store.products
        if p["id"] == i["product_id"]
    )
    summary = Card(class_="bg-green-50 rounded-2xl p-4 border border-green-200")
    summary.add(Text("Resumo do pedido", class_="text-gray-700 font-semibold text-sm mb-2"))
    for item in store.cart:
        p = next((x for x in store.products if x["id"] == item["product_id"]), None)
        if p:
            r = Row(class_="flex justify-between py-1")
            r.add(Text(f"{p['emoji']} {p['name']} x{item['qty']}", class_="text-gray-600 text-xs"))
            r.add(Text(f"R$ {p['price'] * item['qty']:.2f}", class_="text-gray-700 text-xs font-semibold"))
            summary.add(r)
    summary.add(Row(class_="flex justify-between pt-2 border-t border-green-200 mt-2").add(
        Text("Total:", class_="text-gray-700 font-bold text-sm")).add(
        Text(f"R$ {total:.2f}", class_="text-green-700 font-bold text-base")))

    confirm_btn = Button(
        "✅ Confirmar Pedido",
        class_="bg-blue-600 text-white font-bold py-4 rounded-2xl w-full text-base",
        on_click="confirm_order",
    )

    body.add(form).add(summary).add(confirm_btn)
    screen.add(hdr).add(body)
    return screen


def confirm_view(store) -> Column:
    screen = Column(class_="flex flex-col items-center justify-center min-h-screen bg-white p-8")
    screen.add(Text("🎉", class_="text-7xl mb-6"))
    screen.add(Text("Pedido Confirmado!", class_="text-gray-800 text-2xl font-bold mb-2"))
    screen.add(Text(f"Obrigado, {store.checkout_name or 'Cliente'}!", class_="text-gray-500 text-base mb-8"))
    screen.add(Button(
        "🛍️ Continuar Comprando",
        class_="bg-blue-600 text-white font-bold py-3 px-8 rounded-2xl text-base",
        on_click="nav_catalog",
    ))
    return screen
