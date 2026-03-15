"""
Location / GPS native capability.

React Native: expo-location
Flutter: geolocator ^13.0.0
"""

from p2m.native.base import NativeCapability


class Location(NativeCapability):
    """
    Native GPS / location capability.

    Args:
        watch:      True = stream continuous updates, False = one-shot request
        accuracy:   "low" | "medium" | "high"
        on_update:  handler name or callable — fn(lat: float, lng: float, accuracy: float)
        on_error:   handler name or callable — fn(error: str)
        class_:     Tailwind classes

    Example::

        loc = Location(
            watch=False,
            accuracy="high",
            on_update="handle_location",
            on_error="handle_loc_error",
        )

        def handle_location(lat: float, lng: float, accuracy: float):
            store.lat = lat
            store.lng = lng
        events.register("handle_location", handle_location)
    """

    def __init__(
        self,
        watch: bool = False,
        accuracy: str = "high",
        on_update=None,
        on_error=None,
        class_: str = "",
        **props,
    ):
        if callable(on_update):
            on_update = on_update.__name__
        if callable(on_error):
            on_error = on_error.__name__

        super().__init__(
            "Location",
            watch=watch,
            accuracy=accuracy,
            on_update=on_update,
            on_error=on_error,
            class_=class_,
            **props,
        )
