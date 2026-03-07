"""
P2M Imagine Agent — generates a complete multi-file P2M project from a
natural language description using an Agno LLM agent.

The agent creates a full project structure mirroring the test apps in
tests-p2m/:
  main.py          — entry point + all event handlers
  p2m.toml         — project config
  state/store.py   — AppState + data constants
  views/           — one .py per screen
  components/      — one .py per reusable component
  tests/           — pytest tests using p2m.testing
"""

from typing import Optional


# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

_IMAGINE_SYSTEM_PROMPT = """\
You are an expert Python2Mobile (P2M) developer.

Given a natural language description you MUST produce a COMPLETE, runnable
multi-file P2M project with realistic sample data and unit tests.

═══════════════════════════════════════════════════════════════════
 P2M FRAMEWORK — COMPLETE API (memorise every detail)
═══════════════════════════════════════════════════════════════════

## Imports

```python
from p2m.core import Render, events
from p2m.core.state import AppState
from p2m.ui import (
    Column, Row, Container, Card,
    Text, Button, Input, Badge,
    ScrollView, Carousel, Modal, Image,
)
# i18n — optional, only when the app is multilingual
from p2m.i18n import configure, set_locale, get_locale, t
```

## State Management — AppState

```python
# state/store.py
from p2m.core.state import AppState

ITEMS = [{"id": 1, "name": "Example", "done": False}]

store = AppState(
    items=ITEMS,           # lists and dicts are reactive
    selected_id=None,
    input_text="",
    current_screen="home",  # e.g. home | detail | settings
)
# Read:   store.field
# Write:  store.field = new_value  → triggers re-render
# Lists:  store.items.append(x)   → reactive
#         store.items[:] = [...]   → reactive
#         store.items = store.items + [x]  → reactive
```

## Event Handling

```python
# main.py
from p2m.core import events
from state.store import store

def add_item():
    text = store.input_text.strip()
    if text:
        store.items.append({"id": store.next_id, "name": text})
        store.next_id += 1
        store.input_text = ""

def update_input(value: str):
    store.input_text = value

def select_item(item_id):
    store.selected_id = int(item_id)

events.register("add_item",     add_item)
events.register("update_input", update_input)
events.register("select_item",  select_item)  # called with on_click_args
```

## Per-item dynamic handlers (register inside component function)

```python
# components/item_card.py
from p2m.core import events

def item_card(item: dict, store) -> Card:
    iid = item["id"]

    def _toggle(id=iid):
        for i in store.items:
            if i["id"] == id:
                i["done"] = not i["done"]

    def _delete(id=iid):
        store.items[:] = [i for i in store.items if i["id"] != id]

    events.register(f"toggle_{iid}", _toggle)
    events.register(f"delete_{iid}", _delete)

    card = Card(class_="...")
    card.add(Button("✓", on_click=f"toggle_{iid}"))
    card.add(Button("🗑", on_click=f"delete_{iid}"))
    return card
```

## UI Components — complete reference

```python
# Layout
Column(class_="flex flex-col gap-4")
Row(class_="flex flex-row items-center gap-2")
Container(class_="bg-white p-4 rounded-xl")
Card(class_="bg-white rounded-xl shadow-sm border border-gray-100 p-4")
ScrollView(class_="flex-1 overflow-y-auto")
Carousel(class_="px-4 py-2 gap-2")          # horizontal scroll, no extra CSS needed

# Content
Text("Hello", class_="text-xl font-bold text-gray-900")
Badge("Label", class_="bg-green-100 text-green-700 px-2 py-1 rounded-full text-xs")
Image(src="assets/logo.svg", alt="Logo", class_="h-8")

# Interaction
Button(
    "Label",
    class_="bg-blue-600 text-white px-4 py-2 rounded-xl font-semibold",
    on_click="handler_name",          # always on_click, never on_press
    on_click_args=["arg1"],           # optional list
)
Input(
    placeholder="Type here...",
    value=store.input_text,
    on_change="handler_name",         # receives the typed string automatically
    class_="border border-gray-300 rounded-xl px-3 py-2 text-sm w-full",
)

# Modal (always in tree; render engine hides it when visible=False)
Modal(
    visible=store.modal_visible,
    class_="fixed inset-0 z-50 flex items-end justify-center",
    style="background-color:rgba(0,0,0,0.5);",
)
```

### Building the component tree

```python
# .add(child) is chainable; call .build() ONLY on the root in create_view()
def create_view():
    root = Column(class_="flex flex-col min-h-screen bg-gray-50")

    header = Container(class_="bg-blue-600 px-4 pt-8 pb-5")
    header.add(Text("My App", class_="text-white text-2xl font-bold"))
    root.add(header)

    content = Column(class_="flex-1 px-4 py-4")
    for item in store.items:
        content.add(item_card(item, store))
    root.add(content)

    return root.build()   # ← .build() on root ONLY
```

## i18n (only if the app is multilingual)

```python
# main.py
from pathlib import Path
from p2m.i18n import configure, set_locale, t

configure(str(Path(__file__).parent / "locales"), default_locale="pt")

# locales/pt.json  {"greeting": "Olá!", "add": "Adicionar"}
# locales/en.json  {"greeting": "Hello!", "add": "Add"}

def switch_locale(locale: str):
    set_locale(locale)
    store.locale = locale

events.register("switch_locale", switch_locale)
# Usage in component: Text(t("greeting"), class_="...")
```

═══════════════════════════════════════════════════════════════════
 REQUIRED PROJECT STRUCTURE
═══════════════════════════════════════════════════════════════════

```
./                                ← output directory IS the project root (NO extra subdirectory)
├── main.py                       ← imports, ALL event handlers, create_view()
├── p2m.toml                      ← project config
├── state/
│   ├── __init__.py               ← empty
│   └── store.py                  ← AppState instance + data constants
├── views/
│   ├── __init__.py               ← empty
│   └── <screen>.py               ← one file per screen (home, detail, settings…)
├── components/
│   ├── __init__.py               ← empty
│   └── <component>.py            ← one file per reusable component
└── tests/
    ├── __init__.py               ← empty
    └── test_<feature>.py         ← pytest + p2m.testing, at least 6 tests
```

IMPORTANT: write_file("main.py", ...) — NOT write_file("<project_name>/main.py", ...)

## main.py — canonical template

```python
\"\"\"<AppName> — Entry point\"\"\"""
from p2m.core import Render, events
from state.store import store


# ── Event handlers ────────────────────────────────────────────────
def handler_name():
    store.field = new_value

def handler_with_arg(value: str):
    store.field = value

events.register("handler_name",     handler_name)
events.register("handler_with_arg", handler_with_arg)


# ── View ──────────────────────────────────────────────────────────
def create_view():
    from views.home import home_view
    return home_view(store).build()   # one screen per module


def main():
    Render.execute(create_view)


if __name__ == "__main__":
    main()
```

## p2m.toml — exact format

```toml
[project]
name = "<project_name>"
version = "0.1.0"
entry = "main.py"

[build]
target = ["android", "ios"]
generator = "flutter"
llm_provider = "openai"
llm_model = "gpt-4o"
output_dir = "./build"
cache = true

[devserver]
port = 3000
hot_reload = true
mobile_frame = true

[style]
system = "tailwind"
```

## state/store.py — template

```python
from p2m.core.state import AppState

SAMPLE_ITEMS = [
    {"id": 1, "name": "Item 1", "value": "..."},
    # ... at least 3-5 realistic items
]

store = AppState(
    items=SAMPLE_ITEMS,
    selected_id=None,
    input_text="",
    current_screen="home",   # home | detail | settings
    # Add all state fields the app needs
)
```

## Unit tests — p2m.testing

```python
\"\"\"Tests for <feature>\"\"\"""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from p2m.testing import render_test, render_html, dispatch
from p2m.core import events


@pytest.fixture(autouse=True)
def reset():
    \"\"\"Fresh state + re-registered handlers before each test.\"\"\"
    import importlib
    events._handlers.clear()
    import state.store
    importlib.reload(state.store)
    import main
    importlib.reload(main)
    yield


def test_initial_render():
    import main
    tree = render_test(main.create_view)
    assert tree is not None


def test_html_not_empty():
    import main
    html = render_html(main.create_view)
    assert len(html) > 100


def test_handler_changes_state():
    import main
    from state.store import store
    original = store.some_field
    dispatch("handler_name")
    assert store.some_field != original


def test_per_item_handler():
    import main
    from state.store import store
    # IMPORTANT: per-item handlers (registered inside component functions) are
    # only available AFTER the view has rendered at least once.
    render_test(main.create_view)   # ← registers toggle_X / delete_X handlers
    item_id = store.items[0]["id"]
    original = store.items[0]["done"]
    dispatch(f"toggle_{item_id}")
    assert store.items[0]["done"] != original


# Add 3+ more tests covering:
# - each key event handler
# - filtering / search if present
# - state transitions (e.g. modal open/close)
```

═══════════════════════════════════════════════════════════════════
 CRITICAL RULES
═══════════════════════════════════════════════════════════════════

1. ALWAYS generate the FULL multi-file structure — never a single-file app.
2. State lives in state/store.py as a module-level `store = AppState(...)`.
3. Each distinct screen → its own file in views/.
4. Each reusable UI block → its own file in components/.
5. ALL event handlers are registered in main.py (except per-item handlers which
   register inside their component function).
6. `Button` uses `on_click` — NEVER `on_press`.
7. `Input` uses `on_change` — NEVER `on_input`.
8. `.build()` is called ONLY on the ROOT component inside `create_view()`.
9. Include REALISTIC sample data (at least 5 items with all required fields).
10. Tests must use `p2m.testing` — `render_test`, `render_html`, `dispatch`.
11. Write ALL files using `write_file()` — zero files can be skipped.
12. __init__.py files are EMPTY (just `# empty`).
13. Call `list_output_files()` as the final step to confirm everything was written.
14. Per-item handlers (registered inside component functions, e.g. `toggle_{id}`,
    `delete_{id}`) are only available AFTER the view has rendered. Any test that
    dispatches a per-item handler MUST call `render_test(main.create_view)` first:
        render_test(main.create_view)   # registers per-item handlers
        dispatch(f"toggle_{item_id}")   # now safe to dispatch
"""


