"""Calculator UI view."""
from p2m.ui import Column, Row, Container, Text, Button
from p2m.core.state import AppState


def _digit_btn(digit: str) -> Button:
    return Button(
        digit,
        class_="flex-1 py-5 rounded-2xl bg-gray-700 text-white text-xl font-medium",
        on_click="press_digit",
        on_click_args=[digit],
    )


def _op_btn(label: str, op: str, current_op) -> Button:
    active = current_op == op
    bg = "bg-white text-orange-500" if active else "bg-orange-500 text-white"
    return Button(
        label,
        class_=f"flex-1 py-5 rounded-2xl {bg} text-xl font-bold",
        on_click="press_operator",
        on_click_args=[op],
    )


def calculator_view(store: AppState) -> Column:
    root = Column(class_="flex flex-col bg-gray-900 min-h-screen")

    # ── Display ──────────────────────────────────────────────────────────
    display_area = Container(class_="px-6 pt-12 pb-6")
    op_label = store.operator or ""
    display_area.add(Text(op_label, class_="text-gray-500 text-base text-right"))

    n = len(str(store.display))
    size = "text-6xl" if n <= 7 else ("text-4xl" if n <= 10 else "text-2xl")
    display_area.add(Text(store.display, class_=f"{size} font-light text-white text-right"))
    root.add(display_area)

    # ── Button grid ───────────────────────────────────────────────────────
    grid = Container(class_="flex flex-col px-4 pb-8 space-y-3")

    # Row 1: C  +/-  %  ÷
    r1 = Row(class_="flex flex-row gap-3")
    r1.add(Button("C",   class_="flex-1 py-5 rounded-2xl bg-gray-400 text-gray-900 text-xl font-semibold", on_click="press_clear"))
    r1.add(Button("+/-", class_="flex-1 py-5 rounded-2xl bg-gray-400 text-gray-900 text-xl font-semibold", on_click="press_toggle_sign"))
    r1.add(Button("%",   class_="flex-1 py-5 rounded-2xl bg-gray-400 text-gray-900 text-xl font-semibold", on_click="press_percent"))
    r1.add(_op_btn("÷", "/", store.operator))
    grid.add(r1)

    # Row 2: 7  8  9  ×
    r2 = Row(class_="flex flex-row gap-3")
    for d in ["7", "8", "9"]:
        r2.add(_digit_btn(d))
    r2.add(_op_btn("×", "*", store.operator))
    grid.add(r2)

    # Row 3: 4  5  6  −
    r3 = Row(class_="flex flex-row gap-3")
    for d in ["4", "5", "6"]:
        r3.add(_digit_btn(d))
    r3.add(_op_btn("−", "-", store.operator))
    grid.add(r3)

    # Row 4: 1  2  3  +
    r4 = Row(class_="flex flex-row gap-3")
    for d in ["1", "2", "3"]:
        r4.add(_digit_btn(d))
    r4.add(_op_btn("+", "+", store.operator))
    grid.add(r4)

    # Row 5: 0  .  =
    r5 = Row(class_="flex flex-row gap-3")
    r5.add(_digit_btn("0"))
    r5.add(_digit_btn("."))
    r5.add(Button("=", class_="flex-1 py-5 rounded-2xl bg-orange-500 text-white text-xl font-bold", on_click="press_equals"))
    grid.add(r5)

    root.add(grid)
    return root
