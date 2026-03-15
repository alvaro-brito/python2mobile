# ── Static data for the Veloce ride-hailing demo ─────────────────────────────

DRIVERS_NEARBY = [
    {
        "id": "d1", "lat": -23.5590, "lng": -46.6540,
        "title": "Carlos M.",
        "description": "Toyota Corolla · ★ 4.9",
        "color": "blue",
        "car": "Toyota Corolla", "plate": "ABC-1D34", "rating": 4.9, "eta": 3,
    },
    {
        "id": "d2", "lat": -23.5650, "lng": -46.6600,
        "title": "Ana P.",
        "description": "Honda Civic · ★ 4.8",
        "color": "blue",
        "car": "Honda Civic", "plate": "DEF-5E78", "rating": 4.8, "eta": 5,
    },
    {
        "id": "d3", "lat": -23.5570, "lng": -46.6480,
        "title": "Marcos R.",
        "description": "VW Jetta · ★ 4.7",
        "color": "blue",
        "car": "VW Jetta", "plate": "GHI-9F12", "rating": 4.7, "eta": 7,
    },
    {
        "id": "d4", "lat": -23.5630, "lng": -46.6620,
        "title": "Júlia S.",
        "description": "Hyundai HB20 · ★ 4.9",
        "color": "blue",
        "car": "Hyundai HB20", "plate": "JKL-3G56", "rating": 4.9, "eta": 4,
    },
    {
        "id": "d5", "lat": -23.5555, "lng": -46.6555,
        "title": "Roberto F.",
        "description": "Nissan Sentra · ★ 4.6",
        "color": "blue",
        "car": "Nissan Sentra", "plate": "MNO-7H90", "rating": 4.6, "eta": 6,
    },
]

POPULAR_DESTINATIONS = [
    {
        "label": "🏛️  Sé Cathedral",
        "address": "Praça da Sé — São Paulo",
        "lat": -23.5475, "lng": -46.6361,
    },
    {
        "label": "🌿  Ibirapuera Park",
        "address": "Parque Ibirapuera — São Paulo",
        "lat": -23.5874, "lng": -46.6576,
    },
    {
        "label": "✈️  GRU Airport",
        "address": "Rod. Hélio Smidt — Guarulhos",
        "lat": -23.4356, "lng": -46.4731,
    },
    {
        "label": "🛍️  Shopping JK",
        "address": "Av. Juscelino Kubitschek — SP",
        "lat": -23.5965, "lng": -46.6753,
    },
    {
        "label": "🍺  Vila Madalena",
        "address": "Vila Madalena — São Paulo",
        "lat": -23.5536, "lng": -46.6917,
    },
]

TRIP_HISTORY = [
    {
        "id": "t1",
        "origin": "Av. Paulista, 1000",
        "destination": "Sé Cathedral",
        "date": "Mar 14",
        "fare": 18.50,
        "type": "Comfort",
        "duration": "12 min",
        "rating": 5,
    },
    {
        "id": "t2",
        "origin": "Parque Ibirapuera",
        "destination": "Av. Paulista, 1000",
        "date": "Mar 12",
        "fare": 12.90,
        "type": "Economy",
        "duration": "18 min",
        "rating": 4,
    },
    {
        "id": "t3",
        "origin": "GRU Airport",
        "destination": "Av. Paulista, 1800",
        "date": "Mar 10",
        "fare": 67.50,
        "type": "Premium",
        "duration": "45 min",
        "rating": 5,
    },
    {
        "id": "t4",
        "origin": "Shopping JK Iguatemi",
        "destination": "Vila Madalena",
        "date": "Mar 8",
        "fare": 15.30,
        "type": "Economy",
        "duration": "22 min",
        "rating": 4,
    },
]

RIDE_OPTIONS = [
    {
        "type": "economy",
        "name": "Economy",
        "emoji": "🚗",
        "description": "Affordable everyday rides",
        "eta": 5,
        "fare_key": "fare_economy",
    },
    {
        "type": "comfort",
        "name": "Comfort",
        "emoji": "🚙",
        "description": "Spacious sedans with A/C",
        "eta": 4,
        "fare_key": "fare_comfort",
    },
    {
        "type": "premium",
        "name": "Premium",
        "emoji": "🚐",
        "description": "Luxury vehicles, top drivers",
        "eta": 6,
        "fare_key": "fare_premium",
    },
]
