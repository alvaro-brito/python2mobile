from p2m.ui import Row, Text, Button
from p2m.i18n import t


def cart_bar(cart: list):
    total = sum(item["price"] * item["qty"] for item in cart)
    qty = sum(item["qty"] for item in cart)

    bar = Row(
        class_="fixed bottom-0 left-0 right-0 bg-orange-500 px-4 py-3 items-center justify-between z-10",
        style="width:100%;",
    )
    bar.add(
        Text(
            f"🛒 {qty} {t('items')}  •  R$ {total:.2f}",
            class_="text-white font-bold text-sm",
        )
    )
    bar.add(
        Button(
            t("clear_cart"),
            class_="bg-white text-orange-500 text-xs font-bold px-3 py-1 rounded-full",
            on_click="clear_cart",
        )
    )
    return bar
