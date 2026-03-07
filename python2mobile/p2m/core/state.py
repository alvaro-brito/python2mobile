"""
P2M State Management - Simple state container for P2M apps
"""
from typing import Any, Dict


class AppState:
    """
    Simple key-value state store.
    Use module-level instances (singletons) so state is shared across files.

    Example:
        # state/store.py
        from p2m.core.state import AppState
        store = AppState(counter=0, todos=[])

        # Any other file
        from state.store import store
        store.counter += 1
    """

    def __init__(self, **initial: Any):
        # Use object.__setattr__ to avoid recursion in __setattr__
        object.__setattr__(self, "_data", dict(initial))

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    def update(self, **kwargs: Any) -> None:
        self._data.update(kwargs)

    def __getattr__(self, key: str) -> Any:
        data = object.__getattribute__(self, "_data")
        if key in data:
            return data[key]
        raise AttributeError(f"AppState has no attribute '{key}'")

    def __setattr__(self, key: str, value: Any) -> None:
        self._data[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def to_dict(self) -> Dict[str, Any]:
        return dict(self._data)

    def __repr__(self) -> str:
        return f"AppState({self._data!r})"
