"""Login App — P2M demo.

Demonstrates form inputs, validation, authentication flow, and
conditional rendering based on authentication state.
"""
from p2m.core import Render, events
from state.store import store


# Hardcoded user registry  {email: (password, display_name)}
_USERS = {
    "admin@p2m.dev": ("123456", "Admin"),
    "user@test.com":  ("abcdef", "João Silva"),
}


# ──────────────────────────────────────────────────────────────────────────────
# Event handlers
# ──────────────────────────────────────────────────────────────────────────────

def update_email(value: str):
    store.email = value
    store.error = ""


def update_password(value: str):
    store.password = value
    store.error = ""


def do_login():
    email    = store.email.strip()
    password = store.password

    if not email or not password:
        store.error = "Preencha e-mail e senha."
        return

    user_data = _USERS.get(email)
    if user_data is None:
        store.error = "E-mail não encontrado."
        return

    valid_pw, name = user_data
    if password != valid_pw:
        store.error = "Senha incorreta."
        return

    store.error       = ""
    store.logged_user = name
    store.current_screen = "home"


def do_logout():
    store.email          = ""
    store.password       = ""
    store.error          = ""
    store.logged_user    = None
    store.current_screen = "login"


events.register("update_email",    update_email)
events.register("update_password", update_password)
events.register("do_login",        do_login)
events.register("do_logout",       do_logout)


# ──────────────────────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────────────────────

def create_view():
    if store.current_screen == "home":
        from views.home import home_view
        return home_view(store).build()
    else:
        from views.login import login_view
        return login_view(store).build()


def main():
    Render.execute(create_view)


if __name__ == "__main__":
    main()
