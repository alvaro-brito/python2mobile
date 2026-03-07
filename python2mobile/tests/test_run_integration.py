"""
Integration tests for p2m run behavior.

Tests rendering, event handling, navigation, and state management
using the real test apps from tests-p2m/.

Strategy:
- Load each app in isolation via sys.path manipulation + module cleanup
- Trigger initial render to register per-item event handlers
- Dispatch events and verify state + HTML output
"""

import sys
import importlib
from pathlib import Path
import pytest

# Paths
FRAMEWORK_PATH = Path(__file__).parent.parent
TESTS_P2M_PATH = FRAMEWORK_PATH.parent / "tests-p2m"

if str(FRAMEWORK_PATH) not in sys.path:
    sys.path.insert(0, str(FRAMEWORK_PATH))

from p2m.core import events, Render
from p2m.core.render_engine import RenderEngine


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _render(create_view, mobile_frame: bool = False) -> str:
    """Execute view and render to a full HTML page."""
    tree = Render.execute(create_view)
    return RenderEngine().render(tree, mobile_frame=mobile_frame)


def _render_content(create_view) -> str:
    """Render only the inner content (as WebSocket live-updates do)."""
    tree = Render.execute(create_view)
    return RenderEngine().render_content(tree)


def _load_app(app_dir: Path):
    """
    Load a tests-p2m app module after adding its directory to sys.path.
    Returns the module. Caller is responsible for cleanup.
    """
    sys.modules.pop("main", None)
    return importlib.import_module("main")


# ──────────────────────────────────────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def todo_app():
    """
    Load todo_app in isolation.
    Yields (main_module, store).
    Performs an initial render so per-item handlers (toggle_N, delete_N) are
    registered before any test runs.
    """
    app_dir = TESTS_P2M_PATH / "todo_app"
    saved_path = list(sys.path)
    saved_module_keys = set(sys.modules.keys())
    events.clear()

    sys.path.insert(0, str(app_dir))
    mod = _load_app(app_dir)

    # Initial render registers per-item handlers (toggle_N, delete_N)
    _render(mod.create_view)

    yield mod, mod.store

    # Cleanup: restore sys.path and purge app modules
    for key in list(sys.modules.keys()):
        if key not in saved_module_keys:
            del sys.modules[key]
    sys.path[:] = saved_path
    events.clear()


@pytest.fixture
def ecommerce_app():
    """
    Load ecommerce_app in isolation.
    Yields (main_module, store).
    Performs an initial render so product card handlers (add_to_cart_N) are
    registered before any test runs.
    """
    app_dir = TESTS_P2M_PATH / "ecommerce_app"
    saved_path = list(sys.path)
    saved_module_keys = set(sys.modules.keys())
    events.clear()

    sys.path.insert(0, str(app_dir))
    mod = _load_app(app_dir)

    # Initial render registers add_to_cart_N handlers
    _render(mod.create_view)

    yield mod, mod.store

    for key in list(sys.modules.keys()):
        if key not in saved_module_keys:
            del sys.modules[key]
    sys.path[:] = saved_path
    events.clear()


# ──────────────────────────────────────────────────────────────────────────────
# Todo App — Rendering
# ──────────────────────────────────────────────────────────────────────────────

