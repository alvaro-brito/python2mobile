"""
P2M Native Capabilities Demo App

Demonstrates how to use all 9 native device capabilities in a P2M app.
Run with: p2m run
Build with: p2m build --target flutter
            p2m build --target react-native
"""

from p2m.core import Render, events
from p2m.ui import Column, Row, Text, Button, Card, Badge, ScrollView
from p2m.native import (
    Camera, Location, PushNotifications, Biometrics,
    Bluetooth, InAppPurchase, Sensors, SecureStorage, Share, Map,
)
from state.store import store


# ── Secure Storage & Share (service components — declared once) ────────────

secure = SecureStorage(
    on_read="handle_secret_loaded",
    on_write="handle_secret_saved",
)

share = Share(on_complete="handle_shared")


# ── Event Handlers ─────────────────────────────────────────────────────────

# Camera
def handle_photo(uri: str, type: str):
    store.photo_uri = uri
    store.status_message = f"📷 Captured {type}: {uri.split('/')[-1]}"
events.register("handle_photo", handle_photo)

def handle_cam_error(error: str):
    store.status_message = f"Camera error: {error}"
events.register("handle_cam_error", handle_cam_error)

# Location
def handle_location(lat: float, lng: float, accuracy: float):
    store.lat = round(lat, 4)
    store.lng = round(lng, 4)
    store.location_accuracy = round(accuracy, 1)
    store.status_message = f"📍 Location: {store.lat}, {store.lng}"
events.register("handle_location", handle_location)

def handle_loc_error(error: str):
    store.status_message = f"Location error: {error}"
events.register("handle_loc_error", handle_loc_error)

# Push Notifications
def handle_push_token(token: str):
    store.push_token = token[:20] + "…"
    store.status_message = "🔔 Push registered!"
events.register("handle_push_token", handle_push_token)

def handle_notification(title: str, body: str, data: str):
    store.last_notification = f"{title}: {body}"
    store.status_message = f"🔔 Notification: {title}"
events.register("handle_notification", handle_notification)

def handle_push_error(error: str):
    store.status_message = f"Push error: {error}"
events.register("handle_push_error", handle_push_error)

# Biometrics
def handle_auth_success():
    store.authenticated = True
    store.auth_error = ""
    store.status_message = "🔐 Authentication successful!"
events.register("handle_auth_success", handle_auth_success)

def handle_auth_failure(error: str):
    store.authenticated = False
    store.auth_error = error
    store.status_message = f"Auth failed: {error}"
events.register("handle_auth_failure", handle_auth_failure)

# Bluetooth
def handle_device_found(name: str, id: str, rssi: int):
    device = {"name": name, "id": id, "rssi": rssi}
    store.ble_devices = [d for d in store.ble_devices if d["id"] != id]
    store.ble_devices.append(device)
    store.status_message = f"🔵 Found: {name}"
events.register("handle_device_found", handle_device_found)

def handle_ble_connect(device_id: str):
    store.ble_connected_id = device_id
    store.status_message = f"🔗 Connected: {device_id}"
events.register("handle_ble_connect", handle_ble_connect)

def handle_ble_data(device_id: str, characteristic: str, value: str):
    store.ble_last_data = f"{characteristic}: {value}"
    store.status_message = f"📩 Data from {device_id}"
events.register("handle_ble_data", handle_ble_data)

def handle_ble_error(error: str):
    store.status_message = f"BLE error: {error}"
events.register("handle_ble_error", handle_ble_error)

# In-App Purchase
def handle_purchase(product_id: str, transaction_id: str):
    store.is_premium = True
    store.status_message = f"💳 Purchased: {product_id}"
events.register("handle_purchase", handle_purchase)

def handle_iap_error(error: str):
    store.status_message = f"IAP error: {error}"
events.register("handle_iap_error", handle_iap_error)

