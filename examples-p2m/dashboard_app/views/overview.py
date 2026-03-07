"""Overview screen — main dashboard tab."""
from p2m.ui import Column, Row, Container, Text, Button, Card, ScrollView
from p2m.core.state import AppState
from components.stat_card import stat_card


_ACTIVITIES = [
    ("🛒", "Nova venda",           "há 2 min",  "text-green-600"),
    ("👤", "Novo usuário",         "há 5 min",  "text-blue-600"),
    ("💳", "Pagamento recebido",   "há 12 min", "text-emerald-600"),
    ("📦", "Pedido enviado",       "há 28 min", "text-orange-500"),
    ("⚠️", "Estoque baixo",        "há 1h",     "text-red-500"),
]


def overview_view(store: AppState) -> Column:
    root = Column(class_="flex flex-col bg-gray-50 min-h-screen")

    # Header
    header = Container(class_="px-4 pt-10 pb-4 bg-white shadow-sm")
    header.add(Text("📊 Dashboard", class_="text-2xl font-bold text-gray-900"))
    header.add(Text("Visão geral de hoje", class_="text-sm text-gray-500 mt-1"))
    root.add(header)

    content = ScrollView(class_="flex flex-col flex-1 px-4 py-4 space-y-4")

    # Stat rows
    row1 = Row(class_="flex flex-row gap-3")
    row1.add(stat_card("Usuários",  "1.247",   "12%", True,  "👥"))
    row1.add(stat_card("Receita",   "R$8.432", "8%",  True,  "💰"))
    content.add(row1)

    row2 = Row(class_="flex flex-row gap-3")
    row2.add(stat_card("Pedidos",       "184", "5%", True,  "🛒"))
    row2.add(stat_card("Cancelamentos", "12",  "3%", False, "❌"))
    content.add(row2)

    # Recent activity
    activity = Card(class_="bg-white rounded-xl p-4 shadow-sm border border-gray-100")
    activity.add(Text("Atividade Recente", class_="text-base font-semibold text-gray-900 mb-3"))
    for icon, title, time, color in _ACTIVITIES:
        item = Row(class_="flex flex-row items-center justify-between py-2 border-b border-gray-50")
        left = Row(class_="flex flex-row items-center gap-3")
        left.add(Text(icon, class_="text-xl"))
        left.add(Text(title, class_=f"text-sm font-medium {color}"))
        item.add(left)
        item.add(Text(time, class_="text-xs text-gray-400"))
        activity.add(item)
    content.add(activity)

    root.add(content)
    root.add(_nav_bar(store.current_tab))
    return root


def _nav_bar(current: str) -> Row:
    tabs = [
        ("overview",  "🏠", "Visão Geral"),
        ("reports",   "📈", "Relatórios"),
        ("settings",  "⚙️", "Config"),
    ]
    bar = Row(class_="flex flex-row border-t border-gray-200 bg-white")
    for key, icon, label in tabs:
        active = current == key
        color = "text-blue-600" if active else "text-gray-400"
        bg    = "bg-blue-50"    if active else ""
        bar.add(Button(
            f"{icon} {label}",
            class_=f"flex-1 py-3 text-xs font-medium {color} {bg}",
            on_click="nav_tab",
            on_click_args=[key],
        ))
    return bar