class TestTodoAppRendering:
    """Initial rendering and HTML structure of the todo app."""

    def test_initial_screen_is_home(self, todo_app):
        """Default screen is 'home'."""
        _, store = todo_app
        assert store.current_screen == "home"

    def test_home_shows_header(self, todo_app):
        """Home screen header with title is rendered."""
        mod, _ = todo_app
        html = _render(mod.create_view)
        assert "📋 Minhas Tarefas" in html

    def test_home_shows_pending_count(self, todo_app):
        """Pending count in header matches active todos (2 of 3 initially)."""
        mod, _ = todo_app
        html = _render(mod.create_view)
        # Initial state: todos 1 and 3 are pending (todo 2 is done)
        assert "2 pendente(s)" in html

    def test_home_shows_active_todos(self, todo_app):
        """Active (not done) todos appear on home screen."""
        mod, _ = todo_app
        html = _render(mod.create_view)
        assert "Estudar Python2Mobile" in html
        assert "Publicar na App Store" in html

    def test_done_todo_hidden_on_home(self, todo_app):
        """Completed todo does NOT appear on home screen active list."""
        mod, _ = todo_app
        html = _render(mod.create_view)
        # Todo 2 "Criar primeiro app mobile" is done=True, should not be in active list
        assert "Criar primeiro app mobile" not in html

    def test_home_has_input_field(self, todo_app):
        """Input for adding new tasks is rendered."""
        mod, _ = todo_app
        html = _render(mod.create_view)
        assert "Nova tarefa..." in html

    def test_home_has_add_button(self, todo_app):
        """Add button triggers 'add_todo' handler."""
        mod, _ = todo_app
        html = _render(mod.create_view)
        assert "add_todo" in html

    def test_nav_bar_present(self, todo_app):
        """Bottom nav bar with all three tabs is rendered."""
        mod, _ = todo_app
        html = _render(mod.create_view)
        assert "Tarefas" in html
        assert "Concluídas" in html
        assert "Stats" in html

    def test_nav_bar_uses_nav_go_handler(self, todo_app):
        """Nav bar buttons dispatch nav_go with screen argument."""
        mod, _ = todo_app
        html = _render(mod.create_view)
        assert "nav_go" in html

    def test_websocket_script_injected(self, todo_app):
        """WebSocket client script is embedded in the page."""
        mod, _ = todo_app
        html = _render(mod.create_view)
        assert "handleClick" in html
        assert "handleChange" in html
        assert "/ws" in html

    def test_mobile_frame_render(self, todo_app):
        """Render with mobile_frame=True produces iPhone wrapper (390×844 px)."""
        mod, _ = todo_app
        html = _render(mod.create_view, mobile_frame=True)
        assert "mobile-frame" in html
        assert "390px" in html
        assert "844px" in html

    def test_render_content_no_page_wrapper(self, todo_app):
        """render_content() returns inner HTML without full page structure."""
        mod, _ = todo_app
        content = _render_content(mod.create_view)
        assert "<!DOCTYPE" not in content
        assert "<html" not in content
        assert "📋 Minhas Tarefas" in content


# ──────────────────────────────────────────────────────────────────────────────
# Todo App — Navigation
# ──────────────────────────────────────────────────────────────────────────────

class TestTodoAppNavigation:
    """Screen navigation via nav_go handler."""

    def test_nav_to_done_screen(self, todo_app):
        """nav_go('done') switches to done screen and shows header."""
        mod, store = todo_app
        events.dispatch("nav_go", "done")
        assert store.current_screen == "done"
        html = _render(mod.create_view)
        assert "✅ Concluídas" in html

    def test_done_screen_shows_completed_todo(self, todo_app):
        """Done screen lists todos that are marked as completed."""
        mod, store = todo_app
        events.dispatch("nav_go", "done")
        html = _render(mod.create_view)
        assert "Criar primeiro app mobile" in html

    def test_done_screen_shows_clear_button(self, todo_app):
        """Done screen shows 'Limpar concluídas' when there are completed todos."""
        mod, store = todo_app
        events.dispatch("nav_go", "done")
        html = _render(mod.create_view)
        assert "Limpar concluídas" in html

    def test_nav_to_stats_screen(self, todo_app):
        """nav_go('stats') switches to stats screen with percentage header."""
        mod, store = todo_app
        events.dispatch("nav_go", "stats")
        assert store.current_screen == "stats"
        html = _render(mod.create_view)
        assert "📊 Estatísticas" in html

    def test_stats_screen_shows_percentages(self, todo_app):
        """Stats screen displays completion percentage and counts."""
        mod, store = todo_app
        events.dispatch("nav_go", "stats")
        html = _render(mod.create_view)
        # 1/3 done = 33%
        assert "33%" in html
        # Stat cards
        assert "Total" in html
        assert "Feitas" in html
        assert "Pendentes" in html

    def test_nav_back_to_home(self, todo_app):
        """After visiting stats, nav_go('home') returns to home screen."""
        mod, store = todo_app
        events.dispatch("nav_go", "stats")
        events.dispatch("nav_go", "home")
        assert store.current_screen == "home"
        html = _render(mod.create_view)
        assert "📋 Minhas Tarefas" in html

    def test_nav_home_to_done_to_stats(self, todo_app):
        """Sequential navigation through all three screens works."""
        mod, store = todo_app
        for screen in ["done", "stats", "home"]:
            events.dispatch("nav_go", screen)
            assert store.current_screen == screen


