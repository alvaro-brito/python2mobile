"""
Push Notifications native capability.

React Native: expo-notifications
Flutter: firebase_messaging ^15.0.0
"""

from p2m.native.base import NativeCapability


class PushNotifications(NativeCapability):
    """
    Native push notifications capability.

    Registers the device for push notifications and handles incoming messages.

    Args:
        on_register: handler name or callable — fn(token: str)
                     called when the device token is obtained
        on_message:  handler name or callable — fn(title: str, body: str, data: str)
                     called when a push notification is received
        on_error:    handler name or callable — fn(error: str)
        class_:      Tailwind classes

    Example::

        push = PushNotifications(
            on_register="handle_push_token",
            on_message="handle_notification",
            on_error="handle_push_error",
        )

        def handle_push_token(token: str):
            store.push_token = token
        events.register("handle_push_token", handle_push_token)

        def handle_notification(title: str, body: str, data: str):
            store.last_notification = title
        events.register("handle_notification", handle_notification)
    """

    def __init__(
        self,
        on_register=None,
        on_message=None,
        on_error=None,
        class_: str = "",
        **props,
    ):
        if callable(on_register):
            on_register = on_register.__name__
        if callable(on_message):
            on_message = on_message.__name__
        if callable(on_error):
            on_error = on_error.__name__

        super().__init__(
            "PushNotifications",
            on_register=on_register,
            on_message=on_message,
            on_error=on_error,
            class_=class_,
            **props,
        )
