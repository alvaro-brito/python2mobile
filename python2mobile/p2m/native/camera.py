"""
Camera native capability — take photos or record video.

React Native: expo-camera
Flutter: camera ^0.11.0
"""

from p2m.native.base import NativeCapability


class Camera(NativeCapability):
    """
    Native camera capability.

    Args:
        mode:       "photo" | "video" | "both"
        on_capture: handler name or callable — fn(uri: str, type: str)
                    called with ("mock://photo_1.jpg", "photo") in dev mode
        on_error:   handler name or callable — fn(error: str)
        class_:     Tailwind classes for the component container

    Example::

        cam = Camera(
            mode="photo",
            on_capture="handle_photo",
            on_error="handle_cam_error",
            class_="w-full rounded-xl",
        )

        def handle_photo(uri: str, type: str):
            store.photo_uri = uri
        events.register("handle_photo", handle_photo)
    """

    def __init__(
        self,
        mode: str = "photo",
        on_capture=None,
        on_error=None,
        class_: str = "",
        **props,
    ):
        if callable(on_capture):
            on_capture = on_capture.__name__
        if callable(on_error):
            on_error = on_error.__name__

        super().__init__(
            "Camera",
            mode=mode,
            on_capture=on_capture,
            on_error=on_error,
            class_=class_,
            **props,
        )
