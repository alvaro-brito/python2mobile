"""
Integration tests for calculator_app, dashboard_app, and login_app.

Same module-isolation strategy as test_run_integration.py:
- Save/restore sys.path and sys.modules around each test
- Clear the global events registry before and after each fixture
- Initial render ensures all event handlers are registered
"""

import sys
import importlib
from pathlib import Path
import pytest

# ── Paths ─────────────────────────────────────────────────────────────────────

FRAMEWORK_PATH = Path(__file__).parent.parent          # .../python2mobile/
TESTS_P2M_PATH = FRAMEWORK_PATH.parent / "tests-p2m"  # .../tests-p2m/

if str(FRAMEWORK_PATH) not in sys.path:
    sys.path.insert(0, str(FRAMEWORK_PATH))

from p2m.core import events, Render
from p2m.core.render_engine import RenderEngine


# ── Helpers ───────────────────────────────────────────────────────────────────

def _render(create_view, mobile_frame: bool = False) -> str:
    tree = Render.execute(create_view)
    return RenderEngine().render(tree, mobile_frame=mobile_frame)


def _render_content(create_view) -> str:
    tree = Render.execute(create_view)
    return RenderEngine().render_content(tree)


def _load_app(app_dir: Path):
    sys.modules.pop("main", None)
    return importlib.import_module("main")


def _make_fixture(app_name: str):
    """Factory that returns a pytest fixture for the given tests-p2m app."""
    @pytest.fixture
    def _fixture():
        app_dir = TESTS_P2M_PATH / app_name
        saved_path = list(sys.path)
        saved_module_keys = set(sys.modules.keys())
        events.clear()

        sys.path.insert(0, str(app_dir))
        mod = _load_app(app_dir)
        _render(mod.create_view)   # initial render — registers event handlers

        yield mod, mod.store

        for key in list(sys.modules.keys()):
            if key not in saved_module_keys:
                del sys.modules[key]
        sys.path[:] = saved_path
        events.clear()

    return _fixture


calculator_app = _make_fixture("calculator_app")
dashboard_app  = _make_fixture("dashboard_app")
login_app      = _make_fixture("login_app")


# ══════════════════════════════════════════════════════════════════════════════
# CALCULATOR APP
# ══════════════════════════════════════════════════════════════════════════════

