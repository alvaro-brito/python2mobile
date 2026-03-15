from p2m.ui import Row, Button
from state.store import store


def bottom_tabs():
    tabs = [
        ("home",    "🏠", "Home"),
        ("rides",   "🚗", "Rides"),
        ("profile", "👤", "Profile"),
    ]
    row = Row(class_="flex flex-row bg-neutral-950 border-t border-neutral-800")
    for tab_id, emoji, label in tabs:
        is_active = store.active_tab == tab_id
        active_cls = (
            "flex-1 py-3 text-green-500 text-xs font-bold text-center "
            "border-t-2 border-green-500"
        )
        inactive_cls = (
            "flex-1 py-3 text-neutral-500 text-xs text-center "
            "border-t-2 border-transparent"
        )
        row.add(Button(
            f"{emoji}  {label}",
            on_click="set_tab",
            on_click_args=[tab_id],
            class_=active_cls if is_active else inactive_cls,
        ))
    return row
