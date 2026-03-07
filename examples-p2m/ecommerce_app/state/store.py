"""Ecommerce App - State store"""
from p2m.core.state import AppState

PRODUCTS = [
    {"id": 1, "name": "Tênis Air Max",  "price": 299.90, "emoji": "👟", "cat": "Calçados", "stock": 5},
    {"id": 2, "name": "Camisa Polo",    "price":  89.90, "emoji": "👕", "cat": "Roupas",   "stock": 12},
    {"id": 3, "name": "Mochila Slim",   "price": 149.90, "emoji": "🎒", "cat": "Acessórios","stock": 3},
    {"id": 4, "name": "Óculos Aviador", "price": 199.90, "emoji": "🕶️", "cat": "Acessórios","stock": 8},
    {"id": 5, "name": "Relógio Sport",  "price": 449.90, "emoji": "⌚", "cat": "Acessórios","stock": 2},
]

store = AppState(
    products=PRODUCTS,
    cart=[],                # [{"product_id": int, "qty": int}]
    current_screen="catalog",  # catalog | cart | checkout | confirm
    selected_product_id=None,
    search_query="",
    checkout_name="",
    checkout_email="",
)
