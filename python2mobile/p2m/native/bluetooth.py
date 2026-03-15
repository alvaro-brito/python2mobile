"""
Bluetooth BLE (Bluetooth Low Energy) native capability.

React Native: react-native-ble-plx ^3.2.0
Flutter: flutter_blue_plus ^1.35.0
"""

from p2m.native.base import NativeCapability


class Bluetooth(NativeCapability):
    """
    Native Bluetooth BLE capability — scan, connect, read/write characteristics.

    Args:
        service_uuid:       Filter scan results by service UUID (optional, "" = all)
        on_scan_result:     handler name or callable — fn(name: str, id: str, rssi: int)
        on_connect:         handler name or callable — fn(device_id: str)
        on_disconnect:      handler name or callable — fn(device_id: str)
        on_data:            handler name or callable — fn(device_id: str, characteristic: str, value: str)
        on_error:           handler name or callable — fn(error: str)
        class_:             Tailwind classes

    Example::

        ble = Bluetooth(
            service_uuid="FFE0",
            on_scan_result="handle_device_found",
            on_connect="handle_ble_connect",
            on_data="handle_ble_data",
            on_error="handle_ble_error",
        )

        def handle_device_found(name: str, id: str, rssi: int):
            store.devices.append({"name": name, "id": id, "rssi": rssi})
        events.register("handle_device_found", handle_device_found)
    """

    def __init__(
        self,
        service_uuid: str = "",
        on_scan_result=None,
        on_connect=None,
        on_disconnect=None,
        on_data=None,
        on_error=None,
        class_: str = "",
        **props,
    ):
        if callable(on_scan_result):
            on_scan_result = on_scan_result.__name__
        if callable(on_connect):
            on_connect = on_connect.__name__
        if callable(on_disconnect):
            on_disconnect = on_disconnect.__name__
        if callable(on_data):
            on_data = on_data.__name__
        if callable(on_error):
            on_error = on_error.__name__

        super().__init__(
            "Bluetooth",
            service_uuid=service_uuid,
            on_scan_result=on_scan_result,
            on_connect=on_connect,
            on_disconnect=on_disconnect,
            on_data=on_data,
            on_error=on_error,
            class_=class_,
            **props,
        )
