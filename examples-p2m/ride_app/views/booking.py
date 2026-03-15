from p2m.ui import Column, Row, Text, Button, Card, Badge
from p2m.native import Map
from state.store import store
from state.data import RIDE_OPTIONS, POPULAR_DESTINATIONS


def booking_view():
    root = Column(class_="flex flex-col bg-neutral-950 min-h-screen")

    # ── Header ────────────────────────────────────────────────────────────────
    header = Row(
        class_="flex flex-row items-center px-4 py-3 bg-neutral-950 border-b border-neutral-800",
    )
    header.add(Button(
        "←",
        on_click="go_to",
        on_click_args=["home"],
        class_="bg-neutral-800 text-white text-lg font-bold w-10 h-10 rounded-full "
               "flex items-center justify-center mr-3",
    ))
    header.add(Text("Choose a ride", class_="text-white font-bold text-lg flex-1"))
    root.add(header)

    # ── Dark map header ────────────────────────────────────────────────────────
    cur_lat  = float(store.current_lat)
    cur_lng  = float(store.current_lng)
    dest_lat = float(store.destination_lat)
    dest_lng = float(store.destination_lng)
    mid_lat  = (cur_lat + dest_lat) / 2
    mid_lng  = (cur_lng + dest_lng) / 2

    route_markers = [
        {
            "id": "pickup",
            "lat": cur_lat,
            "lng": cur_lng,
            "title": "Pickup",
            "description": store.pickup_address,
            "color": "#22C55E",
        },
    ]
    route_lines = []

    if store.destination_address:
        route_markers.append({
            "id": "destination",
            "lat": dest_lat,
            "lng": dest_lng,
            "title": "Destination",
            "description": store.destination_address,
            "color": "red",
        })
        route_lines.append({
            "coordinates": [
                (cur_lat, cur_lng),
                (mid_lat, mid_lng + 0.005),
                (dest_lat, dest_lng),
            ],
            "color": "#22C55E",
            "width": 5,
            "dashed": False,
        })

    root.add(Map(
        center=(mid_lat, mid_lng),
        zoom=13,
        map_type="dark",
        markers=route_markers,
        routes=route_lines,
        class_="w-full h-52",
    ))

    # ── Bottom sheet ───────────────────────────────────────────────────────────
    sheet = Column(
        class_="flex flex-col bg-neutral-950 rounded-t-3xl px-5 pt-5 pb-6 flex-1 "
               "-mt-4 border-t border-neutral-800",
    )

    # From / To pill
    addr_card = Card(
        class_="bg-neutral-900 rounded-2xl px-4 py-4 mb-5 border border-neutral-700",
    )
    from_row = Row(class_="flex flex-row items-center gap-3 pb-3 border-b border-neutral-700")
    from_row.add(Text("●", class_="text-green-500 text-sm"))
    from_col = Column(class_="flex flex-col flex-1")
    from_col.add(Text("FROM", class_="text-neutral-500 text-xs font-semibold tracking-widest"))
    from_col.add(Text(store.pickup_address, class_="text-white text-sm font-medium mt-0.5"))
    from_row.add(from_col)
    addr_card.add(from_row)

    to_row = Row(class_="flex flex-row items-center gap-3 pt-3")
    to_row.add(Text("■", class_="text-red-500 text-sm"))
    to_col = Column(class_="flex flex-col flex-1")
    to_col.add(Text("TO", class_="text-neutral-500 text-xs font-semibold tracking-widest"))
    dest = store.destination_address or "Choose a destination below"
    dest_cls = "text-white text-sm font-medium mt-0.5" if store.destination_address else "text-neutral-600 text-sm mt-0.5"
    to_col.add(Text(dest, class_=dest_cls))
    to_row.add(to_col)
    if store.destination_address:
        to_row.add(Button("✕", on_click="clear_destination", class_="text-neutral-500 text-sm px-2"))
    addr_card.add(to_row)
    sheet.add(addr_card)

    # ── No destination: show popular places to pick ───────────────────────────
    if not store.destination_address:
        sheet.add(Text(
            "POPULAR DESTINATIONS",
            class_="text-neutral-500 text-xs font-semibold tracking-widest mb-3",
        ))
        for dest_item in POPULAR_DESTINATIONS:
            dest_row = Row(class_="flex flex-row items-center py-3 border-b border-neutral-800")
            dest_row.add(Text(dest_item["label"].split()[0], class_="text-xl mr-3 w-7 text-center"))
            dest_col = Column(class_="flex flex-col flex-1")
            name_part = " ".join(dest_item["label"].split()[1:]) if len(dest_item["label"].split()) > 1 else dest_item["label"]
            dest_col.add(Text(name_part, class_="text-white text-sm font-medium"))
            dest_col.add(Text(dest_item["address"], class_="text-neutral-500 text-xs"))
            dest_row.add(dest_col)
            dest_row.add(Text("›", class_="text-neutral-600 text-xl"))
            wrapper = Column(class_="relative")
            wrapper.add(Button(
                "",
                on_click="set_destination",
                on_click_args=[dest_item["address"], dest_item["lat"], dest_item["lng"]],
                class_="absolute inset-0 opacity-0 z-10",
            ))
            wrapper.add(dest_row)
            sheet.add(wrapper)

        root.add(sheet)
        return root.build()

    # ── Ride type list — Uber style ────────────────────────────────────────────
    sheet.add(Text(
        "CHOOSE A RIDE",
        class_="text-neutral-500 text-xs font-semibold tracking-widest mb-3",
    ))

    for opt in RIDE_OPTIONS:
        fare = getattr(store, opt["fare_key"])
        is_sel = store.selected_ride_type == opt["type"]

        card_cls = (
            "bg-neutral-900 border-2 border-white rounded-2xl px-4 py-4 mb-2"
            if is_sel
            else "bg-neutral-900 border border-neutral-700 rounded-2xl px-4 py-4 mb-2"
        )
        item = Card(class_=card_cls)
        row = Row(class_="flex flex-row items-center gap-4")

        car_pill = Column(class_="flex flex-col items-center justify-center bg-neutral-800 rounded-xl w-12 h-12")
        car_pill.add(Text(opt["emoji"], class_="text-2xl"))
        row.add(car_pill)

        info = Column(class_="flex flex-col flex-1")
        name_cls = "text-white font-bold text-base" if is_sel else "text-neutral-200 font-semibold text-base"
        info.add(Text(opt["name"], class_=name_cls))
        desc_row = Row(class_="flex flex-row items-center gap-1 mt-0.5")
        desc_row.add(Text(f"~{opt['eta']} min", class_="text-neutral-500 text-xs"))
        if is_sel:
            desc_row.add(Badge(
                label="⚡ Fastest",
                class_="bg-green-900 text-green-400 text-xs px-2 py-0.5 rounded-full",
            ))
        info.add(desc_row)
        row.add(info)

        fare_cls = "text-white font-black text-lg" if is_sel else "text-neutral-300 font-bold text-base"
        row.add(Text(f"R$ {fare:.2f}", class_=fare_cls))
        item.add(row)

        # Wrap card + invisible button in a relative container so the
        # absolute button only covers THIS card, not the entire screen
        wrapper = Column(class_="relative")
        wrapper.add(Button(
            "",
            on_click="set_ride_type",
            on_click_args=[opt["type"]],
            class_="absolute inset-0 opacity-0 z-10",
        ))
        wrapper.add(item)
        sheet.add(wrapper)

    # Confirm CTA
    fare_total = getattr(store, f"fare_{store.selected_ride_type}")
    confirm_cls = (
        "w-full bg-white text-black font-bold text-base py-5 rounded-2xl mt-3 shadow-lg"
        if store.destination_address
        else "w-full bg-neutral-800 text-neutral-600 font-bold text-base py-5 rounded-2xl mt-3"
    )
    sheet.add(Button(
        f"Choose {store.selected_ride_type.capitalize()}  ·  R$ {fare_total:.2f}",
        on_click="confirm_ride",
        class_=confirm_cls,
    ))

    root.add(sheet)
    return root.build()
