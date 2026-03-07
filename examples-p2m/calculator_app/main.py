"""Calculator App — P2M demo.

A fully functional calculator demonstrating parameterised event handlers
(press_digit/press_operator called with args from the UI).
"""
from p2m.core import Render, events
from state.store import store


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _format(val: float) -> str:
    """Format a float for the calculator display (max 12 chars)."""
    try:
        if abs(val) >= 1e12 or (val != 0 and abs(val) < 1e-9):
            return f"{val:.3e}"
        if val == int(val):
            return str(int(val))
        s = f"{val:.8f}".rstrip("0").rstrip(".")
        return s[:12]
    except (ValueError, OverflowError):
        return "Erro"


def _calculate():
    """Compute first_num OP display and store the result in display."""
    try:
        a = float(store.first_num)
        b = float(store.display)
        op = store.operator
        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "*":
            result = a * b
        elif op == "/":
            if b == 0:
                store.display = "Erro"
                store.first_num = None
                store.operator = None
                store.awaiting_operand = True
                return
            result = a / b
        else:
            return
        store.display = _format(result)
    except (ValueError, TypeError):
        store.display = "Erro"


# ──────────────────────────────────────────────────────────────────────────────
# Event handlers
# ──────────────────────────────────────────────────────────────────────────────

def press_digit(digit: str):
    """Append a digit (or '.') to the current display."""
    if digit == "." and "." in store.display and not store.awaiting_operand:
        return
    if store.awaiting_operand:
        store.display = digit if digit != "." else "0."
        store.awaiting_operand = False
    elif store.display == "0" and digit != ".":
        store.display = digit
    else:
        if len(store.display) < 12:
            store.display = store.display + digit


def press_operator(op: str):
    """Set the pending operator; evaluate any chained expression."""
    if store.operator and not store.awaiting_operand:
        _calculate()
    store.first_num = float(store.display)
    store.operator = op
    store.awaiting_operand = True


def press_equals():
    """Evaluate the pending expression."""
    if store.operator is not None and store.first_num is not None:
        _calculate()
        store.operator = None
        store.first_num = None
        store.awaiting_operand = True


def press_clear():
    """Reset calculator to initial state."""
    store.display = "0"
    store.first_num = None
    store.operator = None
    store.awaiting_operand = False


def press_toggle_sign():
    """Toggle the sign of the current display value."""
    if store.display not in ("0", "Erro"):
        if store.display.startswith("-"):
            store.display = store.display[1:]
        else:
            store.display = "-" + store.display


def press_percent():
    """Divide the current display by 100."""
    try:
        val = float(store.display)
        store.display = _format(val / 100)
        store.awaiting_operand = True
    except ValueError:
        pass


events.register("press_digit",       press_digit)
events.register("press_operator",    press_operator)
events.register("press_equals",      press_equals)
events.register("press_clear",       press_clear)
events.register("press_toggle_sign", press_toggle_sign)
events.register("press_percent",     press_percent)


# ──────────────────────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────────────────────

def create_view():
    from views.calculator import calculator_view
    return calculator_view(store).build()


def main():
    Render.execute(create_view)


if __name__ == "__main__":
    main()
