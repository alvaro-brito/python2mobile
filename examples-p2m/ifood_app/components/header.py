from p2m.ui import Row, Image, Button
from p2m.i18n import t


def header():
    row = Row(class_="bg-white px-4 py-3 shadow-sm items-center justify-between")

    row.add(Image(src="assets/logo.svg", alt=t("app_name"), class_="h-8"))

    locale_row = Row(class_="gap-2")
    locale_row.add(
        Button("PT", class_="bg-orange-500 text-white text-xs px-3 py-1 rounded-full",
               on_click="switch_locale", on_click_args=["pt"])
    )
    locale_row.add(
        Button("EN", class_="bg-gray-200 text-gray-700 text-xs px-3 py-1 rounded-full",
               on_click="switch_locale", on_click_args=["en"])
    )
    row.add(locale_row)

    return row
