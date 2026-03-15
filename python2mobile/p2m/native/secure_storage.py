"""
Secure Storage (Keychain / Keystore) native capability.

React Native: expo-secure-store
Flutter: flutter_secure_storage ^9.2.0

In `p2m run` (dev mode): backed by an in-memory dict — fully functional for testing.
In `p2m build`: translates to Keychain (iOS) / Keystore (Android).
"""

from p2m.native.base import NativeCapability


class SecureStorage(NativeCapability):
    """
    Native secure key-value storage — Keychain on iOS, Keystore on Android.

    Fully functional in dev mode (in-memory). Call .read(), .write(), .delete()
    from your event handlers; callbacks are dispatched synchronously.

    Args:
        on_read:    handler name or callable — fn(key: str, value: str | None)
        on_write:   handler name or callable — fn(key: str, success: bool)
        on_delete:  handler name or callable — fn(key: str, success: bool)
        class_:     Tailwind classes

    Example::

        secure = SecureStorage(
            on_read="handle_secret_loaded",
            on_write="handle_secret_saved",
        )

        def save_token():
            secure.write("auth_token", store.token)
        events.register("save_token", save_token)

        def load_token():
            secure.read("auth_token")
        events.register("load_token", load_token)

        def handle_secret_loaded(key: str, value: str):
            store.token = value or ""
        events.register("handle_secret_loaded", handle_secret_loaded)
    """

    def __init__(
        self,
        on_read=None,
        on_write=None,
        on_delete=None,
        class_: str = "",
        **props,
    ):
        if callable(on_read):
            on_read = on_read.__name__
        if callable(on_write):
            on_write = on_write.__name__
        if callable(on_delete):
            on_delete = on_delete.__name__

        super().__init__(
            "SecureStorage",
            on_read=on_read,
            on_write=on_write,
            on_delete=on_delete,
            class_=class_,
            **props,
        )

        # Keep string references for dispatch
        self._on_read = on_read
        self._on_write = on_write
        self._on_delete = on_delete
        # In-memory store for dev mode
        self._storage: dict = {}

    # ------------------------------------------------------------------
    # Runtime API (used from event handlers)
    # ------------------------------------------------------------------

    def read(self, key: str) -> None:
        """Read a value from secure storage. Calls on_read(key, value)."""
        value = self._storage.get(key)
        if self._on_read:
            from p2m.core.events import dispatch
            dispatch(self._on_read, key, value)

    def write(self, key: str, value: str) -> None:
        """Write a value to secure storage. Calls on_write(key, True)."""
        self._storage[key] = value
        if self._on_write:
            from p2m.core.events import dispatch
            dispatch(self._on_write, key, True)

    def delete(self, key: str) -> None:
        """Delete a value from secure storage. Calls on_delete(key, True)."""
        self._storage.pop(key, None)
        if self._on_delete:
            from p2m.core.events import dispatch
            dispatch(self._on_delete, key, True)
