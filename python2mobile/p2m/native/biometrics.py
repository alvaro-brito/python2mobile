"""
Biometrics (Face ID / Touch ID / Fingerprint) native capability.

React Native: expo-local-authentication
Flutter: local_auth ^2.3.0
"""

from p2m.native.base import NativeCapability


class Biometrics(NativeCapability):
    """
    Native biometric authentication — Face ID, Touch ID, or fingerprint.

    Args:
        prompt:         Message shown in the OS auth dialog
        fallback_label: Label for the password fallback button (iOS)
        on_success:     handler name or callable — fn()
        on_failure:     handler name or callable — fn(error: str)
                        error values: "UserCancel" | "SystemCancel" | "NotEnrolled" | "NotAvailable"
        class_:         Tailwind classes

    Example::

        bio = Biometrics(
            prompt="Confirme sua identidade",
            fallback_label="Usar Senha",
            on_success="handle_auth_success",
            on_failure="handle_auth_failure",
        )

        def handle_auth_success():
            store.authenticated = True
        events.register("handle_auth_success", handle_auth_success)

        def handle_auth_failure(error: str):
            store.auth_error = error
        events.register("handle_auth_failure", handle_auth_failure)
    """

    def __init__(
        self,
        prompt: str = "Confirm your identity",
        fallback_label: str = "Use Password",
        on_success=None,
        on_failure=None,
        class_: str = "",
        **props,
    ):
        if callable(on_success):
            on_success = on_success.__name__
        if callable(on_failure):
            on_failure = on_failure.__name__

        super().__init__(
            "Biometrics",
            prompt=prompt,
            fallback_label=fallback_label,
            on_success=on_success,
            on_failure=on_failure,
            class_=class_,
            **props,
        )