class TestCalculatorState:
    """State mutations via event handlers."""

    def test_initial_state(self, calculator_app):
        _, store = calculator_app
        assert store.display == "0"
        assert store.first_num is None
        assert store.operator is None
        assert store.awaiting_operand is False

    def test_press_digit_replaces_zero(self, calculator_app):
        mod, store = calculator_app
        events.dispatch("press_digit", "5")
        assert store.display == "5"

    def test_press_multiple_digits(self, calculator_app):
        mod, store = calculator_app
        events.dispatch("press_digit", "3")
        events.dispatch("press_digit", "7")
        assert store.display == "37"

    def test_leading_zero_not_doubled(self, calculator_app):
        """Pressing 0 when display is already '0' should not double it."""
        _, store = calculator_app
        events.dispatch("press_digit", "0")
        assert store.display == "0"

    def test_press_dot_appends(self, calculator_app):
        _, store = calculator_app
        events.dispatch("press_digit", "3")
        events.dispatch("press_digit", ".")
        assert store.display == "3."

    def test_double_dot_ignored(self, calculator_app):
        """Second '.' while not awaiting operand is ignored."""
        _, store = calculator_app
        events.dispatch("press_digit", "3")
        events.dispatch("press_digit", ".")
        events.dispatch("press_digit", "1")
        events.dispatch("press_digit", ".")   # should be ignored
        assert store.display.count(".") == 1

    def test_press_clear_resets(self, calculator_app):
        _, store = calculator_app
        events.dispatch("press_digit", "9")
        events.dispatch("press_operator", "+")
        events.dispatch("press_clear")
        assert store.display == "0"
        assert store.first_num is None
        assert store.operator is None
        assert store.awaiting_operand is False

    def test_press_operator_sets_first_num(self, calculator_app):
        _, store = calculator_app
        events.dispatch("press_digit", "5")
        events.dispatch("press_operator", "+")
        assert store.first_num == 5.0
        assert store.operator == "+"
        assert store.awaiting_operand is True

    def test_addition(self, calculator_app):
        _, store = calculator_app
        events.dispatch("press_digit", "3")
        events.dispatch("press_operator", "+")
        events.dispatch("press_digit", "5")
        events.dispatch("press_equals")
        assert store.display == "8"

    def test_subtraction(self, calculator_app):
        _, store = calculator_app
        events.dispatch("press_digit", "1")
        events.dispatch("press_digit", "0")
        events.dispatch("press_operator", "-")
        events.dispatch("press_digit", "3")
        events.dispatch("press_equals")
        assert store.display == "7"

    def test_multiplication(self, calculator_app):
        _, store = calculator_app
        events.dispatch("press_digit", "4")
        events.dispatch("press_operator", "*")
        events.dispatch("press_digit", "3")
        events.dispatch("press_equals")
        assert store.display == "12"

    def test_division(self, calculator_app):
        _, store = calculator_app
        events.dispatch("press_digit", "8")
        events.dispatch("press_operator", "/")
        events.dispatch("press_digit", "4")
        events.dispatch("press_equals")
        assert store.display == "2"

    def test_division_by_zero(self, calculator_app):
        _, store = calculator_app
        events.dispatch("press_digit", "5")
        events.dispatch("press_operator", "/")
        events.dispatch("press_digit", "0")
        events.dispatch("press_equals")
        assert store.display == "Erro"

    def test_chained_operations(self, calculator_app):
        """5 + 3 then − 2 = 6  (chain without pressing = in between)."""
        _, store = calculator_app
        events.dispatch("press_digit", "5")
        events.dispatch("press_operator", "+")
        events.dispatch("press_digit", "3")
        events.dispatch("press_operator", "-")   # triggers intermediate = 8
        assert store.display == "8"
        events.dispatch("press_digit", "2")
        events.dispatch("press_equals")
        assert store.display == "6"

    def test_press_toggle_sign_positive_to_negative(self, calculator_app):
        _, store = calculator_app
        events.dispatch("press_digit", "5")
        events.dispatch("press_toggle_sign")
        assert store.display == "-5"

    def test_press_toggle_sign_negative_to_positive(self, calculator_app):
        _, store = calculator_app
        events.dispatch("press_digit", "5")
        events.dispatch("press_toggle_sign")
        events.dispatch("press_toggle_sign")
        assert store.display == "5"

    def test_press_percent(self, calculator_app):
        _, store = calculator_app
        events.dispatch("press_digit", "5")
        events.dispatch("press_digit", "0")
        events.dispatch("press_percent")
        assert store.display == "0.5"

    def test_press_equals_without_operator_is_noop(self, calculator_app):
        """Pressing = with no pending operator should not crash."""
        _, store = calculator_app
        events.dispatch("press_digit", "7")
        events.dispatch("press_equals")
        assert store.display == "7"   # unchanged


