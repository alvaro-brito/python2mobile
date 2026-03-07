from p2m.core.state import AppState

store = AppState(
    current_screen="login",
    email="",
    password="",
    error="",
    logged_user=None,
)
