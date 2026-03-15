from p2m.core.state import AppState

store = AppState(
    # Camera
    photo_uri="",
    # Location
    lat=0.0,
    lng=0.0,
    location_accuracy=0.0,
    # Push
    push_token="",
    last_notification="",
    # Biometrics
    authenticated=False,
    auth_error="",
    # Bluetooth
    ble_devices=[],
    ble_connected_id="",
    ble_last_data="",
    # IAP
    is_premium=False,
    # Sensors
    accel_x=0.0,
    accel_y=0.0,
    accel_z=0.0,
    shake_count=0,
    # SecureStorage
    stored_token="",
    # Share
    share_status="",
    # Map
    map_selected_id="",
    map_tap_lat=0.0,
    map_tap_lng=0.0,
    # General
    current_screen="home",
    status_message="",
)
