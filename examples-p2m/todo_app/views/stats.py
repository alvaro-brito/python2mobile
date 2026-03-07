"""Stats screen — productivity metrics"""
from p2m.ui import Container, Column, Row, Text, Badge, Card


def _stat_card(value: str, label: str, color: str, bg: str) -> Card:
    card = Card(class_=f"{bg} rounded-2xl p-5 flex-1")
    card.add(Text(value, class_=f"{color} text-3xl font-bold mb-1"))
    card.add(Text(label, class_="text-gray-500 text-xs uppercase tracking-wide"))
    return card


def stats_view(store) -> Container:
    screen = Column(class_="flex flex-col min-h-screen bg-gray-50")

    total = len(store.todos)
    done = sum(1 for t in store.todos if t["done"])
    pending = total - done
    pct = int(done / total * 100) if total else 0

    # Header
    header = Container(class_="bg-purple-600 px-4 pt-8 pb-6")
    header.add(Text("📊 Estatísticas", class_="text-white text-2xl font-bold mb-1"))
    header.add(Text("Seu progresso geral", class_="text-purple-200 text-sm"))

    body = Column(class_="flex-1 p-4 space-y-4")

    # Progress circle (text)
    pct_card = Card(class_="bg-white rounded-2xl p-6 shadow-sm text-center")
    pct_card.add(Text(f"{pct}%", class_="text-6xl font-extrabold text-purple-600 mb-2"))
    pct_card.add(Text("de conclusão", class_="text-gray-500 text-sm"))

    # Progress bar
    bar_bg = Container(class_="bg-gray-200 rounded-full mt-4")
    bar_fill = Container(class_=f"bg-purple-600 rounded-full p-1")
    bar_fill.add(Text(f"{pct}%", class_="text-white text-xs font-bold text-center"))
    bar_bg.add(bar_fill)
    pct_card.add(bar_bg)

    # Stat cards row
    stats_row = Row(class_="flex gap-3")
    stats_row.add(_stat_card(str(total), "Total", "text-gray-800", "bg-white"))
    stats_row.add(_stat_card(str(done), "Feitas", "text-green-600", "bg-green-50"))
    stats_row.add(_stat_card(str(pending), "Pendentes", "text-orange-500", "bg-orange-50"))

    # List of recent todos
    recent_card = Card(class_="bg-white rounded-2xl p-4 shadow-sm")
    recent_card.add(Text("Últimas tarefas", class_="text-gray-700 font-semibold text-sm mb-3"))
    for todo in store.todos[-4:]:
        r = Row(class_="flex items-center gap-2 py-2 border-b border-gray-50")
        r.add(Badge("✓" if todo["done"] else "○",
                    class_="text-xs " + ("text-green-600" if todo["done"] else "text-gray-400")))
        r.add(Text(todo["text"], class_="text-gray-700 text-sm flex-1"))
        recent_card.add(r)

    body.add(pct_card).add(stats_row).add(recent_card)
    screen.add(header).add(body)
    return screen
