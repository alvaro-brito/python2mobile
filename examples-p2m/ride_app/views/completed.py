from p2m.ui import Column, Row, Text, Button, Card, Badge
from p2m.native import Share
from state.store import store


def completed_view():
    share_comp = Share(on_complete="handle_share")
    root = Column(class_="flex flex-col bg-neutral-950 min-h-screen")

    # ── Hero ─────────────────────────────────────────────────────────────────
    hero = Column(
        class_="flex flex-col items-center px-6 pt-16 pb-8 bg-neutral-900 border-b border-neutral-800",
    )
    hero.add(Text("✅", class_="text-6xl mb-4"))
    hero.add(Text("Trip Completed!", class_="text-white text-3xl font-black mb-1"))
    hero.add(Text(
        f"Thanks for riding, {store.user_name}!",
        class_="text-neutral-400 text-sm text-center",
    ))
    root.add(hero)

    body = Column(class_="flex flex-col px-5 py-5")

    # Trip stats
    stats = Card(class_="bg-neutral-900 rounded-2xl p-5 mb-4 border border-neutral-800")
    row = Row(class_="flex flex-row items-center justify-around")
    for label, value in [
        ("Fare",     f"R$ {store.trip_fare:.2f}"),
        ("Distance", f"{store.trip_distance:.1f} km"),
        ("Duration", f"{store.trip_duration} min"),
    ]:
        col = Column(class_="flex flex-col items-center gap-1")
        col.add(Text(value, class_="text-white font-black text-xl"))
        col.add(Text(label, class_="text-neutral-500 text-xs uppercase tracking-wide"))
        row.add(col)
    stats.add(row)
    body.add(stats)

    # Route recap
    route = Card(class_="bg-neutral-900 rounded-2xl px-5 py-4 mb-4 border border-neutral-800")
    rr = Row(class_="flex flex-row items-start gap-3")
    dots = Column(class_="flex flex-col items-center gap-1 pt-1")
    dots.add(Text("●", class_="text-green-500 text-xs"))
    dots.add(Text("│", class_="text-neutral-700 text-xs leading-none"))
    dots.add(Text("■", class_="text-red-500 text-xs"))
    addrs = Column(class_="flex flex-col flex-1 gap-2")
    addrs.add(Text(store.pickup_address, class_="text-white text-sm font-medium"))
    addrs.add(Text(store.destination_address, class_="text-neutral-400 text-sm"))
    rr.add(dots)
    rr.add(addrs)
    route.add(rr)
    body.add(route)

    # Driver recap
    drv = Card(class_="bg-neutral-900 rounded-2xl px-5 py-4 mb-5 border border-neutral-800")
    drow = Row(class_="flex flex-row items-center gap-3")
    drow.add(Text("🧑‍✈️", class_="text-4xl"))
    di = Column(class_="flex flex-col flex-1")
    di.add(Text(store.driver_name, class_="text-white font-bold text-base"))
    di.add(Text(store.driver_car, class_="text-neutral-400 text-sm"))
    drow.add(di)
    stars_drv = "★" * int(store.driver_rating)
    drow.add(Text(f"{stars_drv}  {store.driver_rating}", class_="text-amber-400 text-sm"))
    drv.add(drow)
    body.add(drv)

    # Star rating
    body.add(Text("Rate your driver", class_="text-white font-bold text-base mb-3"))
    stars_row = Row(class_="flex flex-row items-center justify-center gap-4 mb-6")
    for i in range(1, 6):
        filled = i <= store.trip_rating
        cls = "text-amber-400 text-4xl font-black" if filled else "text-neutral-700 text-4xl font-black"
        stars_row.add(Button("★", on_click="rate_driver", on_click_args=[i], class_=cls))
    body.add(stars_row)

    # Share + home
    body.add(share_comp)
    body.add(Button(
        "📤  Share Trip Receipt",
        on_click="share_receipt",
        class_="w-full bg-neutral-800 text-white font-semibold text-sm py-4 "
               "rounded-2xl mb-3 border border-neutral-700",
    ))
    body.add(Button(
        "Back to Home",
        on_click="go_home",
        class_="w-full bg-green-500 text-black font-bold text-base py-5 rounded-2xl shadow-lg",
    ))

    root.add(body)
    return root.build()