# Sensors
def handle_accel(x: float, y: float, z: float):
    store.accel_x = round(x, 2)
    store.accel_y = round(y, 2)
    store.accel_z = round(z, 2)
    if abs(x) > 15 or abs(y) > 15:
        store.shake_count += 1
        store.status_message = f"📳 Shake #{store.shake_count}!"
events.register("handle_accel", handle_accel)

# Secure Storage
def save_token():
    secure.write("auth_token", "my-super-secret-token-12345")
events.register("save_token", save_token)

def load_token():
    secure.read("auth_token")
events.register("load_token", load_token)

def handle_secret_loaded(key: str, value: str):
    store.stored_token = value or "(empty)"
    store.status_message = f"🔑 Loaded: {key}"
events.register("handle_secret_loaded", handle_secret_loaded)

def handle_secret_saved(key: str, success: bool):
    store.status_message = f"💾 Saved {key}: {'OK' if success else 'FAIL'}"
events.register("handle_secret_saved", handle_secret_saved)

# Share
def do_share():
    share.send(
        title="Check out P2M!",
        text=f"I built this app with Python2Mobile. Location: {store.lat}, {store.lng}",
        url="https://github.com/python2mobile",
    )
events.register("do_share", do_share)

def handle_shared(success: bool):
    store.share_status = "shared" if success else "cancelled"
    store.status_message = "📤 Shared!" if success else "Share cancelled"
events.register("handle_shared", handle_shared)

# Navigation
def go_to(screen: str):
    store.current_screen = screen
events.register("go_to", go_to)

# Map
def handle_pin(marker_id: str):
    store.map_selected_id = marker_id
    store.status_message = f"Pin tapped: {marker_id}"
events.register("handle_pin", handle_pin)

def handle_map_tap(lat: float, lng: float):
    store.map_tap_lat = round(lat, 4)
    store.map_tap_lng = round(lng, 4)
    store.status_message = f"Map tap: {store.map_tap_lat}, {store.map_tap_lng}"
events.register("handle_map_tap", handle_map_tap)


# ── View ───────────────────────────────────────────────────────────────────

def create_view():
    if store.current_screen == "home":
        return home_view()
    elif store.current_screen == "location":
        return location_view()
    elif store.current_screen == "ble":
        return bluetooth_view()
    elif store.current_screen == "sensors":
        return sensors_view()
    elif store.current_screen == "map":
        return map_view()
    return home_view()


def _status_bar():
    """Shared status bar shown at the top of all screens."""
    bar = Row(class_="flex flex-row items-center px-4 py-2 bg-indigo-600")
    bar.add(Text(store.status_message or "Ready", class_="text-white text-xs flex-1 truncate"))
    return bar


