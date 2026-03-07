import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { useLanguage } from "@/contexts/LanguageContext";
import CodeBlock from "@/components/CodeBlock";

// ─────────────────────────────────────────────────────────────────────────────
// Todo App
// ─────────────────────────────────────────────────────────────────────────────

const todoFiles = {
  "main.py": `from p2m.core import Render, events
from p2m.ui import Container, Column
from state.store import store
from components.nav_bar import nav_bar


def update_input(value: str):
    store.input_text = value

def add_todo():
    text = store.input_text.strip()
    if text:
        store.todos.append({"id": store.next_id, "text": text, "done": False})
        store.next_id += 1
        store.input_text = ""

def clear_done():
    store.todos[:] = [t for t in store.todos if not t["done"]]

def nav_go(screen: str):
    store.current_screen = screen


events.register("update_input", update_input)
events.register("add_todo",     add_todo)
events.register("clear_done",   clear_done)
events.register("nav_go",       nav_go)


def create_view():
    from views.home  import home_view
    from views.done  import done_view
    from views.stats import stats_view

    root = Column(class_="flex flex-col min-h-screen")

    if store.current_screen == "home":
        content = home_view(store)
    elif store.current_screen == "done":
        content = done_view(store)
    else:
        content = stats_view(store)

    root.add(content)
    root.add(nav_bar(store.current_screen))
    return root.build()


def main():
    Render.execute(create_view)`,

  "state/store.py": `from p2m.core.state import AppState

store = AppState(
    todos=[
        {"id": 1, "text": "Estudar Python2Mobile", "done": False},
        {"id": 2, "text": "Criar primeiro app mobile", "done": True},
        {"id": 3, "text": "Publicar na App Store", "done": False},
    ],
    next_id=4,
    input_text="",
    current_screen="home",   # home | done | stats
)`,

  "views/home.py": `from p2m.ui import Container, Column, Row, Text, Button, Input, Badge
from components.todo_item import todo_item


def home_view(store) -> Container:
    screen = Column(class_="flex flex-col min-h-screen bg-gray-50")

    header = Container(class_="bg-blue-600 px-4 pt-8 pb-5")
    header.add(Text("📋 Minhas Tarefas", class_="text-white text-2xl font-bold mb-1"))
    pending = sum(1 for t in store.todos if not t["done"])
    header.add(Text(f"{pending} pendente(s)", class_="text-blue-200 text-sm"))

    add_row = Row(class_="flex gap-2 px-4 py-3 bg-white border-b border-gray-200")
    inp = Input(
        placeholder="Nova tarefa...",
        value=store.input_text,
        on_change="update_input",
        class_="flex-1 border border-gray-300 rounded-xl px-3 py-2 text-sm",
    )
    add_btn = Button(
        "+ Add",
        class_="bg-blue-600 text-white font-semibold px-4 py-2 rounded-xl text-sm",
        on_click="add_todo",
    )
    add_row.add(inp).add(add_btn)

    active = [t for t in store.todos if not t["done"]]
    list_container = Column(class_="flex-1 bg-white")
    if active:
        for t in active:
            list_container.add(todo_item(t, store))
    else:
        empty = Container(class_="flex flex-col items-center justify-center py-16")
        empty.add(Text("🎉", class_="text-5xl mb-3"))
        empty.add(Text("Tudo feito!", class_="text-gray-500 text-base"))
        list_container.add(empty)

    screen.add(header).add(add_row).add(list_container)
    return screen`,

  "components/todo_item.py": `from p2m.ui import Row, Button, Text
from p2m.core import events


def todo_item(todo: dict, store) -> Row:
    tid = todo["id"]

    def _toggle(id=tid):
        for t in store.todos:
            if t["id"] == id:
                t["done"] = not t["done"]

    def _delete(id=tid):
        store.todos[:] = [t for t in store.todos if t["id"] != id]

    events.register(f"toggle_{tid}", _toggle)
    events.register(f"delete_{tid}", _delete)

    row = Row(class_="flex items-center justify-between px-4 py-3 bg-white border-b border-gray-100")

    left = Row(class_="flex items-center gap-3 flex-1")
    check_style = (
        "bg-green-500 text-white rounded-full w-6 h-6 text-xs font-bold flex-shrink-0"
        if todo["done"]
        else "border border-gray-300 rounded-full w-6 h-6 text-xs flex-shrink-0 bg-white"
    )
    chk = Button("✓" if todo["done"] else "", class_=check_style, on_click=f"toggle_{tid}")
    lbl_style = "text-gray-800 text-sm flex-1" + (" line-through opacity-50" if todo["done"] else "")
    left.add(chk).add(Text(todo["text"], class_=lbl_style))

    del_btn = Button("🗑", class_="text-red-400 text-sm ml-2", on_click=f"delete_{tid}")
    row.add(left).add(del_btn)
    return row`,

  "components/nav_bar.py": `from p2m.ui import Row, Button


def nav_bar(current: str) -> Row:
    tabs = [
        ("home",  "📋", "Tarefas"),
        ("done",  "✅", "Concluídas"),
        ("stats", "📊", "Stats"),
    ]
    bar = Row(class_="flex border-t border-gray-200 bg-white sticky bottom-0")
    for key, icon, label in tabs:
        active = current == key
        color = "text-blue-600" if active else "text-gray-400"
        bg    = "bg-blue-50"    if active else ""
        btn = Button(
            f"{icon} {label}",
            class_=f"flex-1 py-3 text-xs font-medium {color} {bg}",
            on_click="nav_go",
            on_click_args=[key],
        )
        bar.add(btn)
    return bar`,
};

