from p2m.ui import Column, Row, Text, Button, Card, Badge, ScrollView
from p2m.native import Map, Camera, Share
from state.store import store
from state.data import DRIVERS_NEARBY, POPULAR_DESTINATIONS, TRIP_HISTORY
from components.bottom_tabs import bottom_tabs


def home_view():
    if store.active_tab == "rides":
        return _rides_tab()
    if store.active_tab == "profile":
        return _profile_tab()
    return _home_tab()


# ── Home tab ─────────────────────────────────────────────────────────────────

def _home_tab():
    root = Column(class_="flex flex-col bg-neutral-950 min-h-screen")

    # Dark map with nearby drivers
    map_markers = list(DRIVERS_NEARBY) + [
        {
            "id": "user",
            "lat": store.current_lat,
            "lng": store.current_lng,
            "title": "You",
            "description": store.pickup_address,
            "color": "#22C55E",
        }
    ]
    root.add(Map(
        center=(store.current_lat, store.current_lng),
        zoom=15,
        map_type="dark",
        show_user_location=True,
        markers=map_markers,
        on_marker_press="handle_driver_tap",
        class_="w-full h-72",
    ))

    # ── Bottom sheet ──────────────────────────────────────────────────────────
    sheet = Column(
        class_="flex flex-col bg-neutral-950 rounded-t-3xl px-5 pt-5 pb-0 flex-1 -mt-5 "
               "border-t border-neutral-800",
    )

    # Drag handle
    sheet.add(Row(
        class_="flex flex-row justify-center mb-4",
    ))

    # Greeting
    name = store.user_name or "there"
    greeting = Row(class_="flex flex-row items-center justify-between mb-4")
    greeting.add(Text(f"Hi, {name}! 👋", class_="text-white text-xl font-bold flex-1"))
    greeting.add(Badge(
        label="●  GPS",
        class_="bg-green-950 text-green-400 text-xs font-medium px-3 py-1.5 "
               "rounded-full border border-green-900",
    ))
    sheet.add(greeting)

    # Where to? — Uber-style pill
    sheet.add(Button(
        "🔍   Where to?",
        on_click="go_to",
        on_click_args=["booking"],
        class_="w-full bg-neutral-800 text-neutral-300 font-medium text-base py-4 "
               "rounded-2xl mb-5 text-left px-5 border border-neutral-700",
    ))

    # Popular destinations
    sheet.add(Text(
        "POPULAR",
        class_="text-neutral-500 text-xs font-semibold tracking-widest mb-3",
    ))
    for dest in POPULAR_DESTINATIONS:
        row = Row(class_="flex flex-row items-center py-3 border-b border-neutral-800")
        row.add(Text(dest["label"].split()[0], class_="text-xl mr-3 w-7 text-center"))
        col = Column(class_="flex flex-col flex-1")
        name_part = " ".join(dest["label"].split()[1:]) if len(dest["label"].split()) > 1 else dest["label"]
        col.add(Text(name_part, class_="text-white text-sm font-medium"))
        col.add(Text(dest["address"], class_="text-neutral-500 text-xs"))
        row.add(col)
        row.add(Text("›", class_="text-neutral-600 text-xl"))
        wrapper = Column(class_="relative")
        wrapper.add(Button(
            "",
            on_click="set_destination",
            on_click_args=[dest["address"], dest["lat"], dest["lng"]],
            class_="absolute inset-0 opacity-0 z-10",
        ))
        wrapper.add(row)
        sheet.add(wrapper)

    sheet.add(bottom_tabs())
    root.add(sheet)
    return root.build()


# ── Rides tab ─────────────────────────────────────────────────────────────────

