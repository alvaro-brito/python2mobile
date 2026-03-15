from p2m.core.state import AppState

store = AppState(
    # Navigation
    current_screen="splash",
    active_tab="home",

    # User profile
    user_name="",
    user_phone="",
    user_rating=4.8,

    # GPS — Av. Paulista, São Paulo
    current_lat=-23.5613,
    current_lng=-46.6558,
    location_accuracy=0.0,

    # Booking
    pickup_address="Av. Paulista, 1000 — São Paulo",
    destination_address="",
    destination_lat=-23.5475,
    destination_lng=-46.6361,

    # Ride selection
    selected_ride_type="comfort",
    fare_economy=12.90,
    fare_comfort=18.50,
    fare_premium=32.00,

    # Driver / ride status
    ride_status="",   # "" | "searching" | "driver_found" | "in_progress" | "completed"
    driver_name="",
    driver_car="",
    driver_plate="",
    driver_rating=0.0,
    driver_eta=0,
    driver_lat=-23.5590,
    driver_lng=-46.6540,

    # Trip result
    trip_duration=0,
    trip_distance=0.0,
    trip_fare=0.0,
    trip_rating=0,

    # UI
    status_message="",
    share_status="",
)