def home_view():
    root = Column(class_="flex flex-col bg-gray-50 min-h-screen")
    root.add(_status_bar())

    header = Column(class_="flex flex-col items-center py-5 bg-indigo-600")
    header.add(Text("P2M Native Demo", class_="text-white text-2xl font-bold"))
    header.add(Text("All 9 native capabilities", class_="text-indigo-200 text-sm"))
    root.add(header)

    scroll = ScrollView(class_="flex-1 p-4")

    # Camera section
    cam_card = Card(class_="bg-white rounded-2xl shadow p-4 mb-4")
    cam_card.add(Text("📷 Camera", class_="text-gray-800 font-semibold text-base mb-3"))
    cam_card.add(Camera(
        mode="both",
        on_capture="handle_photo",
        on_error="handle_cam_error",
    ))
    if store.photo_uri:
        cam_card.add(Text(f"Last: {store.photo_uri.split('/')[-1]}", class_="text-gray-500 text-xs mt-2"))
    scroll.add(cam_card)

    # Push Notifications section
    push_card = Card(class_="bg-white rounded-2xl shadow p-4 mb-4")
    push_card.add(Text("🔔 Push Notifications", class_="text-gray-800 font-semibold text-base mb-3"))
    push_card.add(PushNotifications(
        on_register="handle_push_token",
        on_message="handle_notification",
        on_error="handle_push_error",
    ))
    if store.push_token:
        push_card.add(Text(f"Token: {store.push_token}", class_="text-gray-500 text-xs mt-2"))
    if store.last_notification:
        push_card.add(Text(store.last_notification, class_="text-indigo-600 text-xs"))
    scroll.add(push_card)

    # Biometrics section
    bio_card = Card(class_="bg-white rounded-2xl shadow p-4 mb-4")
    bio_card.add(Text("🔐 Biometrics", class_="text-gray-800 font-semibold text-base mb-3"))
    bio_card.add(Biometrics(
        prompt="Confirme sua identidade para continuar",
        fallback_label="Usar Senha",
        on_success="handle_auth_success",
        on_failure="handle_auth_failure",
    ))
    status_text = "✅ Authenticated" if store.authenticated else (store.auth_error or "Not authenticated")
    status_class = "text-green-600 text-xs mt-2" if store.authenticated else "text-red-500 text-xs mt-2"
    bio_card.add(Text(status_text, class_=status_class))
    scroll.add(bio_card)

    # IAP section
    iap_card = Card(class_="bg-white rounded-2xl shadow p-4 mb-4")
    iap_card.add(Text("💳 In-App Purchase", class_="text-gray-800 font-semibold text-base mb-3"))
    if not store.is_premium:
        iap_card.add(InAppPurchase(
            product_id="com.nativedemo.premium",
            product_type="non_consumable",
            on_purchased="handle_purchase",
            on_error="handle_iap_error",
        ))
    else:
        iap_card.add(Badge(label="✅ Premium Active", class_="bg-green-100 text-green-700 text-sm px-3 py-1 rounded-full"))
    scroll.add(iap_card)

    # Secure Storage section
    sec_card = Card(class_="bg-white rounded-2xl shadow p-4 mb-4")
    sec_card.add(Text("🔑 Secure Storage", class_="text-gray-800 font-semibold text-base mb-3"))
    sec_card.add(secure)
    sec_row = Row(class_="flex flex-row gap-2 mt-2")
    sec_row.add(Button("Save Token", on_click="save_token", class_="flex-1 bg-indigo-600 text-white text-xs py-2 rounded-lg"))
    sec_row.add(Button("Load Token", on_click="load_token", class_="flex-1 bg-gray-100 text-gray-700 text-xs py-2 rounded-lg"))
    sec_card.add(sec_row)
    if store.stored_token:
        sec_card.add(Text(f"Value: {store.stored_token[:30]}…", class_="text-gray-500 text-xs mt-1"))
    scroll.add(sec_card)

    # Share section
    share_card = Card(class_="bg-white rounded-2xl shadow p-4 mb-4")
    share_card.add(Text("📤 Share", class_="text-gray-800 font-semibold text-base mb-3"))
    share_card.add(share)
    share_card.add(Button(
        "📤 Share App Info",
        on_click="do_share",
        class_="w-full bg-indigo-600 text-white text-sm font-semibold py-3 rounded-xl mt-2",
    ))
    scroll.add(share_card)

    # Navigation to other screens
    nav_row = Row(class_="flex flex-row gap-2 mt-2 mb-1")
    nav_row.add(Button("📍 Location", on_click="go_to", on_click_args=["location"],
                       class_="flex-1 bg-white border border-indigo-200 text-indigo-600 text-xs py-2 rounded-lg shadow-sm"))
    nav_row.add(Button("🔵 Bluetooth", on_click="go_to", on_click_args=["ble"],
                       class_="flex-1 bg-white border border-indigo-200 text-indigo-600 text-xs py-2 rounded-lg shadow-sm"))
    nav_row.add(Button("📱 Sensors", on_click="go_to", on_click_args=["sensors"],
                       class_="flex-1 bg-white border border-indigo-200 text-indigo-600 text-xs py-2 rounded-lg shadow-sm"))
    scroll.add(nav_row)
    nav_row2 = Row(class_="flex flex-row gap-2 mb-4")
    nav_row2.add(Button("🗺️ Map", on_click="go_to", on_click_args=["map"],
                        class_="flex-1 bg-white border border-indigo-200 text-indigo-600 text-xs py-2 rounded-lg shadow-sm"))
    scroll.add(nav_row2)

    root.add(scroll)
    return root.build()


