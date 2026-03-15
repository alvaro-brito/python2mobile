"""
Share (OS share sheet) native capability.

React Native: expo-sharing + expo-file-system
Flutter: share_plus ^10.0.0

In `p2m run` (dev mode): immediately calls on_complete(True).
In `p2m build`: opens the native OS share sheet.
"""

from p2m.native.base import NativeCapability


class Share(NativeCapability):
    """
    Native OS share sheet — share text, URLs, or files.

    Call .send() from your event handlers; the OS share sheet opens natively.
    In dev mode, on_complete is called immediately with success=True.

    Args:
        on_complete:    handler name or callable — fn(success: bool)
        class_:         Tailwind classes

    Example::

        share = Share(on_complete="handle_shared")

        def do_share():
            share.send(title="Check this out!", text=store.content, url=store.link)
        events.register("do_share", do_share)

        def handle_shared(success: bool):
            store.share_status = "shared" if success else "cancelled"
        events.register("handle_shared", handle_shared)
    """

    def __init__(self, on_complete=None, class_: str = "", **props):
        if callable(on_complete):
            on_complete = on_complete.__name__

        super().__init__(
            "Share",
            on_complete=on_complete,
            class_=class_,
            **props,
        )

        self._on_complete = on_complete

    # ------------------------------------------------------------------
    # Runtime API
    # ------------------------------------------------------------------

    def send(
        self,
        text: str = "",
        title: str = "",
        url: str = "",
        file_uri: str = "",
    ) -> None:
        """
        Open the OS share sheet.

        In dev mode: immediately calls on_complete(True).
        In production: opens the native share sheet with the provided content.

        Args:
            text:       Main text content to share
            title:      Dialog title (Android only)
            url:        URL to share (use instead of or alongside text)
            file_uri:   Local file URI to attach (e.g. "file:///path/to/image.jpg")
        """
        if self._on_complete:
            from p2m.core.events import dispatch
            dispatch(self._on_complete, True)
