"""Settings screen — preferences and profile."""
from p2m.ui import Column, Row, Container, Text, Button, Card
from p2m.core.state import AppState


def settings_view(store: AppState) -> Column:
    root = Column(class_="flex flex-col bg-gray-50 min-h-screen")

    header = Container(class_="px-4 pt-10 pb-4 bg-white shadow-sm")
    header.add(Text("⚙️ Configurações", class_="text-2xl font-bold text-gray-900"))
    root.add(header)

    content = Column(class_="flex flex-col px-4 py-4 space-y-4")

    # Profile card
    profile = Card(class_="bg-white rounded-xl p-4 shadow-sm border border-gray-100")
    pr = Row(class_="flex flex-row items-center gap-4")
    pr.add(Text("👤", class_="text-4xl"))
    info = Column(class_="flex flex-col")
    info.add(Text("Administrador",  class_="text-base font-semibold text-gray-900"))
    info.add(Text("admin@p2m.dev",  class_="text-sm text-gray-500"))
    pr.add(info)
    profile.add(pr)
    content.add(profile)

    # Preferences card
    prefs = Card(class_="bg-white rounded-xl p-4 shadow-sm border border-gray-100")
    prefs.add(Text("Preferências", class_="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3"))

    # Notifications toggle
    notif_row = Row(class_="flex flex-row items-center justify-between py-3 border-b border-gray-100")
    nl = Row(class_="flex flex-row items-center gap-3")
    nl.add(Text("🔔", class_="text-xl"))
    nl.add(Text("Notificações", class_="text-base text-gray-900"))
    notif_row.add(nl)
    n_active = store.notifications_enabled
    n_label  = "Ativo"   if n_active else "Inativo"
    n_color  = "bg-blue-500 text-white" if n_active else "bg-gray-200 text-gray-600"
    notif_row.add(Button(n_label, class_=f"px-3 py-1 rounded-full text-sm font-medium {n_color}", on_click="toggle_notifications"))
    prefs.add(notif_row)

    # Dark mode toggle
    dark_row = Row(class_="flex flex-row items-center justify-between py-3")
    dl = Row(class_="flex flex-row items-center gap-3")
    dl.add(Text("🌙", class_="text-xl"))
    dl.add(Text("Modo Escuro", class_="text-base text-gray-900"))
    dark_row.add(dl)
    d_active = store.dark_mode
    d_label  = "Ativo"   if d_active else "Inativo"
    d_color  = "bg-blue-500 text-white" if d_active else "bg-gray-200 text-gray-600"
    dark_row.add(Button(d_label, class_=f"px-3 py-1 rounded-full text-sm font-medium {d_color}", on_click="toggle_dark_mode"))
    prefs.add(dark_row)

    content.add(prefs)

    # About
    about = Card(class_="bg-white rounded-xl p-4 shadow-sm border border-gray-100")
    about.add(Text("Sobre", class_="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2"))
    about.add(Text("Dashboard App v1.0.0",           class_="text-sm text-gray-700"))
    about.add(Text("Desenvolvido com Python2Mobile", class_="text-xs text-gray-400 mt-1"))
    content.add(about)

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
