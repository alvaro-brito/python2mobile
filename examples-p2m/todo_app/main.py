"""
Todo App — Entry point
Screens: Home (active todos) | Done (completed) | Stats
"""
from p2m.core import Render, events
from p2m.ui import Container, Column
from state.store import store
from components.nav_bar import nav_bar


# ------------------------------------------------------------------ #
# Event Handlers
# ------------------------------------------------------------------ #

def update_input(value: str):
    """Sync text input with state."""
    store.input_text = value


def add_todo():
    """Add new task from input."""
    text = store.input_text.strip()
    if text:
        store.todos.append({"id": store.next_id, "text": text, "done": False})
        store.next_id += 1
        store.input_text = ""


def clear_done():
    """Remove all completed tasks."""
    store.todos[:] = [t for t in store.todos if not t["done"]]


def nav_go(screen: str):
    """Switch active screen."""
    store.current_screen = screen


# Register global handlers
events.register("update_input", update_input)
events.register("add_todo", add_todo)
events.register("clear_done", clear_done)
events.register("nav_go", nav_go)


# ------------------------------------------------------------------ #
# View
# ------------------------------------------------------------------ #

def create_view():
    from views.home import home_view
    from views.done import done_view
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
    Render.execute(create_view)


if __name__ == "__main__":
    main()
