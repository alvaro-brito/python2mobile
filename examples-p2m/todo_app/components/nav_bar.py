"""Bottom navigation bar component"""
from p2m.ui import Container, Button, Row, Text


def nav_bar(current: str) -> Container:
    tabs = [
        ("home",  "📋", "Tarefas"),
        ("done",  "✅", "Concluídas"),
        ("stats", "📊", "Stats"),
    ]
    bar = Row(class_="flex border-t border-gray-200 bg-white sticky bottom-0")
    for key, icon, label in tabs:
        active = current == key
        bg = "bg-blue-50" if active else ""
        color = "text-blue-600" if active else "text-gray-400"
        btn = Button(
            f"{icon} {label}",
            class_=f"flex-1 py-3 text-xs font-medium {color} {bg}",
            on_click="nav_go",
            on_click_args=[key],
        )
        bar.add(btn)
    return bar
