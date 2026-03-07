"""
Tests for p2m.i18n — configure, set_locale, get_locale, t.
"""

import json
import pytest
from pathlib import Path


@pytest.fixture()
def locale_dir(tmp_path):
    """Create a temporary locales directory with pt.json and en.json."""
    pt = {"greeting": "Olá, {name}!", "key_only": "Valor", "shared": "Português"}
    en = {"greeting": "Hello, {name}!", "key_only": "Value",  "shared": "English"}
    (tmp_path / "pt.json").write_text(json.dumps(pt), encoding="utf-8")
    (tmp_path / "en.json").write_text(json.dumps(en), encoding="utf-8")
    return tmp_path


@pytest.fixture(autouse=True)
def reset_i18n():
    """Reset i18n module state between tests."""
    import p2m.i18n.translator as _t
    _t._locale = "en"
    _t._translations = {}
    _t._locales_dir = None
    yield
    _t._locale = "en"
    _t._translations = {}
    _t._locales_dir = None


class TestConfigure:
    def test_configure_and_translate(self, locale_dir):
        from p2m.i18n import configure, t
        configure(str(locale_dir), default_locale="pt")
        assert t("key_only") == "Valor"

    def test_configure_sets_locale(self, locale_dir):
        from p2m.i18n import configure, get_locale
        configure(str(locale_dir), default_locale="pt")
        assert get_locale() == "pt"

    def test_configure_default_en(self, locale_dir):
        from p2m.i18n import configure, t
        configure(str(locale_dir), default_locale="en")
        assert t("key_only") == "Value"


class TestFormatKwargs:
    def test_format_kwargs(self, locale_dir):
        from p2m.i18n import configure, t
        configure(str(locale_dir), default_locale="pt")
        assert t("greeting", name="João") == "Olá, João!"

    def test_format_kwargs_en(self, locale_dir):
        from p2m.i18n import configure, set_locale, t
        configure(str(locale_dir), default_locale="pt")
        set_locale("en")
        assert t("greeting", name="Alice") == "Hello, Alice!"


class TestMissingKey:
    def test_missing_key_returns_key(self, locale_dir):
        from p2m.i18n import configure, t
        configure(str(locale_dir), default_locale="pt")
        assert t("nonexistent_key") == "nonexistent_key"

    def test_missing_locale_file_returns_key(self, tmp_path):
        from p2m.i18n import configure, t
        configure(str(tmp_path), default_locale="xx")
        assert t("some_key") == "some_key"


class TestSetLocale:
    def test_set_locale_switches_language(self, locale_dir):
        from p2m.i18n import configure, set_locale, t
        configure(str(locale_dir), default_locale="pt")
        assert t("shared") == "Português"
        set_locale("en")
        assert t("shared") == "English"

    def test_set_locale_back(self, locale_dir):
        from p2m.i18n import configure, set_locale, t
        configure(str(locale_dir), default_locale="en")
        set_locale("pt")
        set_locale("en")
        assert t("shared") == "English"


class TestGetLocale:
    def test_get_locale_default(self, locale_dir):
        from p2m.i18n import configure, get_locale
        configure(str(locale_dir), default_locale="pt")
        assert get_locale() == "pt"

    def test_get_locale_after_switch(self, locale_dir):
        from p2m.i18n import configure, set_locale, get_locale
        configure(str(locale_dir), default_locale="pt")
        set_locale("en")
        assert get_locale() == "en"