# ──────────────────────────────────────────────────────────────────────────────
# Todo App — Event Handlers
# ──────────────────────────────────────────────────────────────────────────────

class TestTodoAppEvents:
    """State mutations via event dispatch."""

    def test_update_input_syncs_state(self, todo_app):
        """update_input stores the typed text in store.input_text."""
        _, store = todo_app
        events.dispatch("update_input", "hello world")
        assert store.input_text == "hello world"

    def test_update_input_overwrite(self, todo_app):
        """Multiple update_input calls overwrite previous value."""
        _, store = todo_app
        events.dispatch("update_input", "first")
        events.dispatch("update_input", "second")
        assert store.input_text == "second"

    def test_add_todo_appends_new_item(self, todo_app):
        """Typing text + add_todo appends a new task to store.todos."""
        _, store = todo_app
        initial_count = len(store.todos)
        events.dispatch("update_input", "Aprender testes de integração")
        events.dispatch("add_todo")
        assert len(store.todos) == initial_count + 1
        texts = [t["text"] for t in store.todos]
        assert "Aprender testes de integração" in texts

    def test_add_todo_assigns_new_id(self, todo_app):
        """New todo gets the next sequential id."""
        _, store = todo_app
        events.dispatch("update_input", "Nova tarefa")
        events.dispatch("add_todo")
        new_todo = store.todos[-1]
        assert new_todo["id"] == 4  # initial next_id was 4

    def test_add_todo_clears_input(self, todo_app):
        """After adding a todo, input_text is reset to empty string."""
        _, store = todo_app
        events.dispatch("update_input", "Nova tarefa")
        events.dispatch("add_todo")
        assert store.input_text == ""

    def test_add_todo_empty_input_ignored(self, todo_app):
        """Adding a todo with empty text does not modify the list."""
        _, store = todo_app
        initial_count = len(store.todos)
        events.dispatch("update_input", "   ")
        events.dispatch("add_todo")
        assert len(store.todos) == initial_count

    def test_add_todo_appears_in_html(self, todo_app):
        """New todo is visible in the rendered HTML."""
        mod, store = todo_app
        events.dispatch("update_input", "Tarefa de teste!")
        events.dispatch("add_todo")
        html = _render(mod.create_view)
        assert "Tarefa de teste!" in html

    def test_toggle_todo_marks_done(self, todo_app):
        """toggle_1 flips todo 1 from done=False to done=True."""
        _, store = todo_app
        todo_1 = next(t for t in store.todos if t["id"] == 1)
        assert todo_1["done"] is False
        events.dispatch("toggle_1")
        assert todo_1["done"] is True

    def test_toggle_done_todo_reverts(self, todo_app):
        """toggle_2 flips todo 2 (done=True) back to done=False."""
        mod, store = todo_app
        # Render done screen to register toggle_2 handler
        events.dispatch("nav_go", "done")
        _render(mod.create_view)
        events.dispatch("nav_go", "home")

        todo_2 = next(t for t in store.todos if t["id"] == 2)
        assert todo_2["done"] is True
        events.dispatch("toggle_2")
        assert todo_2["done"] is False

    def test_toggle_affects_pending_count(self, todo_app):
        """After toggling todo 1 as done, pending count drops to 1."""
        mod, _ = todo_app
        events.dispatch("toggle_1")
        html = _render(mod.create_view)
        assert "1 pendente(s)" in html

    def test_toggle_twice_reverts(self, todo_app):
        """Toggling a todo twice returns it to the original state."""
        _, store = todo_app
        todo_1 = next(t for t in store.todos if t["id"] == 1)
        events.dispatch("toggle_1")
        events.dispatch("toggle_1")
        assert todo_1["done"] is False

    def test_delete_removes_from_state(self, todo_app):
        """delete_1 removes todo with id=1 from store.todos."""
        _, store = todo_app
        initial_count = len(store.todos)
        ids_before = [t["id"] for t in store.todos]
        assert 1 in ids_before
        events.dispatch("delete_1")
        assert len(store.todos) == initial_count - 1
        assert 1 not in [t["id"] for t in store.todos]

    def test_delete_removes_from_html(self, todo_app):
        """Deleted todo no longer appears in rendered HTML."""
        mod, _ = todo_app
        events.dispatch("delete_1")
        html = _render(mod.create_view)
        assert "Estudar Python2Mobile" not in html

    def test_delete_nonexistent_no_error(self, todo_app):
        """Deleting a non-existent id is a no-op."""
        _, store = todo_app
        initial_count = len(store.todos)
        events.dispatch("delete_999")
        assert len(store.todos) == initial_count

    def test_clear_done_removes_completed(self, todo_app):
        """clear_done removes all todos marked done=True."""
        _, store = todo_app
        done_before = [t for t in store.todos if t["done"]]
        assert len(done_before) == 1  # todo 2 is done
        events.dispatch("clear_done")
        done_after = [t for t in store.todos if t["done"]]
        assert len(done_after) == 0

    def test_clear_done_keeps_pending(self, todo_app):
        """clear_done does NOT remove active (not done) todos."""
        _, store = todo_app
        events.dispatch("clear_done")
        pending = [t for t in store.todos if not t["done"]]
        assert len(pending) == 2  # todos 1 and 3

    def test_clear_done_empty_list_no_error(self, todo_app):
        """clear_done on a list with no completed todos is a no-op."""
        _, store = todo_app
        events.dispatch("clear_done")
        initial_count = len(store.todos)
        events.dispatch("clear_done")  # second call
        assert len(store.todos) == initial_count

    def test_done_screen_empty_after_clear(self, todo_app):
        """After clear_done, done screen shows empty state."""
        mod, _ = todo_app
        events.dispatch("clear_done")
        events.dispatch("nav_go", "done")
        html = _render(mod.create_view)
        assert "Nenhuma tarefa concluída" in html

    def test_stats_update_after_toggle(self, todo_app):
        """Stats screen reflects updated counts after toggling a todo."""
        mod, _ = todo_app
        # Toggle todos 1 and 3 as done → all 3 done
        events.dispatch("toggle_1")
        events.dispatch("toggle_3")
        events.dispatch("nav_go", "stats")
        html = _render(mod.create_view)
        assert "100%" in html


