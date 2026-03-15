from p2m.ui import Column, Row, Text, Button, Badge
from state.store import store


def driver_card():
    """Driver info card — shown in tracking screen."""
    card = Column(class_="flex flex-col gap-3")

    # Status badge
    status_map = {
        "driver_found":  ("Driver assigned", "bg-blue-600"),
        "in_progress":   ("Ride in progress", "bg-green-600"),
    }
    label, color = status_map.get(store.ride_status, ("Searching...", "bg-neutral-600"))
    card.add(Badge(
        label=f"●  {label}",
        class_=f"{color} text-white text-xs font-semibold px-4 py-1.5 rounded-full self-start",
    ))

    # Driver row
    info = Row(class_="flex flex-row items-center gap-4")
    info.add(Text("🧑‍✈️", class_="text-5xl"))

    details = Column(class_="flex flex-col flex-1 gap-0.5")
    details.add(Text(store.driver_name, class_="text-white font-bold text-xl"))
    stars = "★" * int(store.driver_rating)
    details.add(Text(f"{stars}  {store.driver_rating}", class_="text-amber-400 text-sm"))
    details.add(Text(store.driver_car, class_="text-neutral-400 text-sm"))

    eta_col = Column(class_="flex flex-col items-center bg-neutral-800 rounded-2xl px-4 py-2")
    eta_col.add(Text(str(store.driver_eta), class_="text-white text-3xl font-black leading-none"))
    eta_col.add(Text("min", class_="text-neutral-400 text-xs"))

    info.add(details)
    info.add(eta_col)
    card.add(info)

    # Plate
    card.add(Badge(
        label=f"🚗  {store.driver_plate}",
        class_="bg-neutral-800 text-neutral-200 text-xs font-mono px-4 py-2 "
               "rounded-xl border border-neutral-700 self-start",
    ))

    # Action buttons
    actions = Row(class_="flex flex-row gap-3 mt-1")
    actions.add(Button(
        "💬  Message",
        on_click="message_driver",
        class_="flex-1 bg-neutral-800 text-white text-sm font-semibold py-3.5 "
               "rounded-2xl border border-neutral-700",
    ))
    actions.add(Button(
        "📞  Call",
        on_click="call_driver",
        class_="flex-1 bg-neutral-800 text-white text-sm font-semibold py-3.5 "
               "rounded-2xl border border-neutral-700",
    ))
    card.add(actions)

    return card
