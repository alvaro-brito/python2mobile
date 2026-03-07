from p2m.ui import Column, Row, Text, Button, Card
from p2m.i18n import t


def restaurant_card(restaurant: dict):
    card = Card(class_="bg-white mx-4 mb-3 rounded-xl shadow-sm overflow-hidden")

    # Emoji banner
    banner = Row(
        class_="bg-orange-100 items-center justify-center",
        style="height:100px;"
    )
    banner.add(Text(restaurant["emoji"], class_="text-5xl"))
    card.add(banner)

    body = Column(class_="p-3")

    # Name + rating
    name_row = Row(class_="items-center justify-between mb-1")
    name_row.add(Text(restaurant["name"], class_="font-bold text-gray-800 text-base"))
    name_row.add(Text(f"⭐ {restaurant['rating']}", class_="text-sm text-gray-500"))
    body.add(name_row)

    # Delivery info
    info_row = Row(class_="items-center gap-3 mb-2")
    info_row.add(
        Text(
            f"🕒 {restaurant['delivery_time']} {t('delivery_time_suffix')}",
            class_="text-xs text-gray-500",
        )
    )
    info_row.add(
        Text(
            f"🛵 R$ {restaurant['delivery_fee']:.2f}",
            class_="text-xs text-gray-500",
        )
    )
    body.add(info_row)

    # Open modal button
    body.add(
        Button(
            t("open_modal_label"),
            class_="bg-orange-500 text-white text-sm font-semibold px-4 py-2 rounded-lg w-full",
            on_click="open_restaurant",
            on_click_args=[restaurant["id"]],
        )
    )
    card.add(body)
    return card