// ─────────────────────────────────────────────────────────────────────────────
// E-commerce App
// ─────────────────────────────────────────────────────────────────────────────

const ecommerceFiles = {
  "main.py": `from p2m.core import Render, events
from p2m.ui import Column
from state.store import store


def search_products(value: str):
    store.search_query = value

def nav_cart():
    store.current_screen = "cart"

def nav_catalog():
    store.current_screen = "catalog"
    store.search_query = ""

def nav_checkout():
    if store.cart:
        store.current_screen = "checkout"

def update_checkout_name(value: str):
    store.checkout_name = value

def update_checkout_email(value: str):
    store.checkout_email = value

def confirm_order():
    if store.checkout_name.strip():
        store.current_screen = "confirm"
        store.cart.clear()


events.register("search_products",      search_products)
events.register("nav_cart",             nav_cart)
events.register("nav_catalog",          nav_catalog)
events.register("nav_checkout",         nav_checkout)
events.register("update_checkout_name", update_checkout_name)
events.register("update_checkout_email",update_checkout_email)
events.register("confirm_order",        confirm_order)


def create_view():
    from views.catalog  import catalog_view
    from views.cart     import cart_view
    from views.checkout import checkout_view, confirm_view

    if store.current_screen == "catalog":
        return catalog_view(store).build()
    elif store.current_screen == "cart":
        return cart_view(store).build()
    elif store.current_screen == "checkout":
        return checkout_view(store).build()
    else:
        return confirm_view(store).build()


def main():
    Render.execute(create_view)`,

  "state/store.py": `from p2m.core.state import AppState

PRODUCTS = [
    {"id": 1, "name": "Tênis Air Max",  "price": 299.90, "emoji": "👟", "cat": "Calçados",  "stock": 5},
    {"id": 2, "name": "Camisa Polo",    "price":  89.90, "emoji": "👕", "cat": "Roupas",    "stock": 12},
    {"id": 3, "name": "Mochila Slim",   "price": 149.90, "emoji": "🎒", "cat": "Acessórios","stock": 3},
    {"id": 4, "name": "Óculos Aviador", "price": 199.90, "emoji": "🕶️", "cat": "Acessórios","stock": 8},
    {"id": 5, "name": "Relógio Sport",  "price": 449.90, "emoji": "⌚", "cat": "Acessórios","stock": 2},
]

store = AppState(
    products=PRODUCTS,
    cart=[],                      # [{"product_id": int, "qty": int}]
    current_screen="catalog",     # catalog | cart | checkout | confirm
    selected_product_id=None,
    search_query="",
    checkout_name="",
    checkout_email="",
)`,

  "views/catalog.py": `from p2m.ui import Container, Column, Row, Text, Input, Button
from components.product_card import product_card


def catalog_view(store) -> Column:
    screen = Column(class_="flex flex-col min-h-screen bg-gray-50")

    hdr = Container(class_="bg-blue-600 px-4 pt-8 pb-5")
    cart_total = sum(i["qty"] for i in store.cart)
    top = Row(class_="flex items-center justify-between mb-3")
    top.add(Text("🛍️ P2M Shop", class_="text-white text-2xl font-bold"))
    top.add(Button(
        f"🛒 {cart_total}",
        class_="bg-white text-blue-700 font-bold px-3 py-1 rounded-full text-sm",
        on_click="nav_cart",
    ))
    hdr.add(top)
    hdr.add(Input(
        placeholder="Buscar produto...",
        value=store.search_query,
        on_change="search_products",
        class_="bg-white rounded-xl px-3 py-2 text-sm w-full",
    ))

    body = Column(class_="flex-1 p-4")
    query = store.search_query.lower()
    filtered = [p for p in store.products if query in p["name"].lower()] if query else store.products
    for p in filtered:
        body.add(product_card(p, store))

    screen.add(hdr).add(body)
    return screen`,

  "components/product_card.py": `from p2m.ui import Card, Row, Column, Text, Button, Badge
from p2m.core import events


def product_card(product: dict, store) -> Card:
    pid = product["id"]

    def _add(id=pid):
        for item in store.cart:
            if item["product_id"] == id:
                item["qty"] += 1
                return
        store.cart.append({"product_id": id, "qty": 1})

    events.register(f"add_to_cart_{pid}", _add)

    card = Card(class_="bg-white rounded-2xl p-4 shadow-sm border border-gray-100 mb-3")
    top = Row(class_="flex items-center justify-between mb-3")
    top.add(Text(product["emoji"], class_="text-4xl"))
    top.add(Badge(product["cat"], class_="bg-blue-100 text-blue-700 text-xs rounded-full px-3 py-1"))
    card.add(top)
    card.add(Text(product["name"],            class_="text-gray-800 font-bold text-base mb-1"))
    card.add(Text(f"R$ {product['price']:.2f}", class_="text-green-600 font-bold text-xl mb-1"))
    card.add(Text(f"Estoque: {product['stock']}", class_="text-gray-400 text-xs mb-3"))

    in_cart  = sum(i["qty"] for i in store.cart if i["product_id"] == pid)
    btn_label = f"🛒 No carrinho ({in_cart})" if in_cart else "🛒 Adicionar"
    btn_style = "bg-green-600" if in_cart else "bg-blue-600"
    card.add(Button(
        btn_label,
        class_=f"{btn_style} text-white font-semibold py-2 px-4 rounded-xl w-full text-sm",
        on_click=f"add_to_cart_{pid}",
    ))
    return card`,
};

