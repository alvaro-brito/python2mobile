from p2m.core.state import AppState

RESTAURANTS = [
    {
        "id": 1,
        "name": "Domino's Pizza",
        "category": "pizza",
        "rating": 4.7,
        "delivery_time": 30,
        "delivery_fee": 5.99,
        "emoji": "🍕",
        "menu": [
            {"id": 1, "name": "Pepperoni Grande", "price": 42.90, "emoji": "🍕"},
            {"id": 2, "name": "Quatro Queijos",   "price": 38.90, "emoji": "🧀"},
            {"id": 3, "name": "Portuguesa",        "price": 36.90, "emoji": "🫒"},
        ],
    },
    {
        "id": 2,
        "name": "Sushi Nagoya",
        "category": "sushi",
        "rating": 4.9,
        "delivery_time": 45,
        "delivery_fee": 8.00,
        "emoji": "🍣",
        "menu": [
            {"id": 4, "name": "Combo 30 peças",   "price": 89.90, "emoji": "🍱"},
            {"id": 5, "name": "Temaki de Salmão",  "price": 29.90, "emoji": "🌯"},
            {"id": 6, "name": "Uramaki Crispy",    "price": 34.90, "emoji": "🍙"},
        ],
    },
    {
        "id": 3,
        "name": "Bob's Burger",
        "category": "burger",
        "rating": 4.5,
        "delivery_time": 25,
        "delivery_fee": 4.99,
        "emoji": "🍔",
        "menu": [
            {"id": 7,  "name": "Classic Smash",     "price": 32.90, "emoji": "🍔"},
            {"id": 8,  "name": "BBQ Bacon",          "price": 36.90, "emoji": "🥓"},
            {"id": 9,  "name": "Batata Frita Grande", "price": 14.90, "emoji": "🍟"},
        ],
    },
    {
        "id": 4,
        "name": "Taco Loco",
        "category": "tacos",
        "rating": 4.6,
        "delivery_time": 35,
        "delivery_fee": 6.50,
        "emoji": "🌮",
        "menu": [
            {"id": 10, "name": "Combo 3 Tacos",    "price": 39.90, "emoji": "🌮"},
            {"id": 11, "name": "Burrito Carnitas",  "price": 28.90, "emoji": "🌯"},
            {"id": 12, "name": "Nachos Supreme",    "price": 22.90, "emoji": "🧆"},
        ],
    },
    {
        "id": 5,
        "name": "Açaí do Parque",
        "category": "dessert",
        "rating": 4.8,
        "delivery_time": 20,
        "delivery_fee": 3.99,
        "emoji": "🍧",
        "menu": [
            {"id": 13, "name": "Açaí 500ml",        "price": 18.90, "emoji": "🫐"},
            {"id": 14, "name": "Açaí 700ml c/ frutas", "price": 26.90, "emoji": "🍓"},
            {"id": 15, "name": "Smoothie Açaí",     "price": 15.90, "emoji": "🥤"},
        ],
    },
]

store = AppState(
    selected_category="all",
    selected_restaurant_id=None,
    modal_visible=False,
    cart=[],
    locale="pt",
)
