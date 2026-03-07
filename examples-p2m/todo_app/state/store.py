"""Todo App - Global state store (singleton)"""
from p2m.core.state import AppState

store = AppState(
    todos=[
        {"id": 1, "text": "Estudar Python2Mobile", "done": False},
        {"id": 2, "text": "Criar primeiro app mobile", "done": True},
        {"id": 3, "text": "Publicar na App Store", "done": False},
    ],
    next_id=4,
    input_text="",
    current_screen="home",   # home | done | stats
)
