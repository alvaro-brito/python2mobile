from p2m.ui import Column, Row, Text, Button, Badge
from p2m.native import Map
from state.store import store
from components.driver_card import driver_card


def tracking_view():
    root = Column(class_="flex flex-col bg-neutral-950 min-h-screen")

    # Dark map with full route
    drv_lat  = float(store.driver_lat)
    drv_lng  = float(store.driver_lng)
    cur_lat  = float(store.current_lat)
    cur_lng  = float(store.current_lng)
    dest_lat = float(store.destination_lat)
    dest_lng = float(store.destination_lng)
    mid_lat  = (drv_lat + dest_lat) / 2
    mid_lng  = (drv_lng + dest_lng) / 2

    markers = [
        {
            "id": "driver",
            "lat": drv_lat,
            "lng": drv_lng,
            "title": store.driver_name,
            "description": store.driver_car,
            "color": "#22C55E",
        },
        {
            "id": "pickup",
            "lat": cur_lat,
            "lng": cur_lng,
            "title": "Your pickup",
            "description": store.pickup_address,
            "color": "white",
        },
        {
            "id": "destination",
            "lat": dest_lat,
            "lng": dest_lng,
            "title": "Destination",
            "description": store.destination_address,
            "color": "red",
        },
    ]

    route_coords = [
        (drv_lat, drv_lng),
        (cur_lat, cur_lng),
        ((cur_lat + dest_lat) / 2, (cur_lng + dest_lng) / 2 + 0.004),
        (dest_lat, dest_lng),
    ]

    root.add(Map(
        center=(mid_lat, mid_lng),
        zoom=13,
        map_type="dark",
        show_user_location=True,
        markers=markers,
        routes=[{
            "coordinates": route_coords,
            "color": "#22C55E",
            "width": 5,
            "dashed": False,
        }],
        class_="w-full h-64",
    ))

    # ── Bottom sheet ──────────────────────────────────────────────────────────
    sheet = Column(
        class_="flex flex-col bg-neutral-950 rounded-t-3xl px-5 pt-5 pb-7 flex-1 "
               "-mt-4 border-t border-neutral-800",
    )

    # Route summary at top of sheet
    status_labels = {
        "driver_found":  ("Driver is on the way", "text-blue-400"),
        "in_progress":   ("Ride in progress", "text-green-400"),
    }
    label, label_cls = status_labels.get(store.ride_status, ("Processing…", "text-neutral-400"))
    sheet.add(Text(label, class_=f"{label_cls} text-sm font-semibold mb-1"))
    dest_summary = store.destination_address or "Destination"
    sheet.add(Text(
        f"Heading to: {dest_summary}",
        class_="text-white font-bold text-base mb-4",
    ))

    sheet.add(driver_card())

    # Demo controls
    sheet.add(Text(
        "── DEMO ──",
        class_="text-neutral-700 text-xs font-semibold tracking-widest text-center mt-5 mb-3",
    ))

    if store.ride_status == "driver_found":
        sheet.add(Button(
            "🚗  Simulate: Driver Arrived",
            on_click="simulate_pickup",
            class_="w-full bg-blue-600 text-white font-bold text-sm py-4 rounded-2xl mb-3",
        ))
        sheet.add(Button(
            "Cancel Ride",
            on_click="cancel_ride",
            class_="w-full text-neutral-500 text-sm font-medium py-3 text-center",
        ))

    if store.ride_status == "in_progress":
        sheet.add(Button(
            "🏁  Simulate: Trip Completed",
            on_click="complete_ride",
            class_="w-full bg-green-500 text-black font-bold text-sm py-4 rounded-2xl",
        ))

    root.add(sheet)
    return root.build()
