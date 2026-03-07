from p2m.ui import Modal, Column, Row, Text, Button
from p2m.i18n import t


def restaurant_modal(restaurant, visible: bool):
    modal = Modal(
        visible=visible,
        class_="fixed inset-0 z-50 flex items-end justify-center",
        style="background-color:rgba(0,0,0,0.5);",
    )

    if not visible or not restaurant:
        return modal  # empty hidden modal — display:none applied by render engine

    sheet = Column(
        class_="bg-white rounded-t-2xl w-full",
        style="max-height:75vh;overflow-y:auto;",
    )

    # Header row: name + close button
    header_row = Row(class_="px-4 pt-4 pb-2 items-center justify-between")
    header_row.add(
        Text(
            f"{restaurant['emoji']}  {restaurant['name']}",
            class_="font-bold text-gray-800 text-lg",
        )
    )
    header_row.add(
        Button("✕", class_="text-gray-500 text-xl", on_click="close_modal")
    )
    sheet.add(header_row)

    # Info row: rating, delivery time, delivery fee
    info_row = Row(class_="px-4 pb-3 gap-4")
    info_row.add(Text(f"⭐ {restaurant['rating']}", class_="text-sm text-gray-600"))
    info_row.add(
        Text(
            f"🕒 {restaurant['delivery_time']} {t('delivery_time_suffix')}",
            class_="text-sm text-gray-600",
        )
    )
    info_row.add(
        Text(f"🛵 R$ {restaurant['delivery_fee']:.2f}", class_="text-sm text-gray-600")
    )
    sheet.add(info_row)

    # Menu title
    sheet.add(
        Text(t("menu"), class_="font-bold text-gray-800 text-base px-4 pb-2")
    )

    # Menu items
    for item in restaurant.get("menu", []):
        item_row = Row(class_="px-4 py-2 items-center justify-between border-b border-gray-100")
        left = Column(class_="")
        left.add(
            Text(
                f"{item['emoji']} {item['name']}",
                class_="text-gray-800 text-sm font-medium",
            )
        )
        left.add(
            Text(f"R$ {item['price']:.2f}", class_="text-orange-500 text-sm font-bold")
        )
        item_row.add(left)
        item_row.add(
            Button(
                t("add"),
                class_="bg-orange-500 text-white text-xs font-bold px-3 py-1 rounded-full",
                on_click="add_to_cart",
                on_click_args=[item["id"]],
            )
        )
        sheet.add(item_row)

    modal.add(sheet)
    return modal