def location_view():
    root = Column(class_="flex flex-col bg-gray-50 min-h-screen")
    root.add(_status_bar())

    header = Row(class_="flex flex-row items-center px-4 py-3 bg-white border-b border-gray-100")
    header.add(Button("← Back", on_click="go_to", on_click_args=["home"],
                      class_="text-indigo-600 text-sm font-medium"))
    header.add(Text("📍 Location", class_="text-gray-800 font-semibold flex-1 text-center"))
    root.add(header)

    card = Card(class_="bg-white rounded-2xl shadow m-4 p-4")
    card.add(Location(
        watch=False,
        accuracy="high",
        on_update="handle_location",
        on_error="handle_loc_error",
    ))
    if store.lat != 0.0 or store.lng != 0.0:
        coords = Column(class_="flex flex-col gap-1 mt-3 p-3 bg-gray-50 rounded-xl")
        coords.add(Text(f"Latitude:  {store.lat}", class_="font-medium text-sm text-gray-700"))
        coords.add(Text(f"Longitude: {store.lng}", class_="text-sm text-gray-700"))
        coords.add(Text(f"Accuracy:  ±{store.location_accuracy}m", class_="text-xs text-gray-500"))
        card.add(coords)
    root.add(card)

    return root.build()


def bluetooth_view():
    root = Column(class_="flex flex-col bg-gray-50 min-h-screen")
    root.add(_status_bar())

    header = Row(class_="flex flex-row items-center px-4 py-3 bg-white border-b border-gray-100")
    header.add(Button("← Back", on_click="go_to", on_click_args=["home"],
                      class_="text-indigo-600 text-sm font-medium"))
    header.add(Text("🔵 Bluetooth BLE", class_="text-gray-800 font-semibold flex-1 text-center"))
    root.add(header)

    card = Card(class_="bg-white rounded-2xl shadow m-4 p-4")
    card.add(Bluetooth(
        service_uuid="FFE0",
        on_scan_result="handle_device_found",
        on_connect="handle_ble_connect",
        on_data="handle_ble_data",
        on_error="handle_ble_error",
    ))

    if store.ble_devices:
        card.add(Text(f"Devices ({len(store.ble_devices)})", class_="text-gray-600 text-sm font-medium mt-3 mb-1"))
        for d in store.ble_devices[-5:]:  # show last 5
            dev_row = Row(class_="flex flex-row items-center py-2 border-b border-gray-50")
            dev_row.add(Text(d["name"], class_="flex-1 text-sm text-gray-800"))
            dev_row.add(Badge(label=f'{d["rssi"]} dBm',
                              class_="text-xs text-gray-500 bg-gray-100 px-2 py-0 rounded"))
            card.add(dev_row)

    if store.ble_last_data:
        card.add(Text(f"Last data: {store.ble_last_data}", class_="text-indigo-600 text-xs mt-2"))

    root.add(card)
    return root.build()


def sensors_view():
    root = Column(class_="flex flex-col bg-gray-50 min-h-screen")
    root.add(_status_bar())

    header = Row(class_="flex flex-row items-center px-4 py-3 bg-white border-b border-gray-100")
    header.add(Button("← Back", on_click="go_to", on_click_args=["home"],
                      class_="text-indigo-600 text-sm font-medium"))
    header.add(Text("📱 Sensors", class_="text-gray-800 font-semibold flex-1 text-center"))
    root.add(header)

    card = Card(class_="bg-white rounded-2xl shadow m-4 p-4")
    card.add(Sensors(
        sensor_type="accelerometer",
        interval=200,
        on_update="handle_accel",
    ))

    data_grid = Column(class_="flex flex-col gap-2 mt-3")
    for label, val in [("X", store.accel_x), ("Y", store.accel_y), ("Z", store.accel_z)]:
        row = Row(class_="flex flex-row items-center py-2 border-b border-gray-50")
        row.add(Text(f"Accel {label}", class_="flex-1 text-sm text-gray-600"))
        row.add(Text(f"{val:.2f} m/s²", class_="text-sm font-semibold text-indigo-600"))
        data_grid.add(row)
    data_grid.add(Text(f"Shakes: {store.shake_count}", class_="text-indigo-700 font-bold text-lg mt-2"))
    card.add(data_grid)

    root.add(card)
    return root.build()