# ──────────────────────────────────────────────────────────────────────────────
# Ecommerce App — Rendering
# ──────────────────────────────────────────────────────────────────────────────

class TestEcommerceAppRendering:
    """Initial rendering of the ecommerce catalog."""

    def test_initial_screen_is_catalog(self, ecommerce_app):
        """Default screen is 'catalog'."""
        _, store = ecommerce_app
        assert store.current_screen == "catalog"

    def test_catalog_header(self, ecommerce_app):
        """Catalog header shows shop title."""
        mod, _ = ecommerce_app
        html = _render(mod.create_view)
        assert "🛍️ P2M Shop" in html

    def test_all_products_displayed(self, ecommerce_app):
        """All 5 products are listed in the catalog."""
        mod, _ = ecommerce_app
        html = _render(mod.create_view)
        assert "Tênis Air Max" in html
        assert "Camisa Polo" in html
        assert "Mochila Slim" in html
        assert "Óculos Aviador" in html
        assert "Relógio Sport" in html

    def test_product_prices_displayed(self, ecommerce_app):
        """Product prices are rendered."""
        mod, _ = ecommerce_app
        html = _render(mod.create_view)
        assert "299.90" in html
        assert "89.90" in html

    def test_empty_cart_badge(self, ecommerce_app):
        """Cart badge shows 0 items initially."""
        mod, _ = ecommerce_app
        html = _render(mod.create_view)
        assert "🛒 0" in html

    def test_search_input_present(self, ecommerce_app):
        """Search input with placeholder is rendered."""
        mod, _ = ecommerce_app
        html = _render(mod.create_view)
        assert "Buscar produto..." in html

    def test_websocket_script_injected(self, ecommerce_app):
        """WebSocket client script is present in the page."""
        mod, _ = ecommerce_app
        html = _render(mod.create_view)
        assert "handleClick" in html
        assert "handleChange" in html


