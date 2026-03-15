"""
Veloce — Ride-hailing demo app built with Python2Mobile (P2M)

Native capabilities used:
  - Map       : interactive dark maps in home, booking, searching, and tracking screens
  - Location  : real-time GPS tracking on the home screen
  - Camera    : profile photo update in the profile tab
  - Share     : share trip receipt from the completed screen

Screens:
  splash → login → home (tabs: home / rides / profile)
         → booking → searching → tracking → completed → home

Run:    p2m run
Build:  p2m build --target flutter
        p2m build --target react-native
"""

from p2m.core import Render, events
from state.store import store
from state.data import DRIVERS_NEARBY

from views.welcome   import splash_view, login_view
from views.home      import home_view
from views.booking   import booking_view
from views.searching import searching_view
from views.tracking  import tracking_view
from views.completed import completed_view


# ── Navigation ────────────────────────────────────────────────────────────────

def go_to(screen: str):
    store.current_screen = screen
    store.status_message = ""
events.register("go_to", go_to)


def set_tab(tab: str):
    store.active_tab = tab
events.register("set_tab", set_tab)


# ── Welcome / Auth ─────────────────────────────────────────────────────────────

def set_name(value: str):
    store.user_name = value
events.register("set_name", set_name)


def set_phone(value: str):
    store.user_phone = value
events.register("set_phone", set_phone)


def login():
    if store.user_name.strip() and store.user_phone.strip():
        store.current_screen = "home"
        store.active_tab = "home"
        store.status_message = ""
events.register("login", login)


def logout():
    store.user_name = ""
    store.user_phone = ""
    store.current_screen = "splash"
events.register("logout", logout)


# ── GPS / Location ────────────────────────────────────────────────────────────

def handle_gps(lat, lng, accuracy=0.0):
    store.current_lat = round(float(lat), 6)
    store.current_lng = round(float(lng), 6)
    store.location_accuracy = round(float(accuracy), 1)
events.register("handle_gps", handle_gps)


def handle_gps_error(error: str):
    store.status_message = f"GPS error: {error}"
events.register("handle_gps_error", handle_gps_error)


# ── Driver tap on map ─────────────────────────────────────────────────────────

def handle_driver_tap(driver_id: str):
    driver = next((d for d in DRIVERS_NEARBY if d["id"] == driver_id), None)
    if driver:
        store.status_message = f"🚗  {driver['title']} · {driver['description']}"
events.register("handle_driver_tap", handle_driver_tap)


# ── Booking ───────────────────────────────────────────────────────────────────

def set_destination(address: str, lat, lng):
    store.destination_address = address
    store.destination_lat = float(lat)
    store.destination_lng = float(lng)
    store.current_screen = "booking"
events.register("set_destination", set_destination)


def clear_destination():
    store.destination_address = ""
events.register("clear_destination", clear_destination)


def set_ride_type(ride_type: str):
    store.selected_ride_type = ride_type
events.register("set_ride_type", set_ride_type)


def confirm_ride():
    if not store.destination_address:
        store.status_message = "Please select a destination first."
        return
    store.ride_status = "searching"
    store.current_screen = "searching"
events.register("confirm_ride", confirm_ride)


# ── Demo: simulate driver flow ────────────────────────────────────────────────

def simulate_driver_found():
    """Assign a mock driver — demonstrates what happens after real matching."""
    driver = DRIVERS_NEARBY[0]  # closest driver in demo
    store.driver_name   = driver["title"]   # type: ignore[index]
    store.driver_car    = driver["car"]     # type: ignore[index]
    store.driver_plate  = driver["plate"]   # type: ignore[index]
    store.driver_rating = driver["rating"]  # type: ignore[index]
    store.driver_eta    = driver["eta"]     # type: ignore[index]
    store.driver_lat    = driver["lat"]     # type: ignore[index]
    store.driver_lng    = driver["lng"]     # type: ignore[index]
    store.ride_status   = "driver_found"
    store.current_screen = "tracking"
