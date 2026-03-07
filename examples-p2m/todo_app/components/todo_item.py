"""Single todo item component — registers its own handlers"""
from p2m.ui import Row, Column, Button, Text, Badge, Container
from p2m.core import events


def todo_item(todo: dict, store) -> Row:
    tid = todo["id"]

    # Register per-item handlers (refreshed each render)
    def _toggle(id=tid):
        for t in store.todos:
            if t["id"] == id:
                t["done"] = not t["done"]

    def _delete(id=tid):
        store.todos[:] = [t for t in store.todos if t["id"] != id]

    events.register(f"toggle_{tid}", _toggle)
    events.register(f"delete_{tid}", _delete)

    row = Row(
        class_="flex items-center justify-between px-4 py-3 bg-white border-b border-gray-100"
    )

    # Left: checkbox + text
    left = Row(class_="flex items-center gap-3 flex-1")
    check_style = (
        "bg-green-500 text-white rounded-full w-6 h-6 text-xs font-bold flex-shrink-0"
        if todo["done"]
        else "border border-gray-300 rounded-full w-6 h-6 text-xs flex-shrink-0 bg-white"
    )
    chk = Button(
        "✓" if todo["done"] else "",
        class_=check_style,
        on_click=f"toggle_{tid}",
    )
    label_style = "text-gray-800 text-sm flex-1" + (" line-through opacity-50" if todo["done"] else "")
    lbl = Text(todo["text"], class_=label_style)
    left.add(chk).add(lbl)

    # Right: delete
    del_btn = Button(
        "🗑",
        class_="text-red-400 text-sm ml-2",
        on_click=f"delete_{tid}",
    )

    row.add(left).add(del_btn)
    return row