# ──────────────────────────────────────────────────────────────────────────────
# Ecommerce App — Events & Cart Flow
# ──────────────────────────────────────────────────────────────────────────────

class TestEcommerceAppEvents:
    """Event dispatch, state mutations, cart and checkout flow."""

    def test_search_filters_products(self, ecommerce_app):
        """search_products('Tênis') shows only matching product."""
        mod, _ = ecommerce_app
        events.dispatch("search_products", "Tênis")
        html = _render(mod.create_view)
        assert "Tênis Air Max" in html
        assert "Camisa Polo" not in html
        assert "Mochila Slim" not in html

    def test_search_partial_match(self, ecommerce_app):
        """Partial search term matches products containing the string."""
        mod, _ = ecommerce_app
        # "slim" is a substring of "Mochila Slim"
        events.dispatch("search_products", "slim")
        html = _render(mod.create_view)
        assert "Mochila Slim" in html
        assert "Tênis Air Max" not in html

    def test_search_no_results(self, ecommerce_app):
        """Non-matching search shows empty state."""
        mod, _ = ecommerce_app
        events.dispatch("search_products", "xyzxyzxyz")
        html = _render(mod.create_view)
        assert "Nenhum produto encontrado" in html

    def test_search_updates_state(self, ecommerce_app):
        """search_products stores the query in store.search_query."""
        _, store = ecommerce_app
        events.dispatch("search_products", "relógio")
        assert store.search_query == "relógio"

    def test_add_to_cart_first_item(self, ecommerce_app):
        """add_to_cart_1 adds product 1 to an empty cart."""
        _, store = ecommerce_app
        assert store.cart == []
        events.dispatch("add_to_cart_1")
        assert len(store.cart) == 1
        assert store.cart[0]["product_id"] == 1
        assert store.cart[0]["qty"] == 1

    def test_add_to_cart_increments_existing(self, ecommerce_app):
        """Adding the same product again increments its quantity (no duplicate)."""
        _, store = ecommerce_app
        events.dispatch("add_to_cart_1")
        events.dispatch("add_to_cart_1")
        assert len(store.cart) == 1
        assert store.cart[0]["qty"] == 2

    def test_add_multiple_different_products(self, ecommerce_app):
        """Adding different products creates separate cart entries."""
        _, store = ecommerce_app
        events.dispatch("add_to_cart_1")
        events.dispatch("add_to_cart_2")
        events.dispatch("add_to_cart_3")
        assert len(store.cart) == 3

    def test_cart_badge_reflects_total_qty(self, ecommerce_app):
        """Cart badge count updates in catalog view after adding items."""
        mod, _ = ecommerce_app
        events.dispatch("add_to_cart_1")
        events.dispatch("add_to_cart_2")
        html = _render(mod.create_view)
        assert "🛒 2" in html

    def test_add_shows_in_cart_button(self, ecommerce_app):
        """Product card button label updates after item is added to cart."""
        mod, _ = ecommerce_app
        events.dispatch("add_to_cart_1")
        html = _render(mod.create_view)
        assert "No carrinho (1)" in html

    def test_nav_cart_changes_screen(self, ecommerce_app):
        """nav_cart sets current_screen to 'cart'."""
        _, store = ecommerce_app
        events.dispatch("nav_cart")
        assert store.current_screen == "cart"

    def test_cart_screen_shows_items(self, ecommerce_app):
        """Cart screen lists added products."""
        mod, _ = ecommerce_app
        events.dispatch("add_to_cart_1")
        events.dispatch("nav_cart")
        html = _render(mod.create_view)
        assert "🛒 Carrinho" in html
        assert "Tênis Air Max" in html

    def test_cart_screen_empty_state(self, ecommerce_app):
        """Cart screen shows empty state when no items added."""
        mod, _ = ecommerce_app
        events.dispatch("nav_cart")
        html = _render(mod.create_view)
        assert "Carrinho vazio" in html

    def test_cart_screen_shows_total(self, ecommerce_app):
        """Cart screen calculates and shows the total price."""
        mod, _ = ecommerce_app
        events.dispatch("add_to_cart_1")  # R$ 299.90
        events.dispatch("nav_cart")
        html = _render(mod.create_view)
        assert "299.90" in html

    def test_cart_inc_increases_qty(self, ecommerce_app):
        """cart_inc_1 increments quantity of product 1 in cart."""
        mod, store = ecommerce_app
        events.dispatch("add_to_cart_1")
        events.dispatch("nav_cart")
        _render(mod.create_view)  # renders cart view → registers cart_inc_1 handler
        events.dispatch("cart_inc_1")
        assert store.cart[0]["qty"] == 2

    def test_cart_dec_decreases_qty(self, ecommerce_app):
        """cart_dec_1 decrements quantity; at 1 → 0 it removes the item."""
        mod, store = ecommerce_app
        events.dispatch("add_to_cart_1")
        events.dispatch("nav_cart")
        _render(mod.create_view)  # register cart_dec_1 handler
        events.dispatch("cart_dec_1")
        assert store.cart == []  # qty hit 0, item removed

    def test_cart_dec_from_two(self, ecommerce_app):
        """cart_dec_1 from qty=2 leaves qty=1 (does not remove)."""
        mod, store = ecommerce_app
        events.dispatch("add_to_cart_1")
        events.dispatch("add_to_cart_1")  # qty = 2
        events.dispatch("nav_cart")
        _render(mod.create_view)
        events.dispatch("cart_dec_1")
        assert store.cart[0]["qty"] == 1

    def test_nav_checkout_empty_cart_blocked(self, ecommerce_app):
        """nav_checkout does nothing when cart is empty."""
        _, store = ecommerce_app
        events.dispatch("nav_checkout")
        assert store.current_screen == "catalog"

    def test_nav_checkout_with_items(self, ecommerce_app):
        """nav_checkout navigates to 'checkout' when cart has items."""
        _, store = ecommerce_app
        events.dispatch("add_to_cart_1")
        events.dispatch("nav_checkout")
        assert store.current_screen == "checkout"

    def test_checkout_screen_renders(self, ecommerce_app):
        """Checkout screen shows form fields."""
        mod, _ = ecommerce_app
        events.dispatch("add_to_cart_1")
        events.dispatch("nav_checkout")
        html = _render(mod.create_view)
        assert "Checkout" in html
        assert "Seu nome" in html
        assert "seu@email.com" in html

    def test_checkout_shows_order_summary(self, ecommerce_app):
        """Checkout screen shows the cart items in a summary."""
        mod, _ = ecommerce_app
        events.dispatch("add_to_cart_1")
        events.dispatch("nav_checkout")
        html = _render(mod.create_view)
        assert "Resumo do pedido" in html
        assert "Tênis Air Max" in html

    def test_update_checkout_name(self, ecommerce_app):
        """update_checkout_name stores the name in state."""
        _, store = ecommerce_app
        events.dispatch("update_checkout_name", "João Silva")
        assert store.checkout_name == "João Silva"

    def test_update_checkout_email(self, ecommerce_app):
        """update_checkout_email stores the email in state."""
        _, store = ecommerce_app
        events.dispatch("update_checkout_email", "joao@email.com")
        assert store.checkout_email == "joao@email.com"

    def test_confirm_order_clears_cart(self, ecommerce_app):
        """confirm_order empties the cart and navigates to confirm screen."""
        _, store = ecommerce_app
        events.dispatch("add_to_cart_1")
        events.dispatch("nav_checkout")
        events.dispatch("update_checkout_name", "Maria")
        events.dispatch("confirm_order")
        assert store.cart == []
        assert store.current_screen == "confirm"

    def test_confirm_order_empty_name_blocked(self, ecommerce_app):
        """confirm_order with empty name does NOT clear cart or navigate."""
        _, store = ecommerce_app
        events.dispatch("add_to_cart_1")
        events.dispatch("nav_checkout")
        # Intentionally no update_checkout_name
        events.dispatch("confirm_order")
        assert len(store.cart) == 1
        assert store.current_screen == "checkout"

    def test_confirm_screen_renders_name(self, ecommerce_app):
        """Confirmation screen shows the customer's name."""
        mod, _ = ecommerce_app
        events.dispatch("add_to_cart_1")
        events.dispatch("nav_checkout")
        events.dispatch("update_checkout_name", "Carlos")
        events.dispatch("confirm_order")
        html = _render(mod.create_view)
        assert "Pedido Confirmado!" in html
        assert "Carlos" in html

    def test_nav_catalog_resets_search(self, ecommerce_app):
        """nav_catalog returns to catalog and resets search_query."""
        _, store = ecommerce_app
        events.dispatch("search_products", "Relógio")
        events.dispatch("nav_cart")
        events.dispatch("nav_catalog")
        assert store.current_screen == "catalog"
        assert store.search_query == ""

    def test_nav_catalog_from_cart_shows_all_products(self, ecommerce_app):
        """After nav_catalog from cart, all products are shown again."""
        mod, _ = ecommerce_app
        events.dispatch("nav_cart")
        events.dispatch("nav_catalog")
        html = _render(mod.create_view)
        assert "Tênis Air Max" in html
        assert "Relógio Sport" in html