def _rides_tab():
    root = Column(class_="flex flex-col bg-neutral-950 min-h-screen")

    header = Column(class_="px-5 pt-12 pb-5")
    header.add(Text("Your Trips", class_="text-white text-3xl font-black"))
    header.add(Text(
        f"{len(TRIP_HISTORY)} completed rides",
        class_="text-neutral-500 text-sm mt-1",
    ))
    root.add(header)

    scroll = ScrollView(class_="flex-1 px-4")

    for trip in TRIP_HISTORY:
        card = Card(class_="bg-neutral-900 rounded-2xl p-4 mb-3 border border-neutral-800")

        route = Row(class_="flex flex-row items-start gap-3 mb-3")
        dots = Column(class_="flex flex-col items-center gap-1 pt-1 flex-shrink-0")
        dots.add(Text("●", class_="text-green-500 text-xs"))
        dots.add(Text("│", class_="text-neutral-700 text-xs leading-none"))
        dots.add(Text("│", class_="text-neutral-700 text-xs leading-none"))
        dots.add(Text("■", class_="text-red-500 text-xs"))
        addrs = Column(class_="flex flex-col flex-1 gap-2")
        addrs.add(Text(trip["origin"], class_="text-white text-sm font-medium"))
        addrs.add(Text(trip["destination"], class_="text-neutral-400 text-sm"))
        route.add(dots)
        route.add(addrs)
        card.add(route)

        stats = Row(class_="flex flex-row items-center justify-between")
        meta = Row(class_="flex flex-row items-center gap-2")
        meta.add(Text(trip["date"], class_="text-neutral-500 text-xs"))
        meta.add(Text("·", class_="text-neutral-600"))
        meta.add(Text(trip["duration"], class_="text-neutral-500 text-xs"))
        stats.add(meta)

        right = Row(class_="flex flex-row items-center gap-2")
        type_colors = {
            "Economy": "bg-neutral-700 text-neutral-300",
            "Comfort":  "bg-blue-950 text-blue-300",
            "Premium":  "bg-amber-950 text-amber-300",
        }
        tc = type_colors.get(trip["type"], "bg-neutral-700 text-neutral-300")
        right.add(Badge(label=trip["type"], class_=f"{tc} text-xs px-2 py-0.5 rounded-full"))
        right.add(Text(f'R$ {trip["fare"]:.2f}', class_="text-white font-bold text-sm"))
        stats.add(right)
        card.add(stats)

        filled = "★" * trip["rating"]
        empty  = "☆" * (5 - trip["rating"])
        card.add(Text(f"{filled}{empty}", class_="text-amber-400 text-sm mt-2"))

        scroll.add(card)

    root.add(scroll)
    root.add(bottom_tabs())
    return root.build()


# ── Profile tab ───────────────────────────────────────────────────────────────

def _profile_tab():
    share_comp = Share(on_complete="handle_share")

    root = Column(class_="flex flex-col bg-neutral-950 min-h-screen")
    scroll = ScrollView(class_="flex-1")

    # Header
    header = Column(
        class_="flex flex-col items-center px-5 pt-12 pb-7 bg-neutral-900 border-b border-neutral-800",
    )
    header.add(Text("🧑‍💼", class_="text-7xl mb-3"))
    header.add(Text(store.user_name or "Your Name", class_="text-white text-xl font-bold"))
    header.add(Text(
        store.user_phone or "+55 (11) 99999-9999",
        class_="text-neutral-400 text-sm mt-1",
    ))
    stars = "★" * int(store.user_rating)
    header.add(Text(f"{stars}  {store.user_rating}", class_="text-amber-400 text-sm mt-2"))
    header.add(Camera(
        mode="photo",
        on_capture="handle_profile_photo",
        on_error="handle_profile_error",
    ))
    scroll.add(header)

    settings = Column(class_="flex flex-col px-5 mt-2")
    for icon, title, subtitle in [
        ("💳", "Payment Methods",   "Cards, Pix, wallets"),
        ("📍", "Saved Places",       "Home, work, favorites"),
        ("🔔", "Notifications",      "Rides, promotions, alerts"),
        ("⭐", "My Ratings",         f"You have {store.user_rating} stars"),
        ("❓", "Help & Support",     "FAQs and contact"),
    ]:
        row = Row(class_="flex flex-row items-center py-4 border-b border-neutral-800")
        row.add(Text(icon, class_="text-2xl mr-4 w-8 text-center"))
        col = Column(class_="flex flex-col flex-1")
        col.add(Text(title, class_="text-white text-sm font-medium"))
        col.add(Text(subtitle, class_="text-neutral-500 text-xs"))
        row.add(col)
        row.add(Text("›", class_="text-neutral-600 text-xl"))
        settings.add(row)

    settings.add(share_comp)
    settings.add(Button(
        "📤  Invite Friends",
        on_click="do_share",
        class_="w-full bg-green-500 text-black font-bold text-sm py-4 rounded-2xl mt-5",
    ))
    settings.add(Button(
        "Sign Out",
        on_click="logout",
        class_="w-full text-red-400 text-sm font-medium py-4 mt-2 text-center",
    ))
    scroll.add(settings)

    root.add(scroll)
    root.add(bottom_tabs())
    return root.build()
