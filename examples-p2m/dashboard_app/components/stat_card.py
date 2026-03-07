"""Stat card component for the dashboard."""
from p2m.ui import Card, Row, Text, Badge


def stat_card(title: str, value: str, change: str, positive: bool = True, icon: str = "📊") -> Card:
    card = Card(class_="flex-1 p-4 rounded-xl bg-white shadow-sm border border-gray-100")

    header = Row(class_="flex flex-row items-center justify-between mb-2")
    header.add(Text(icon, class_="text-2xl"))
    change_color = "bg-green-100 text-green-600" if positive else "bg-red-100 text-red-500"
    prefix = "+" if positive else ""
    header.add(Badge(f"{prefix}{change}", class_=f"text-xs font-medium px-2 py-1 rounded-full {change_color}"))
    card.add(header)

    card.add(Text(value, class_="text-2xl font-bold text-gray-900 mb-1"))
    card.add(Text(title, class_="text-sm text-gray-500"))
    return card