// ─────────────────────────────────────────────────────────────────────────────
// Dashboard App
// ─────────────────────────────────────────────────────────────────────────────

const dashboardFiles = {
  "main.py": `from p2m.core import Render, events
from state.store import store


def nav_tab(tab: str):
    store.current_tab = tab

def toggle_notifications():
    store.notifications_enabled = not store.notifications_enabled

def toggle_dark_mode():
    store.dark_mode = not store.dark_mode


events.register("nav_tab",              nav_tab)
events.register("toggle_notifications", toggle_notifications)
events.register("toggle_dark_mode",     toggle_dark_mode)


def create_view():
    if store.current_tab == "reports":
        from views.reports  import reports_view
        return reports_view(store).build()
    elif store.current_tab == "settings":
        from views.settings import settings_view
        return settings_view(store).build()
    else:
        from views.overview import overview_view
        return overview_view(store).build()


def main():
    Render.execute(create_view)`,

  "state/store.py": `from p2m.core.state import AppState

store = AppState(
    current_tab="overview",        # overview | reports | settings
    notifications_enabled=True,
    dark_mode=False,
)`,

  "views/overview.py": `from p2m.ui import Column, Row, Container, Text, Button, Card, ScrollView
from components.stat_card import stat_card

_ACTIVITIES = [
    ("🛒", "Nova venda",          "há 2 min",  "text-green-600"),
    ("👤", "Novo usuário",        "há 5 min",  "text-blue-600"),
    ("💳", "Pagamento recebido",  "há 12 min", "text-emerald-600"),
    ("📦", "Pedido enviado",      "há 28 min", "text-orange-500"),
    ("⚠️", "Estoque baixo",       "há 1h",     "text-red-500"),
]


def overview_view(store) -> Column:
    root = Column(class_="flex flex-col bg-gray-50 min-h-screen")

    header = Container(class_="px-4 pt-10 pb-4 bg-white shadow-sm")
    header.add(Text("📊 Dashboard", class_="text-2xl font-bold text-gray-900"))
    header.add(Text("Visão geral de hoje", class_="text-sm text-gray-500 mt-1"))
    root.add(header)

    content = ScrollView(class_="flex flex-col flex-1 px-4 py-4 space-y-4")

    row1 = Row(class_="flex flex-row gap-3")
    row1.add(stat_card("Usuários",  "1.247",   "12%", True,  "👥"))
    row1.add(stat_card("Receita",   "R$8.432", "8%",  True,  "💰"))
    content.add(row1)

    row2 = Row(class_="flex flex-row gap-3")
    row2.add(stat_card("Pedidos",       "184", "5%", True,  "🛒"))
    row2.add(stat_card("Cancelamentos", "12",  "3%", False, "❌"))
    content.add(row2)

    activity = Card(class_="bg-white rounded-xl p-4 shadow-sm border border-gray-100")
    activity.add(Text("Atividade Recente", class_="text-base font-semibold text-gray-900 mb-3"))
    for icon, title, time, color in _ACTIVITIES:
        item = Row(class_="flex flex-row items-center justify-between py-2 border-b border-gray-50")
        left = Row(class_="flex flex-row items-center gap-3")
        left.add(Text(icon,  class_="text-xl"))
        left.add(Text(title, class_=f"text-sm font-medium {color}"))
        item.add(left)
        item.add(Text(time, class_="text-xs text-gray-400"))
        activity.add(item)
    content.add(activity)

    root.add(content)
    root.add(_nav_bar(store.current_tab))
    return root


def _nav_bar(current: str) -> Row:
    tabs = [("overview", "🏠", "Visão Geral"), ("reports", "📈", "Relatórios"), ("settings", "⚙️", "Config")]
    bar = Row(class_="flex flex-row border-t border-gray-200 bg-white")
    for key, icon, label in tabs:
        active = current == key
        bar.add(Button(
            f"{icon} {label}",
            class_=f"flex-1 py-3 text-xs font-medium {'text-blue-600 bg-blue-50' if active else 'text-gray-400'}",
            on_click="nav_tab", on_click_args=[key],
        ))
    return bar`,

  "components/stat_card.py": `from p2m.ui import Card, Row, Text, Badge


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
    return card`,
};