events.register("simulate_driver_found", simulate_driver_found)


def simulate_pickup():
    """Driver has arrived at pickup — ride starts."""
    store.ride_status = "in_progress"
    store.driver_eta  = 0
    store.status_message = "🚗  Ride in progress!"
events.register("simulate_pickup", simulate_pickup)


def complete_ride():
    """Trip complete — show summary & rating screen."""
    fare_map = {
        "economy": store.fare_economy,
        "comfort":  store.fare_comfort,
        "premium":  store.fare_premium,
    }
    store.ride_status     = "completed"
    store.trip_fare       = fare_map.get(store.selected_ride_type, store.fare_comfort)
    store.trip_duration   = 14
    store.trip_distance   = 4.8
    store.current_screen  = "completed"
events.register("complete_ride", complete_ride)


def cancel_ride():
    store.ride_status        = ""
    store.driver_name        = ""
    store.driver_car         = ""
    store.driver_plate       = ""
    store.driver_rating      = 0.0
    store.driver_eta         = 0
    store.current_screen     = "home"
    store.status_message     = "Ride cancelled."
events.register("cancel_ride", cancel_ride)


# ── Driver actions (tracking screen) ─────────────────────────────────────────

def message_driver():
    store.status_message = f"💬  Message sent to {store.driver_name}."
events.register("message_driver", message_driver)


def call_driver():
    store.status_message = f"📞  Calling {store.driver_name}…"
events.register("call_driver", call_driver)


# ── Rating ────────────────────────────────────────────────────────────────────

def rate_driver(stars: int):
    store.trip_rating = stars
    store.status_message = f"Thanks! You rated {stars} ★"
events.register("rate_driver", rate_driver)


# ── Profile ───────────────────────────────────────────────────────────────────

def handle_profile_photo(uri: str, media_type: str):
    store.status_message = "Profile photo updated!"
events.register("handle_profile_photo", handle_profile_photo)


def handle_profile_error(error: str):
    store.status_message = f"Camera error: {error}"
events.register("handle_profile_error", handle_profile_error)


# ── Share ─────────────────────────────────────────────────────────────────────

_share = None  # lazy singleton — set on first share_receipt call

def share_receipt():
    global _share
    from p2m.native import Share as _Share
    if _share is None:
        _share = _Share(on_complete="handle_share")
    _share.send(
        title="My Veloce Trip Receipt",
        text=(
            f"Just completed a ride with Veloce!\n"
            f"From: {store.pickup_address}\n"
            f"To:   {store.destination_address}\n"
            f"Fare: R$ {store.trip_fare:.2f}  ·  {store.trip_duration} min"
        ),
    )
events.register("share_receipt", share_receipt)


def do_share():
    global _share
    from p2m.native import Share as _Share
    if _share is None:
        _share = _Share(on_complete="handle_share")
    _share.send(
        title="Veloce — Ride Smarter",
        text="Try Veloce, the ride app built with Python2Mobile!",
    )
events.register("do_share", do_share)


def handle_share(success: bool):
    store.share_status   = "shared" if success else "cancelled"
    store.status_message = "📤  Shared!" if success else "Share cancelled."
events.register("handle_share", handle_share)


# ── Go back to home (post-ride) ───────────────────────────────────────────────

def go_home():
    store.current_screen  = "home"
    store.active_tab      = "home"
    store.ride_status     = ""
    store.destination_address = ""
    store.trip_rating     = 0
    store.status_message  = f"Welcome back, {store.user_name}! 👋"
events.register("go_home", go_home)


# ── View router ───────────────────────────────────────────────────────────────

def create_view():
    s = store.current_screen
    if s == "splash":
        return splash_view()
    if s == "login":
        return login_view()
    if s == "home":
        return home_view()
    if s == "booking":
        return booking_view()
    if s == "searching":
        return searching_view()
    if s == "tracking":
        return tracking_view()
    if s == "completed":
        return completed_view()
    return splash_view()


def main():
    Render.execute(create_view)


if __name__ == "__main__":
    main()
