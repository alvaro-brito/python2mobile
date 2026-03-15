"""
P2M Native Capabilities — declarative access to device hardware APIs.

Each capability renders a simulation panel in `p2m run` (browser dev mode)
and generates the correct native code in `p2m build` (Flutter / React Native).

Usage::

    from p2m.native import Camera, Location, Biometrics, SecureStorage, Share
    # ... etc.

    cam = Camera(mode="photo", on_capture="handle_photo", class_="w-full")
    root.add(cam)
"""

from p2m.native.camera import Camera
from p2m.native.location import Location
from p2m.native.push_notifications import PushNotifications
from p2m.native.biometrics import Biometrics
from p2m.native.bluetooth import Bluetooth
from p2m.native.in_app_purchase import InAppPurchase
from p2m.native.sensors import Sensors
from p2m.native.secure_storage import SecureStorage
from p2m.native.share import Share
from p2m.native.map import Map

__all__ = [
    "Camera",
    "Location",
    "PushNotifications",
    "Biometrics",
    "Bluetooth",
    "InAppPurchase",
    "Sensors",
    "SecureStorage",
    "Share",
    "Map",
]