// ─────────────────────────────────────────────────────────────────────────────
// iFood App
// ─────────────────────────────────────────────────────────────────────────────

const ifoodFiles = {
  "main.py": `from pathlib import Path
from p2m.core import Render, events
from p2m.i18n import configure, set_locale

_APP_DIR = Path(__file__).parent
configure(str(_APP_DIR / "locales"), default_locale="pt")

from state.store import store, RESTAURANTS
from views.home import home_view


def select_category(cat: str):
    store.selected_category = cat

def open_restaurant(restaurant_id):
    store.selected_restaurant_id = int(restaurant_id)
    store.modal_visible = True

def close_modal():
    store.modal_visible = False
    store.selected_restaurant_id = None

def add_to_cart(item_id):
    item_id = int(item_id)
    item_data = None
    for restaurant in RESTAURANTS:
        for menu_item in restaurant["menu"]:
            if menu_item["id"] == item_id:
                item_data = menu_item
                break
        if item_data:
            break
    if item_data is None:
        return
    for cart_item in store.cart:
        if cart_item["id"] == item_id:
            cart_item["qty"] += 1
            store.cart = list(store.cart)
            return
    store.cart = store.cart + [{"id": item_id, "name": item_data["name"],
                                 "price": item_data["price"], "qty": 1,
                                 "emoji": item_data["emoji"]}]

def clear_cart():
    store.cart = []

def switch_locale(locale: str):
    set_locale(locale)
    store.locale = locale


events.register("select_category", select_category)
events.register("open_restaurant", open_restaurant)
events.register("close_modal",     close_modal)
events.register("add_to_cart",     add_to_cart)
events.register("clear_cart",      clear_cart)
events.register("switch_locale",   switch_locale)


def create_view():
    return home_view()

def main():
    Render.execute(create_view)`,

  "state/store.py": `from p2m.core.state import AppState

RESTAURANTS = [
    {"id": 1, "name": "Domino's Pizza", "category": "pizza",   "rating": 4.7,
     "delivery_time": 30, "delivery_fee": 5.99, "emoji": "🍕",
     "menu": [{"id": 1, "name": "Pepperoni Grande", "price": 42.90, "emoji": "🍕"},
              {"id": 2, "name": "Quatro Queijos",   "price": 38.90, "emoji": "🧀"},
              {"id": 3, "name": "Portuguesa",        "price": 36.90, "emoji": "🫒"}]},
    {"id": 2, "name": "Sushi Nagoya",   "category": "sushi",   "rating": 4.9,
     "delivery_time": 45, "delivery_fee": 8.00,  "emoji": "🍣",
     "menu": [{"id": 4, "name": "Combo 30 peças",  "price": 89.90, "emoji": "🍱"},
              {"id": 5, "name": "Temaki de Salmão", "price": 29.90, "emoji": "🌯"},
              {"id": 6, "name": "Uramaki Crispy",   "price": 34.90, "emoji": "🍙"}]},
    {"id": 3, "name": "Bob's Burger",   "category": "burger",  "rating": 4.5,
     "delivery_time": 25, "delivery_fee": 4.99,  "emoji": "🍔",
     "menu": [{"id": 7, "name": "Classic Smash",      "price": 32.90, "emoji": "🍔"},
              {"id": 8, "name": "BBQ Bacon",           "price": 36.90, "emoji": "🥓"},
              {"id": 9, "name": "Batata Frita Grande", "price": 14.90, "emoji": "🍟"}]},
    {"id": 4, "name": "Taco Loco",      "category": "tacos",   "rating": 4.6,
     "delivery_time": 35, "delivery_fee": 6.50,  "emoji": "🌮",
     "menu": [{"id": 10, "name": "Combo 3 Tacos",   "price": 39.90, "emoji": "🌮"},
              {"id": 11, "name": "Burrito Carnitas", "price": 28.90, "emoji": "🌯"},
              {"id": 12, "name": "Nachos Supreme",   "price": 22.90, "emoji": "🧆"}]},
    {"id": 5, "name": "Açaí do Parque", "category": "dessert", "rating": 4.8,
     "delivery_time": 20, "delivery_fee": 3.99,  "emoji": "🍧",
     "menu": [{"id": 13, "name": "Açaí 500ml",          "price": 18.90, "emoji": "🫐"},
              {"id": 14, "name": "Açaí 700ml c/ frutas", "price": 26.90, "emoji": "🍓"},
              {"id": 15, "name": "Smoothie Açaí",        "price": 15.90, "emoji": "🥤"}]},
]

store = AppState(
    selected_category="all",
    selected_restaurant_id=None,
    modal_visible=False,
    cart=[],
    locale="pt",
)`,

  "views/home.py": `from p2m.ui import Column, Row, Text, Input, ScrollView
from p2m.i18n import t
from state.store import store, RESTAURANTS
from components.header           import header
from components.category_carousel import category_carousel
from components.restaurant_card  import restaurant_card
from components.restaurant_modal import restaurant_modal
from components.cart_bar         import cart_bar


def home_view():
    root = Column(class_="bg-gray-50 min-h-screen")

    root.add(header())

    search_row = Row(class_="px-4 py-3")
    search_row.add(Input(placeholder=t("search_placeholder"), class_="bg-white rounded-xl shadow-sm"))
    root.add(search_row)

    root.add(category_carousel(store.selected_category))

    root.add(Text(t("nearby_restaurants"), class_="text-gray-800 font-bold text-lg px-4 pt-2 pb-1"))

    for r in RESTAURANTS:
        if store.selected_category == "all" or r["category"] == store.selected_category:
            root.add(restaurant_card(r))

    if store.cart:
        root.add(cart_bar(store.cart))

    restaurant = next((r for r in RESTAURANTS if r["id"] == store.selected_restaurant_id), None)
    root.add(restaurant_modal(restaurant, store.modal_visible))

    return root.build()`,

  "components/header.py": `from p2m.ui import Row, Image, Button
from p2m.i18n import t


def header():
    row = Row(class_="bg-white px-4 py-3 shadow-sm items-center justify-between")
    row.add(Image(src="assets/logo.svg", alt=t("app_name"), class_="h-8"))

    locale_row = Row(class_="gap-2")
    locale_row.add(Button("PT", class_="bg-orange-500 text-white text-xs px-3 py-1 rounded-full",
                           on_click="switch_locale", on_click_args=["pt"]))
    locale_row.add(Button("EN", class_="bg-gray-200 text-gray-700 text-xs px-3 py-1 rounded-full",
                           on_click="switch_locale", on_click_args=["en"]))
    row.add(locale_row)
    return row`,

  "components/category_carousel.py": `from p2m.ui import Carousel, Button
from p2m.i18n import t

CATEGORIES = [
    ("all",     "category_all"),
    ("pizza",   "category_pizza"),
    ("sushi",   "category_sushi"),
    ("burger",  "category_burger"),
    ("tacos",   "category_tacos"),
    ("dessert", "category_dessert"),
]


def category_carousel(selected: str):
    carousel = Carousel(class_="px-4 py-2 gap-2")
    for cat_key, i18n_key in CATEGORIES:
        is_active = cat_key == selected
        cls = (
            "bg-orange-500 text-white text-sm px-4 py-2 rounded-full flex-shrink-0"
            if is_active
            else "bg-white text-gray-600 text-sm px-4 py-2 rounded-full shadow-sm flex-shrink-0"
        )
        carousel.add(Button(t(i18n_key), class_=cls,
                            on_click="select_category", on_click_args=[cat_key]))
    return carousel`,

  "components/restaurant_modal.py": `from p2m.ui import Modal, Column, Row, Text, Button
from p2m.i18n import t


def restaurant_modal(restaurant, visible: bool):
    modal = Modal(
        visible=visible,
        class_="fixed inset-0 z-50 flex items-end justify-center",
        style="background-color:rgba(0,0,0,0.5);",
    )

    if not visible or not restaurant:
        return modal  # display:none applied by render engine

    sheet = Column(class_="bg-white rounded-t-2xl w-full", style="max-height:75vh;overflow-y:auto;")

    header_row = Row(class_="px-4 pt-4 pb-2 items-center justify-between")
    header_row.add(Text(f"{restaurant['emoji']}  {restaurant['name']}",
                        class_="font-bold text-gray-800 text-lg"))
    header_row.add(Button("✕", class_="text-gray-500 text-xl", on_click="close_modal"))
    sheet.add(header_row)

    sheet.add(Text(t("menu"), class_="font-bold text-gray-800 text-base px-4 pb-2"))

    for item in restaurant.get("menu", []):
        item_row = Row(class_="px-4 py-2 items-center justify-between border-b border-gray-100")
        left = Column(class_="")
        left.add(Text(f"{item['emoji']} {item['name']}", class_="text-gray-800 text-sm font-medium"))
        left.add(Text(f"R$ {item['price']:.2f}", class_="text-orange-500 text-sm font-bold"))
        item_row.add(left)
        item_row.add(Button(t("add"), class_="bg-orange-500 text-white text-xs font-bold px-3 py-1 rounded-full",
                            on_click="add_to_cart", on_click_args=[item["id"]]))
        sheet.add(item_row)

    modal.add(sheet)
    return modal`,
};