# ──────────────────────────────────────────────────────────────────────────────
# App Isolation
# ──────────────────────────────────────────────────────────────────────────────

class TestAppIsolation:
    """
    Verify per-test isolation: each fixture provides a fresh module + store.

    Note: the two apps share Python module names ('views', 'state', 'components').
    Using both fixtures in the SAME test causes module conflicts, so each test
    below uses only one fixture at a time.
    """

    def test_todo_store_initial_state(self, todo_app):
        """todo_app fixture provides a fresh store with 3 initial todos."""
        _, store = todo_app
        assert hasattr(store, "todos")
        assert len(store.todos) == 3
        assert store.current_screen == "home"

    def test_ecommerce_store_initial_state(self, ecommerce_app):
        """ecommerce_app fixture provides a fresh store with 5 products."""
        _, store = ecommerce_app
        assert hasattr(store, "products")
        assert len(store.products) == 5
        assert store.current_screen == "catalog"

    def test_todo_event_registry(self, todo_app):
        """After loading todo_app, its specific handlers are registered."""
        assert events.has("nav_go")
        assert events.has("add_todo")
        assert events.has("clear_done")
        # Ecommerce-specific handlers must NOT be present
        assert not events.has("search_products")
        assert not events.has("confirm_order")

    def test_ecommerce_event_registry(self, ecommerce_app):
        """After loading ecommerce_app, its specific handlers are registered."""
        assert events.has("search_products")
        assert events.has("confirm_order")
        assert events.has("nav_checkout")
        # Todo-specific handlers must NOT be present
        assert not events.has("nav_go")
        assert not events.has("add_todo")

    def test_todo_state_mutation_does_not_persist(self, todo_app):
        """State changes in one test do not leak to the next (fresh fixture)."""
        _, store = todo_app
        events.dispatch("update_input", "leaked value")
        assert store.input_text == "leaked value"
        # The NEXT test that uses todo_app will get a fresh store via re-import

    def test_todo_fresh_state_after_mutation(self, todo_app):
        """Fixture re-import gives clean initial state regardless of previous test."""
        _, store = todo_app
        # input_text must be "" (not "leaked value" from the previous test)
        assert store.input_text == ""
