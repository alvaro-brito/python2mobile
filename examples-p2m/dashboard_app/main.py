"""Dashboard App — P2M demo.

An analytics dashboard with three tabs (overview, reports, settings)
and preference toggles, demonstrating navigation and boolean state.
"""
from p2m.core import Render, events
from state.store import store


# ──────────────────────────────────────────────────────────────────────────────
# Event handlers
# ──────────────────────────────────────────────────────────────────────────────

def nav_tab(tab: str):
    """Switch the active dashboard tab."""
    store.current_tab = tab


def toggle_notifications():
    """Toggle the notifications preference."""
    store.notifications_enabled = not store.notifications_enabled


def toggle_dark_mode():
    """Toggle the dark-mode preference."""
    store.dark_mode = not store.dark_mode


events.register("nav_tab",               nav_tab)
events.register("toggle_notifications",  toggle_notifications)
events.register("toggle_dark_mode",      toggle_dark_mode)


# ──────────────────────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────────────────────

def create_view():
    if store.current_tab == "reports":
        from views.reports import reports_view
        return reports_view(store).build()
    elif store.current_tab == "settings":
        from views.settings import settings_view
        return settings_view(store).build()
    else:
        from views.overview import overview_view
        return overview_view(store).build()


def main():
    Render.execute(create_view)


if __name__ == "__main__":
    main()
