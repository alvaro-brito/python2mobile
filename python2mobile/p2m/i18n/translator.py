"""
P2M i18n — Simple JSON-based translator.

Usage:
    from p2m.i18n import configure, set_locale, get_locale, t

    configure("locales/", default_locale="pt")
    t("search_placeholder")          # "Buscar restaurantes..."
    t("greeting", name="João")       # "Olá, João!"
    set_locale("en")
    t("search_placeholder")          # "Search restaurants..."
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional

_locale: str = "en"
_translations: Dict[str, Dict[str, str]] = {}
_locales_dir: Optional[Path] = None


def configure(locales_dir: str, default_locale: str = "en") -> None:
    """Point to the locales directory and set the default locale."""
    global _locales_dir, _locale, _translations
    _locales_dir = Path(locales_dir)
    _translations = {}
    _locale = default_locale
    _load_locale(default_locale)


def set_locale(locale: str) -> None:
    """Switch to a different locale (loads JSON if not yet cached)."""
    global _locale
    _locale = locale
    _load_locale(locale)


def get_locale() -> str:
    """Return the currently active locale code."""
    return _locale


def t(key: str, **kwargs: Any) -> str:
    """Look up *key* in the current locale's translations.

    Falls back to the key string itself if the key is missing.
    Supports keyword formatting: t("greeting", name="João") with
    {"greeting": "Olá, {name}!"} → "Olá, João!"
    """
    locale_dict = _translations.get(_locale, {})
    template = locale_dict.get(key, key)
    if kwargs:
        try:
            return template.format(**kwargs)
        except (KeyError, ValueError):
            return template
    return template


# ── Internal ──────────────────────────────────────────────────────────────────

def _load_locale(locale: str) -> None:
    if locale in _translations:
        return
    if _locales_dir is None:
        _translations[locale] = {}
        return
    json_path = _locales_dir / f"{locale}.json"
    if json_path.is_file():
        with open(json_path, encoding="utf-8") as fh:
            _translations[locale] = json.load(fh)
    else:
        _translations[locale] = {}
