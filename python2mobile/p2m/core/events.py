"""
P2M Event System - Global handler registry
Handlers are registered by name and dispatched on WebSocket events.
"""
from typing import Any, Callable, Dict


_handlers: Dict[str, Callable] = {}


def register(name: str, func: Callable) -> None:
    """Register a named event handler."""
    _handlers[name] = func


def unregister(name: str) -> None:
    _handlers.pop(name, None)


def clear() -> None:
    _handlers.clear()


def dispatch(name: str, *args: Any) -> bool:
    """Call handler by name. Returns True if handler found."""
    handler = _handlers.get(name)
    if not handler:
        return False
    try:
        if args:
            handler(*args)
        else:
            handler()
        return True
    except TypeError:
        # Handler signature mismatch — try without args
        try:
            handler()
            return True
        except Exception as e:
            print(f"[P2M] Handler '{name}' error: {e}")
    except Exception as e:
        print(f"[P2M] Handler '{name}' error: {e}")
    return False


def on(name: str) -> Callable:
    """Decorator: @events.on('my_action')"""
    def decorator(func: Callable) -> Callable:
        _handlers[name] = func
        return func
    return decorator


def has(name: str) -> bool:
    return name in _handlers