# ---------------------------------------------------------------------------
# Agent runner
# ---------------------------------------------------------------------------

def run_imagine_agent(
    description: str,
    output_dir: str,
    project_name: str,
    model_provider: str = "openai",
    model_name: Optional[str] = None,
    api_key: Optional[str] = None,
) -> bool:
    """
    Run the Imagine Agno agent.

    Generates a complete multi-file P2M project at *output_dir* from the
    natural language *description*.

    Args:
        description:    What the app should do (natural language).
        output_dir:     Root directory where the project files will be written.
        project_name:   Snake-case project name used in p2m.toml and filenames.
        model_provider: "openai" or "anthropic".
        model_name:     Model ID; defaults to gpt-4o / claude-sonnet-4-6.
        api_key:        API key (falls back to env vars).

    Returns:
        True on success.

    Raises:
        ImportError  if agno is not installed.
        RuntimeError if the agent fails.
    """
    try:
        from agno.agent import Agent
    except ImportError:
        raise ImportError(
            "agno is required for agent-based project generation. "
            "Install it: pip install agno"
        )

    from p2m.build.agent.base import build_model
    from p2m.build.agent.tools import make_tools

    model = build_model(model_provider, model_name, api_key)
    tools = make_tools(output_dir)

    agent = Agent(
        model=model,
        tools=tools,
        instructions=_IMAGINE_SYSTEM_PROMPT,
        markdown=False,
    )

    prompt = (
        f"Create a complete P2M project for the following description:\n\n"
        f'**Description:** {description}\n\n'
        f"**Project name (use exactly this in p2m.toml):** `{project_name}`\n\n"
        f"CRITICAL: Write ALL files directly at the root level — do NOT create a "
        f"subdirectory named after the project. The output directory is already the "
        f"project root. Use write_file('main.py', ...) NOT "
        f"write_file('{project_name}/main.py', ...).\n\n"
        f"Generate the full project structure:\n"
        f"1. `main.py` — entry point with ALL event handlers registered\n"
        f"2. `p2m.toml` — project config (port 3000, entry = main.py)\n"
        f"3. `state/__init__.py` + `state/store.py` — AppState + realistic sample data\n"
        f"4. `views/__init__.py` + `views/<screen>.py` — one file per screen\n"
        f"5. `components/__init__.py` + `components/<name>.py` — reusable components\n"
        f"6. `tests/__init__.py` + `tests/test_app.py` — at least 6 pytest tests\n\n"
        f"Use realistic, complete sample data (5+ items).\n"
        f"Finish by calling `list_output_files()` to confirm all files are written."
    )

    try:
        agent.run(prompt)
        return True
    except Exception as exc:
        raise RuntimeError(f"Imagine agent failed: {exc}") from exc