class TestCalculatorRendering:
    """HTML output from the calculator view."""

    def test_render_shows_display(self, calculator_app):
        mod, _ = calculator_app
        html = _render(mod.create_view)
        assert "0" in html

    def test_render_digit_buttons_present(self, calculator_app):
        mod, _ = calculator_app
        html = _render(mod.create_view)
        for d in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            assert d in html

    def test_render_digit_buttons_use_press_digit(self, calculator_app):
        mod, _ = calculator_app
        html = _render(mod.create_view)
        assert "press_digit" in html

    def test_render_operator_buttons_present(self, calculator_app):
        mod, _ = calculator_app
        html = _render(mod.create_view)
        assert "press_operator" in html
        assert "press_equals"   in html
        assert "press_clear"    in html

    def test_render_display_updates_after_digit(self, calculator_app):
        mod, store = calculator_app
        events.dispatch("press_digit", "9")
        html = _render(mod.create_view)
        assert "9" in html

    def test_render_result_shown_after_equals(self, calculator_app):
        mod, store = calculator_app
        events.dispatch("press_digit", "6")
        events.dispatch("press_operator", "+")
        events.dispatch("press_digit", "4")
        events.dispatch("press_equals")
        html = _render(mod.create_view)
        assert "10" in html

    def test_render_active_operator_highlighted(self, calculator_app):
        """Active operator button gets a different background class."""
        mod, store = calculator_app
        events.dispatch("press_digit", "3")
        events.dispatch("press_operator", "+")
        html = _render(mod.create_view)
        # Active op button uses 'bg-white' instead of 'bg-orange-500'
        assert "background-color:#ffffff" in html

    def test_render_error_state(self, calculator_app):
        mod, store = calculator_app
        events.dispatch("press_digit", "1")
        events.dispatch("press_operator", "/")
        events.dispatch("press_digit", "0")
        events.dispatch("press_equals")
        html = _render(mod.create_view)
        assert "Erro" in html


# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD APP
# ══════════════════════════════════════════════════════════════════════════════

class TestDashboardState:
    """State mutations for dashboard navigation and toggles."""

    def test_initial_state(self, dashboard_app):
        _, store = dashboard_app
        assert store.current_tab == "overview"
        assert store.notifications_enabled is True
        assert store.dark_mode is False

    def test_nav_tab_to_reports(self, dashboard_app):
        _, store = dashboard_app
        events.dispatch("nav_tab", "reports")
        assert store.current_tab == "reports"

    def test_nav_tab_to_settings(self, dashboard_app):
        _, store = dashboard_app
        events.dispatch("nav_tab", "settings")
        assert store.current_tab == "settings"

    def test_nav_tab_back_to_overview(self, dashboard_app):
        _, store = dashboard_app
        events.dispatch("nav_tab", "reports")
        events.dispatch("nav_tab", "overview")
        assert store.current_tab == "overview"

    def test_toggle_notifications_off(self, dashboard_app):
        _, store = dashboard_app
        assert store.notifications_enabled is True
        events.dispatch("toggle_notifications")
        assert store.notifications_enabled is False

    def test_toggle_notifications_on(self, dashboard_app):
        _, store = dashboard_app
        events.dispatch("toggle_notifications")   # off
        events.dispatch("toggle_notifications")   # on again
        assert store.notifications_enabled is True

    def test_toggle_dark_mode_on(self, dashboard_app):
        _, store = dashboard_app
        assert store.dark_mode is False
        events.dispatch("toggle_dark_mode")
        assert store.dark_mode is True

    def test_toggle_dark_mode_off(self, dashboard_app):
        _, store = dashboard_app
        events.dispatch("toggle_dark_mode")   # on
        events.dispatch("toggle_dark_mode")   # off
        assert store.dark_mode is False