def map_view():
    root = Column(class_="flex flex-col bg-gray-50 min-h-screen")
    root.add(_status_bar())

    header = Row(class_="flex flex-row items-center px-4 py-3 bg-white border-b border-gray-100")
    header.add(Button("← Back", on_click="go_to", on_click_args=["home"],
                      class_="text-indigo-600 text-sm font-medium"))
    header.add(Text("🗺️ Map", class_="text-gray-800 font-semibold flex-1 text-center"))
    root.add(header)

    # Info bar — selected pin or last tap
    info = Row(class_="flex flex-row items-center px-4 py-2 bg-indigo-50 border-b border-indigo-100")
    if store.map_selected_id:
        info.add(Text(f"📍 Pin: {store.map_selected_id}", class_="text-indigo-700 text-xs font-medium flex-1"))
    elif store.map_tap_lat != 0.0:
        info.add(Text(
            f"Tap: {store.map_tap_lat}, {store.map_tap_lng}",
            class_="text-indigo-700 text-xs flex-1",
        ))
    else:
        info.add(Text("Tap the map or press a pin", class_="text-gray-400 text-xs flex-1"))
    root.add(info)

    # Interactive Leaflet map — São Paulo demo
    map_component = Map(
        center=(-23.5505, -46.6333),
        zoom=14,
        map_type="standard",
        show_user_location=True,
        markers=[
            {
                "id": "ibirapuera",
                "lat": -23.5874,
                "lng": -46.6576,
                "title": "Ibirapuera Park",
                "description": "Largest urban park in SP",
                "color": "green",
            },
            {
                "id": "paulista",
                "lat": -23.5613,
                "lng": -46.6558,
                "title": "Av. Paulista",
                "description": "Financial & cultural hub",
                "color": "blue",
            },
            {
                "id": "se",
                "lat": -23.5475,
                "lng": -46.6361,
                "title": "Sé Cathedral",
                "description": "Historic city center",
                "color": "red",
            },
        ],
        routes=[
            {
                "coordinates": [
                    (-23.5613, -46.6558),
                    (-23.5700, -46.6510),
                    (-23.5874, -46.6576),
                ],
                "color": "#6366f1",
                "width": 4,
                "dashed": False,
            },
        ],
        circles=[
            {
                "lat": -23.5613,
                "lng": -46.6558,
                "radius": 300,
                "color": "#6366f1",
                "fill_opacity": 0.1,
            },
        ],
        on_marker_press="handle_pin",
        on_map_press="handle_map_tap",
        class_="w-full h-96",
    )
    root.add(map_component)

    # Legend
    legend = Column(class_="flex flex-col gap-1 px-4 py-3 bg-white border-t border-gray-100")
    legend.add(Text("Markers", class_="text-gray-500 text-xs font-semibold uppercase tracking-wide mb-1"))
    for color, label in [("🟢", "Ibirapuera Park"), ("🔵", "Av. Paulista"), ("🔴", "Sé Cathedral")]:
        row = Row(class_="flex flex-row items-center gap-2")
        row.add(Text(color, class_="text-sm"))
        row.add(Text(label, class_="text-gray-700 text-xs"))
        legend.add(row)
    root.add(legend)

    return root.build()


def main():
    Render.execute(create_view)


if __name__ == "__main__":
    main()