// ─────────────────────────────────────────────────────────────────────────────
// App component
// ─────────────────────────────────────────────────────────────────────────────

type AppKey = "todo" | "ecommerce" | "dashboard" | "ifood";

const appMeta: Record<AppKey, { icon: string; en: string; pt: string; files: Record<string, string>; badge?: { en: string; pt: string } }> = {
  todo: {
    icon: "📋",
    en: "Todo App",
    pt: "Todo App",
    files: todoFiles,
  },
  ecommerce: {
    icon: "🛍️",
    en: "E-commerce",
    pt: "E-commerce",
    files: ecommerceFiles,
  },
  dashboard: {
    icon: "📊",
    en: "Dashboard",
    pt: "Dashboard",
    files: dashboardFiles,
  },
  ifood: {
    icon: "🍔",
    en: "iFood-style",
    pt: "iFood",
    files: ifoodFiles,
    badge: { en: "Advanced", pt: "Avançado" },
  },
};

const appDescriptions: Record<AppKey, { en: string; pt: string }> = {
  todo: {
    en: "Multi-screen task manager with global state, per-item event handlers, and bottom navigation.",
    pt: "Gerenciador de tarefas multi-telas com estado global, event handlers por item e navegação inferior.",
  },
  ecommerce: {
    en: "4-screen store with product catalog, search, cart with qty controls, and checkout flow.",
    pt: "Loja com 4 telas: catálogo de produtos, busca, carrinho com controle de quantidade e checkout.",
  },
  dashboard: {
    en: "Analytics dashboard with 3 tabs, stat cards, activity feed, and boolean toggles.",
    pt: "Dashboard analytics com 3 abas, cards de estatísticas, feed de atividades e toggles.",
  },
  ifood: {
    en: "Food delivery app with Carousel, Modal, i18n (pt/en), static assets, and in-app tests.",
    pt: "App de delivery com Carousel, Modal, i18n (pt/en), assets estáticos e testes integrados.",
  },
};

