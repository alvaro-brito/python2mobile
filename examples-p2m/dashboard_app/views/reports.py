"""Reports screen — transactions list."""
from p2m.ui import Column, Row, Container, Text, Button, Card, Badge
from p2m.core.state import AppState


_TRANSACTIONS = [
    ("T-001", "Camiseta Azul",     "R$89,90",  "Pago",       "bg-green-100 text-green-700"),
    ("T-002", "Tênis Sport",       "R$299,00", "Pago",       "bg-green-100 text-green-700"),
    ("T-003", "Mochila Slim",      "R$149,50", "Em trânsito","bg-blue-100 text-blue-700"),
    ("T-004", "Fone Bluetooth",    "R$199,90", "Pendente",   "bg-yellow-100 text-yellow-700"),
    ("T-005", "Smartwatch",        "R$599,00", "Pago",       "bg-green-100 text-green-700"),
    ("T-006", "Carregador USB-C",  "R$49,90",  "Cancelado",  "bg-red-100 text-red-700"),
]


def reports_view(store: AppState) -> Column:
    root = Column(class_="flex flex-col bg-gray-50 min-h-screen")

    header = Container(class_="px-4 pt-10 pb-4 bg-white shadow-sm")
    header.add(Text("📈 Relatórios", class_="text-2xl font-bold text-gray-900"))
    header.add(Text("Últimas transações", class_="text-sm text-gray-500 mt-1"))
    root.add(header)

    # Summary strip
    summary = Row(class_="flex flex-row gap-3 px-4 py-4")
    for label, val in [("Total", "R$1.387,20"), ("Pedidos", "6"), ("Taxa de sucesso", "67%")]:
        card = Card(class_="flex-1 p-3 bg-white rounded-xl shadow-sm border border-gray-100 text-center")
        card.add(Text(val,   class_="text-lg font-bold text-gray-900"))
        card.add(Text(label, class_="text-xs text-gray-500"))
        summary.add(card)
    root.add(summary)

    # Transactions list
    list_card = Card(class_="mx-4 bg-white rounded-xl shadow-sm border border-gray-100 mb-4")
    list_card.add(Text("Transações", class_="text-sm font-semibold text-gray-700 p-4 border-b border-gray-100"))
    for tid, name, price, status, badge_cls in _TRANSACTIONS:
        row = Row(class_="flex flex-row items-center justify-between px-4 py-3 border-b border-gray-50")
        left = Column(class_="flex flex-col")
        left.add(Text(name, class_="text-sm font-medium text-gray-900"))
        left.add(Text(tid,  class_="text-xs text-gray-400"))
        row.add(left)
        right = Column(class_="flex flex-col")
        right.add(Text(price,  class_="text-sm font-semibold text-gray-900"))
        right.add(Badge(status, class_=f"text-xs px-2 py-1 rounded-full {badge_cls}"))
        row.add(right)
        list_card.add(row)
    root.add(list_card)

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
