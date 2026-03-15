"""
In-App Purchase / Subscriptions native capability.

React Native: react-native-iap ^12.15.0
Flutter: in_app_purchase ^3.2.0
"""

from p2m.native.base import NativeCapability


class InAppPurchase(NativeCapability):
    """
    Native in-app purchase capability — consumables, non-consumables, and subscriptions.

    Args:
        product_id:     Store product ID (e.g. "com.myapp.premium")
        product_type:   "consumable" | "non_consumable" | "subscription"
        on_purchased:   handler name or callable — fn(product_id: str, transaction_id: str)
        on_restored:    handler name or callable — fn(product_id: str)
                        called when a previous purchase is restored
        on_error:       handler name or callable — fn(error: str)
        class_:         Tailwind classes

    Example::

        iap = InAppPurchase(
            product_id="com.myapp.premium",
            product_type="non_consumable",
            on_purchased="handle_purchase",
            on_error="handle_iap_error",
        )

        def handle_purchase(product_id: str, transaction_id: str):
            store.is_premium = True
        events.register("handle_purchase", handle_purchase)
    """

    def __init__(
        self,
        product_id: str = "",
        product_type: str = "non_consumable",
        on_purchased=None,
        on_restored=None,
        on_error=None,
        class_: str = "",
        **props,
    ):
        if callable(on_purchased):
            on_purchased = on_purchased.__name__
        if callable(on_restored):
            on_restored = on_restored.__name__
        if callable(on_error):
            on_error = on_error.__name__

        super().__init__(
            "InAppPurchase",
            product_id=product_id,
            product_type=product_type,
            on_purchased=on_purchased,
            on_restored=on_restored,
            on_error=on_error,
            class_=class_,
            **props,
        )
