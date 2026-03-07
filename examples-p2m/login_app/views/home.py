"""Home screen — shown after successful authentication."""
from p2m.ui import Column, Row, Container, Text, Button, Card
from p2m.core.state import AppState


def home_view(store: AppState) -> Column:
    root = Column(class_="flex flex-col bg-gray-50 min-h-screen")

    # App bar
    app_bar = Row(class_="flex flex-row items-center justify-between px-4 pt-10 pb-4 bg-white shadow-sm")
    app_bar.add(Text("🏠 Início", class_="text-xl font-bold text-gray-900"))
    app_bar.add(Button(
        "Sair",
        class_="px-4 py-2 bg-gray-100 text-gray-700 text-sm font-medium rounded-lg",
        on_click="do_logout",
    ))
    root.add(app_bar)

    content = Column(class_="flex flex-col px-4 py-6 space-y-4")

    # Welcome card
    welcome = Card(class_="bg-blue-600 rounded-2xl p-6 text-center")
    welcome.add(Text("👋",   class_="text-4xl mb-2"))
    welcome.add(Text(f"Olá, {store.logged_user}!",  class_="text-xl font-bold text-white"))
    welcome.add(Text("Login realizado com sucesso.", class_="text-sm text-blue-100 mt-1"))
    content.add(welcome)

    # Quick stats
    stats = Row(class_="flex flex-row gap-3")
    for label, val, icon in [("Sessões", "42", "📅"), ("Ações", "128", "⚡"), ("Dias", "7", "🗓️")]:
        card = Card(class_="flex-1 bg-white rounded-xl p-3 shadow-sm border border-gray-100 text-center")
        card.add(Text(icon, class_="text-2xl mb-1"))
        card.add(Text(val,   class_="text-xl font-bold text-gray-900"))
        card.add(Text(label, class_="text-xs text-gray-500"))
        stats.add(card)
    content.add(stats)

    # Account info
    info = Card(class_="bg-white rounded-xl p-4 shadow-sm border border-gray-100")
    info.add(Text("Informações da Conta", class_="text-sm font-semibold text-gray-700 mb-3"))
    for label, val in [
        ("Usuário", store.logged_user or ""),
        ("E-mail",  store.email),
        ("Status",  "Ativo"),
    ]:
        row = Row(class_="flex flex-row items-center justify-between py-2 border-b border-gray-50")
        row.add(Text(label, class_="text-sm text-gray-500"))
        row.add(Text(val,   class_="text-sm font-medium text-gray-900"))
        info.add(row)
    content.add(info)

    root.add(content)
    return root
