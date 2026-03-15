from p2m.ui import Column, Row, Text, Button, Badge
from p2m.native import Map
from state.store import store
from state.data import DRIVERS_NEARBY


def searching_view():
    root = Column(class_="flex flex-col bg-neutral-950 min-h-screen")

    # Dark map with search circle
    root.add(Map(
        center=(store.current_lat, store.current_lng),
        zoom=14,
        map_type="dark",
        show_user_location=True,
        markers=list(DRIVERS_NEARBY),
        circles=[{
            "lat": store.current_lat,
            "lng": store.current_lng,
            "radius": 500,
            "color": "#22C55E",
            "fill_opacity": 0.06,
        }],
        class_="w-full h-52",
    ))

    # Bottom sheet
    sheet = Column(
        class_="flex flex-col bg-neutral-950 rounded-t-3xl px-6 pt-6 pb-8 flex-1 "
               "-mt-4 border-t border-neutral-800",
    )

    # Title area
    title_row = Row(class_="flex flex-row items-center gap-4 mb-5")
    title_row.add(Text("🚗", class_="text-4xl"))
    title_col = Column(class_="flex flex-col flex-1")
    title_col.add(Text("Finding your driver…", class_="text-white text-xl font-bold"))
    title_col.add(Text(
        "Matching top-rated drivers nearby",
        class_="text-neutral-500 text-sm mt-0.5",
    ))
    title_row.add(title_col)
    sheet.add(title_row)

    # Dots animation
    sheet.add(Text(
        "· · · · · · · · · ·",
        class_="text-green-500 text-lg font-black tracking-widest text-center mb-5",
    ))

    # Route info
    addr_box = Column(
        class_="bg-neutral-900 rounded-2xl px-5 py-4 mb-4 border border-neutral-800",
    )
    # From
    from_r = Row(class_="flex flex-row items-center gap-3 pb-3 border-b border-neutral-800")
    from_r.add(Text("●", class_="text-green-500 text-xs"))
    from_c = Column(class_="flex flex-col flex-1")
    from_c.add(Text("PICKUP", class_="text-neutral-500 text-xs font-semibold tracking-widest"))
    from_c.add(Text(store.pickup_address, class_="text-white text-sm font-medium mt-0.5"))
    from_r.add(from_c)
    addr_box.add(from_r)
    # To
    to_r = Row(class_="flex flex-row items-center gap-3 pt-3")
    to_r.add(Text("■", class_="text-red-500 text-xs"))
    to_c = Column(class_="flex flex-col flex-1")
    to_c.add(Text("DESTINATION", class_="text-neutral-500 text-xs font-semibold tracking-widest"))
    dest_txt = store.destination_address or "Not set"
    to_c.add(Text(dest_txt, class_="text-white text-sm font-medium mt-0.5"))
    to_r.add(to_c)
    addr_box.add(to_r)
    sheet.add(addr_box)

    sheet.add(Badge(
        label="⏱  Estimated wait: 2 – 5 min",
        class_="bg-neutral-900 text-neutral-300 text-sm px-4 py-2 rounded-full "
               "border border-neutral-700 self-center mb-5",
    ))

    # Demo controls
    sheet.add(Text(
        "── DEMO ──",
        class_="text-neutral-700 text-xs font-semibold tracking-widest text-center mb-3",
    ))
    sheet.add(Button(
        "✅  Simulate Driver Found",
        on_click="simulate_driver_found",
        class_="w-full bg-green-500 text-black font-bold text-sm py-4 rounded-2xl mb-3",
    ))
    sheet.add(Button(
        "Cancel Ride",
        on_click="cancel_ride",
        class_="w-full text-neutral-500 text-sm font-medium py-3 text-center",
    ))

    root.add(sheet)
    return root.build()
