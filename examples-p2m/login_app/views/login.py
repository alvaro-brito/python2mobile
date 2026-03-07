"""Login screen — authentication form."""
from p2m.ui import Column, Container, Text, Button, Input, Card
from p2m.core.state import AppState


def login_view(store: AppState) -> Column:
    root = Column(class_="flex flex-col bg-gray-50 min-h-screen")

    # Hero
    hero = Container(class_="flex flex-col items-center px-6 pt-16 pb-8")
    hero.add(Text("🔐", class_="text-6xl mb-4"))
    hero.add(Text("Bem-vindo",              class_="text-3xl font-bold text-gray-900"))
    hero.add(Text("Faça login para continuar", class_="text-sm text-gray-500 mt-2"))
    root.add(hero)

    # Form card
    form = Card(class_="mx-6 bg-white rounded-2xl p-6 shadow-md border border-gray-100")

    form.add(Text("E-mail", class_="text-sm font-medium text-gray-700 mb-1"))
    form.add(Input(
        placeholder="seu@email.com",
        class_="w-full mb-4",
        on_change="update_email",
        value=store.email,
        input_type="email",
    ))

    form.add(Text("Senha", class_="text-sm font-medium text-gray-700 mb-1"))
    form.add(Input(
        placeholder="••••••",
        class_="w-full mb-4",
        on_change="update_password",
        value=store.password,
        input_type="password",
    ))

    if store.error:
        form.add(Text(f"⚠️ {store.error}", class_="text-sm text-red-500 mb-3"))

    form.add(Button(
        "Entrar",
        class_="w-full py-3 bg-blue-600 text-white font-semibold rounded-xl",
        on_click="do_login",
    ))
    root.add(form)

    hint = Container(class_="px-6 mt-4")
    hint.add(Text("💡 Demo: admin@p2m.dev / 123456", class_="text-xs text-gray-400 text-center"))
    root.add(hint)

    return root
