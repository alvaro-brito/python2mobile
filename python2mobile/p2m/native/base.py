"""
Base class for all P2M native device capabilities.
"""

from p2m.ui.components import Component


class NativeCapability(Component):
    """
    Base for all native device capabilities (Camera, Location, etc.).

    Inherits from Component so it fits anywhere in the P2M view tree.
    In `p2m run` it renders a mock simulation panel.
    In `p2m build` the platform agents translate it to native code.
    """

    def __init__(self, capability_type: str, **props):
        super().__init__(
            component_type=f"Native_{capability_type}",
            props=props,
        )