export default function AdvancedExamples() {
  const { language } = useLanguage();
  const isPortuguese = language === "pt";
  const [activeApp, setActiveApp] = useState<AppKey>("todo");

  const app = appMeta[activeApp];
  const desc = appDescriptions[activeApp];
  const fileNames = Object.keys(app.files);
  const [activeFile, setActiveFile] = useState(fileNames[0]);

  const handleAppChange = (val: string) => {
    const key = val as AppKey;
    setActiveApp(key);
    setActiveFile(Object.keys(appMeta[key].files)[0]);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold text-foreground mb-4">
          {isPortuguese ? "Exemplos Avançados" : "Advanced Examples"}
        </h1>
        <p className="text-lg text-muted-foreground">
          {isPortuguese
            ? "Aplicações reais de tests-p2m/ com múltiplas telas, estado e componentes"
            : "Real apps from tests-p2m/ with multiple screens, state, and components"}
        </p>
      </div>

      {/* App selector */}
      <Tabs value={activeApp} onValueChange={handleAppChange}>
        <TabsList className="h-auto flex flex-wrap gap-1 p-1">
          {(Object.keys(appMeta) as AppKey[]).map((key) => {
            const m = appMeta[key];
            return (
              <TabsTrigger key={key} value={key} className="px-4 py-2 text-sm">
                {m.icon} {isPortuguese ? m.pt : m.en}
                {m.badge && (
                  <span className="ml-2 text-xs bg-orange-100 text-orange-700 px-1.5 py-0.5 rounded-full">
                    {isPortuguese ? m.badge.pt : m.badge.en}
                  </span>
                )}
              </TabsTrigger>
            );
          })}
        </TabsList>

        {(Object.keys(appMeta) as AppKey[]).map((key) => (
          <TabsContent key={key} value={key}>
            {/* App description */}
            <Card className="p-5 mb-4 bg-slate-50">
              <p className="text-muted-foreground text-sm">
                {isPortuguese ? appDescriptions[key].pt : appDescriptions[key].en}
              </p>
            </Card>

            {/* File tabs */}
            <Tabs
              value={activeFile}
              onValueChange={setActiveFile}
            >
              <TabsList className="h-auto flex flex-wrap gap-1 p-1 mb-0">
                {Object.keys(appMeta[key].files).map((fname) => (
                  <TabsTrigger key={fname} value={fname} className="px-3 py-1 text-xs font-mono">
                    {fname}
                  </TabsTrigger>
                ))}
              </TabsList>

              {Object.entries(appMeta[key].files).map(([fname, code]) => (
                <TabsContent key={fname} value={fname} className="mt-0">
                  <CodeBlock code={code} language="python" filename={fname} />
                </TabsContent>
              ))}
            </Tabs>
          </TabsContent>
        ))}
      </Tabs>
    </div>
  );
}
