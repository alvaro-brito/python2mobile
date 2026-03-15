"""
Device Sensors (Accelerometer, Gyroscope, Magnetometer) native capability.

React Native: expo-sensors
Flutter: sensors_plus ^6.0.0
"""

from p2m.native.base import NativeCapability


class Sensors(NativeCapability):
    """
    Native device sensors — accelerometer, gyroscope, or magnetometer.

    Args:
        sensor_type:    "accelerometer" | "gyroscope" | "magnetometer"
        interval:       Update interval in milliseconds (default 100ms)
        on_update:      handler name or callable — fn(x: float, y: float, z: float)
                        For accelerometer: x/y/z in m/s² (gravity ~9.8 on z when flat)
                        For gyroscope: x/y/z in rad/s
                        For magnetometer: x/y/z in μT
        class_:         Tailwind classes

    Example::

        accel = Sensors(
            sensor_type="accelerometer",
            interval=200,
            on_update="handle_accel",
        )

        def handle_accel(x: float, y: float, z: float):
            store.accel_x = round(x, 2)
            store.accel_y = round(y, 2)
            store.accel_z = round(z, 2)
            # Detect shake
            if abs(x) > 15 or abs(y) > 15:
                store.shake_count += 1
        events.register("handle_accel", handle_accel)
    """

    def __init__(
        self,
        sensor_type: str = "accelerometer",
        interval: int = 100,
        on_update=None,
        class_: str = "",
        **props,
    ):
        if callable(on_update):
            on_update = on_update.__name__

        super().__init__(
            "Sensors",
            sensor_type=sensor_type,
            interval=interval,
            on_update=on_update,
            class_=class_,
            **props,
        )