class TestDashboardRendering:
    """HTML output for each dashboard tab."""

    def test_render_overview_shows_title(self, dashboard_app):
        mod, _ = dashboard_app
        html = _render(mod.create_view)
        assert "Dashboard" in html

    def test_render_overview_shows_stats(self, dashboard_app):
        mod, _ = dashboard_app
        html = _render(mod.create_view)
        assert "1.247"   in html   # Usuários stat
        assert "R$8.432" in html   # Receita stat

    def test_render_overview_shows_activity(self, dashboard_app):
        mod, _ = dashboard_app
        html = _render(mod.create_view)
        assert "Atividade Recente" in html

    def test_render_nav_tabs_all_present(self, dashboard_app):
        mod, _ = dashboard_app
        html = _render(mod.create_view)
        assert "nav_tab" in html
        assert "overview"  in html
        assert "reports"   in html
        assert "settings"  in html

    def test_render_reports_view(self, dashboard_app):
        mod, store = dashboard_app
        events.dispatch("nav_tab", "reports")
        html = _render(mod.create_view)
        assert "Relatórios" in html
        assert "Transações"  in html

    def test_render_reports_shows_transactions(self, dashboard_app):
        mod, _ = dashboard_app
        events.dispatch("nav_tab", "reports")
        html = _render(mod.create_view)
        assert "Mochila Slim"  in html
        assert "R$149,50"      in html

    def test_render_settings_view(self, dashboard_app):
        mod, _ = dashboard_app
        events.dispatch("nav_tab", "settings")
        html = _render(mod.create_view)
        assert "Configurações"  in html
        assert "Notificações"   in html
        assert "Modo Escuro"    in html

    def test_render_settings_notifications_active(self, dashboard_app):
        """Notifications are ON by default — button should say 'Ativo'."""
        mod, _ = dashboard_app
        events.dispatch("nav_tab", "settings")
        html = _render(mod.create_view)
        assert "Ativo" in html

    def test_render_settings_notifications_toggled(self, dashboard_app):
        """After toggling off, button should say 'Inativo'."""
        mod, _ = dashboard_app
        events.dispatch("toggle_notifications")
        events.dispatch("nav_tab", "settings")
        html = _render(mod.create_view)
        assert "Inativo" in html

    def test_render_active_tab_highlighted(self, dashboard_app):
        """Active tab button uses blue color class."""
        mod, _ = dashboard_app
        events.dispatch("nav_tab", "reports")
        html = _render(mod.create_view)
        # Active tab gets text-blue-600 → color:#2563eb
        assert "color:#2563eb" in html


# ══════════════════════════════════════════════════════════════════════════════
# LOGIN APP
# ══════════════════════════════════════════════════════════════════════════════

class TestLoginState:
    """State mutations for the authentication flow."""

    def test_initial_state(self, login_app):
        _, store = login_app
        assert store.current_screen == "login"
        assert store.email         == ""
        assert store.password      == ""
        assert store.error         == ""
        assert store.logged_user   is None

    def test_update_email(self, login_app):
        _, store = login_app
        events.dispatch("update_email", "admin@p2m.dev")
        assert store.email == "admin@p2m.dev"

    def test_update_password(self, login_app):
        _, store = login_app
        events.dispatch("update_password", "secret")
        assert store.password == "secret"

    def test_update_email_clears_error(self, login_app):
        _, store = login_app
        store.error = "some error"
        events.dispatch("update_email", "new@email.com")
        assert store.error == ""

    def test_update_password_clears_error(self, login_app):
        _, store = login_app
        store.error = "some error"
        events.dispatch("update_password", "pwd")
        assert store.error == ""

    def test_login_success_admin(self, login_app):
        _, store = login_app
        events.dispatch("update_email",    "admin@p2m.dev")
        events.dispatch("update_password", "123456")
        events.dispatch("do_login")
        assert store.current_screen == "home"
        assert store.logged_user    == "Admin"
        assert store.error          == ""

    def test_login_success_second_user(self, login_app):
        _, store = login_app
        events.dispatch("update_email",    "user@test.com")
        events.dispatch("update_password", "abcdef")
        events.dispatch("do_login")
        assert store.current_screen == "home"
        assert store.logged_user    == "João Silva"

    def test_login_email_not_found(self, login_app):
        _, store = login_app
        events.dispatch("update_email",    "unknown@test.com")
        events.dispatch("update_password", "anything")
        events.dispatch("do_login")
        assert store.current_screen == "login"
        assert "não encontrado" in store.error

    def test_login_wrong_password(self, login_app):
        _, store = login_app
        events.dispatch("update_email",    "admin@p2m.dev")
        events.dispatch("update_password", "wrong")
        events.dispatch("do_login")
        assert store.current_screen == "login"
        assert "incorreta" in store.error

    def test_login_empty_email(self, login_app):
        _, store = login_app
        events.dispatch("update_password", "123456")
        events.dispatch("do_login")
        assert store.current_screen == "login"
        assert store.error != ""

    def test_login_empty_password(self, login_app):
        _, store = login_app
        events.dispatch("update_email", "admin@p2m.dev")
        events.dispatch("do_login")
        assert store.current_screen == "login"
        assert store.error != ""

    def test_login_both_empty(self, login_app):
        _, store = login_app
        events.dispatch("do_login")
        assert store.current_screen == "login"
        assert store.error != ""

    def test_logout_returns_to_login(self, login_app):
        _, store = login_app
        events.dispatch("update_email",    "admin@p2m.dev")
        events.dispatch("update_password", "123456")
        events.dispatch("do_login")
        assert store.current_screen == "home"
        events.dispatch("do_logout")
        assert store.current_screen == "login"

    def test_logout_clears_credentials(self, login_app):
        _, store = login_app
        events.dispatch("update_email",    "admin@p2m.dev")
        events.dispatch("update_password", "123456")
        events.dispatch("do_login")
        events.dispatch("do_logout")
        assert store.email        == ""
        assert store.password     == ""
        assert store.logged_user  is None


class TestLoginRendering:
    """HTML output for login and home screens."""

    def test_render_login_form(self, login_app):
        mod, _ = login_app
        html = _render(mod.create_view)
        assert "Bem-vindo"    in html
        assert "E-mail"       in html
        assert "Senha"        in html
        assert "Entrar"       in html

    def test_render_login_has_email_input(self, login_app):
        mod, _ = login_app
        html = _render(mod.create_view)
        assert 'type="email"' in html
        assert "update_email" in html

    def test_render_login_has_password_input(self, login_app):
        mod, _ = login_app
        html = _render(mod.create_view)
        assert 'type="password"' in html
        assert "update_password" in html

    def test_render_login_has_submit_button(self, login_app):
        mod, _ = login_app
        html = _render(mod.create_view)
        assert "do_login" in html

    def test_render_login_shows_error(self, login_app):
        mod, store = login_app
        store.error = "Senha incorreta."
        html = _render(mod.create_view)
        assert "Senha incorreta." in html
        assert "⚠️" in html

    def test_render_no_error_when_clean(self, login_app):
        mod, _ = login_app
        html = _render(mod.create_view)
        assert "⚠️" not in html

    def test_render_home_after_login(self, login_app):
        mod, store = login_app
        events.dispatch("update_email",    "admin@p2m.dev")
        events.dispatch("update_password", "123456")
        events.dispatch("do_login")
        html = _render(mod.create_view)
        assert "Olá, Admin!" in html
        assert "Sair"        in html

    def test_render_home_shows_user_email(self, login_app):
        mod, _ = login_app
        events.dispatch("update_email",    "admin@p2m.dev")
        events.dispatch("update_password", "123456")
        events.dispatch("do_login")
        html = _render(mod.create_view)
        assert "admin@p2m.dev" in html

    def test_render_home_has_logout_button(self, login_app):
        mod, _ = login_app
        events.dispatch("update_email",    "admin@p2m.dev")
        events.dispatch("update_password", "123456")
        events.dispatch("do_login")
        html = _render(mod.create_view)
        assert "do_logout" in html

    def test_render_login_after_logout(self, login_app):
        mod, _ = login_app
        events.dispatch("update_email",    "admin@p2m.dev")
        events.dispatch("update_password", "123456")
        events.dispatch("do_login")
        events.dispatch("do_logout")
        html = _render(mod.create_view)
        assert "Bem-vindo" in html
        assert "Entrar"    in html
