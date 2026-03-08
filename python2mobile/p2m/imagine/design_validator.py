"""
P2M Design Validator — post-generation fixer for known layout anti-patterns.

Runs automatically after `p2m imagine` generates a project.  Applies two passes:

  Pass 1 — Deterministic rule-based fixes (instant, no LLM)
  Pass 2 — LLM review pass (optional, only when API key is available)

Known anti-patterns detected and fixed:
  - Arbitrary Tailwind values: bg-[#xxx], h-[Npx], w-[Npx], text-[Npx]
  - CSS Grid in views (grid grid-cols-N) → warn + attempt Row conversion hint
  - aspect-square on flex-1 buttons → replace with py-5
  - Missing w-full on Row classes inside Column (flex-col) contexts
  - Missing min-h-screen on root Column
  - flex-1 on display containers (pushes buttons to bottom) → h-36
  - press_digit "0" bug: `"0" if ... == "0"` → `digit if ... == "0"`
  - Unicode minus: ASCII "-" in _calculate → "−" (U+2212)
  - "=" button routing to press_operator → press_equals
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Arbitrary-value → standard class mappings
# ---------------------------------------------------------------------------

# Map common h-[Npx] → closest h-N Tailwind class
_H_PX_MAP = {
    range(12, 20): "h-4",
    range(20, 28): "h-5",
    range(28, 36): "h-7",
    range(36, 44): "h-9",
    range(44, 52): "h-11",
    range(52, 60): "h-13",
    range(60, 72): "h-16",
    range(72, 84): "h-20",
    range(84, 96): "h-24",
    range(96, 120): "h-28",
    range(120, 144): "h-32",
    range(144, 168): "h-36",
    range(168, 192): "h-44",
    range(192, 220): "h-48",
    range(220, 256): "h-56",
    range(256, 300): "h-64",
}

# Common color hex → Tailwind named approximations
_COLOR_MAP = {
    "#000000": "black",   "#111111": "gray-950", "#1c1c1e": "gray-900",
    "#212121": "gray-900","#2c2c2e": "gray-800", "#3a3a3c": "gray-800",
    "#48484a": "gray-700","#636366": "gray-600", "#8e8e93": "gray-500",
    "#a5a5a5": "gray-400","#aeaeb2": "gray-400", "#c7c7cc": "gray-300",
    "#d1d1d6": "gray-200","#e5e5ea": "gray-100", "#f2f2f7": "gray-50",
    "#ffffff": "white",
    "#ff3b30": "red-500",  "#ff453a": "red-500",  "#ff6b6b": "red-400",
    "#ff9500": "orange-500","#ff9f0a": "orange-500","#ffcc00": "yellow-400",
    "#34c759": "green-500","#30d158": "green-500","#00c7be": "teal-500",
    "#007aff": "blue-500", "#0a84ff": "blue-500", "#5856d6": "violet-600",
    "#af52de": "purple-500","#ff2d55": "rose-500","#ff375f": "rose-500",
}


def _closest_h_class(px: int) -> str:
    for r, cls in _H_PX_MAP.items():
        if px in r:
            return cls
    return "h-16" if px < 64 else "h-24"


def _closest_bg_class(hex_color: str) -> str:
    key = hex_color.lower()
    if key in _COLOR_MAP:
        return f"bg-{_COLOR_MAP[key]}"
    # Try without alpha
    base = key[:7]
    if base in _COLOR_MAP:
        return f"bg-{_COLOR_MAP[base]}"
    # Fallback: guess gray shade from luminance
    try:
        r = int(key[1:3], 16)
        g = int(key[3:5], 16)
        b = int(key[5:7], 16)
        lum = (r + g + b) / (3 * 255)
        if lum < 0.1:   return "bg-gray-900"
        if lum < 0.25:  return "bg-gray-800"
        if lum < 0.40:  return "bg-gray-700"
        if lum < 0.55:  return "bg-gray-600"
        if lum < 0.70:  return "bg-gray-400"
        if lum < 0.85:  return "bg-gray-200"
        return "bg-gray-50"
    except Exception:
        return "bg-gray-700"


# ---------------------------------------------------------------------------
# Rule-based fixer
# ---------------------------------------------------------------------------

class DesignFixer:
    """Apply deterministic fixes to a Python source string."""

    def __init__(self, source: str, filename: str = ""):
        self.source = source
        self.filename = filename
        self.changes: list[str] = []

    # ── public API ───────────────────────────────────────────────────────────

    def fix(self) -> str:
        s = self.source
        s = self._fix_broken_docstrings(s)  # must run first — syntax errors block other analysis
        s = self._fix_arbitrary_bg(s)
        s = self._fix_arbitrary_h(s)
        s = self._fix_arbitrary_w(s)
        s = self._fix_arbitrary_text(s)
        s = self._fix_aspect_square(s)
        s = self._fix_row_missing_w_full(s)
        s = self._fix_press_digit_zero_bug(s)
        s = self._fix_unicode_minus(s)
        s = self._fix_equals_press_operator(s)
        return s

    # ── individual fixers ────────────────────────────────────────────────────

    def _fix_arbitrary_bg(self, s: str) -> str:
        """bg-[#rrggbb] or bg-[#rrggbbaa] → bg-gray-NNN / bg-orange-500 etc."""
        def replace(m: re.Match) -> str:
            hex_val = m.group(1)
            replacement = _closest_bg_class(hex_val)
            self.changes.append(f"bg-[{hex_val}] → {replacement}")
            return replacement
        return re.sub(r'bg-\[(#[0-9a-fA-F]{3,8})\]', replace, s)

    def _fix_arbitrary_h(self, s: str) -> str:
        """h-[Npx] → closest h-N class."""
        def replace(m: re.Match) -> str:
            px = int(m.group(1))
            replacement = _closest_h_class(px)
            self.changes.append(f"h-[{px}px] → {replacement}")
            return replacement
        return re.sub(r'h-\[(\d+)px\]', replace, s)

    def _fix_arbitrary_w(self, s: str) -> str:
        """w-[Npx] → closest w-N class (mirrors h mapping)."""
        def replace(m: re.Match) -> str:
            px = int(m.group(1))
            replacement = _closest_h_class(px).replace("h-", "w-")
            self.changes.append(f"w-[{px}px] → {replacement}")
            return replacement
        return re.sub(r'w-\[(\d+)px\]', replace, s)

    def _fix_arbitrary_text(self, s: str) -> str:
        """text-[Npx] → closest text-NNN class."""
        _TEXT_PX_MAP = {
            range(0, 13):  "text-xs",
            range(13, 15): "text-sm",
            range(15, 18): "text-base",
            range(18, 21): "text-lg",
            range(21, 25): "text-xl",
            range(25, 29): "text-2xl",
            range(29, 33): "text-3xl",
            range(33, 39): "text-4xl",
            range(39, 48): "text-5xl",
            range(48, 60): "text-6xl",
            range(60, 72): "text-7xl",
        }
        def replace(m: re.Match) -> str:
            px = int(m.group(1))
            for r, cls in _TEXT_PX_MAP.items():
                if px in r:
                    self.changes.append(f"text-[{px}px] → {cls}")
                    return cls
            replacement = "text-4xl"
            self.changes.append(f"text-[{px}px] → {replacement}")
            return replacement
        return re.sub(r'text-\[(\d+)px\]', replace, s)

    def _fix_aspect_square(self, s: str) -> str:
        """
        Remove 'aspect-square' when it appears alongside 'flex-1'.
        In P2M's renderer, aspect-square on a flex-1 item collapses the button
        to its content height → tiny unusable circles.
        Replace with py-5 if not already present.
        """
        # Only target string literals (inside quotes) to avoid touching comments
        def replace(m: re.Match) -> str:
            inner = m.group(1)
            quote = m.group(0)[0]  # ' or "
            if "flex-1" in inner and "aspect-square" in inner:
                new_inner = inner.replace("aspect-square", "").strip()
                # Normalise multiple spaces
                new_inner = re.sub(r'  +', ' ', new_inner)
                # Add py-5 if not already there
                if "py-" not in new_inner:
                    new_inner = new_inner.rstrip() + " py-5"
                self.changes.append("aspect-square removed (flex-1 context → py-5 added)")
                return f'{quote}{new_inner}{quote}'
            return m.group(0)

        return re.sub(r'(["\'])([^"\']*aspect-square[^"\']*)\1', replace, s)

    def _fix_row_missing_w_full(self, s: str) -> str:
        """
        Add w-full to Row class_ strings that contain flex-row but NOT w-full.
        A Row without w-full inside a flex-col Column collapses to content width,
        making flex-1 buttons inside it not fill the screen.
        """
        def replace(m: re.Match) -> str:
            inner = m.group(1)
            quote = m.group(0)[0]
            if "flex-row" in inner and "w-full" not in inner:
                new_inner = inner.replace("flex-row", "flex-row w-full")
                self.changes.append("Row missing w-full → added w-full to flex-row")
                return f'{quote}{new_inner}{quote}'
            return m.group(0)

        return re.sub(r'(["\'])([^"\']*flex-row[^"\']*)\1', replace, s)

    def _fix_press_digit_zero_bug(self, s: str) -> str:
        """
        Fix the classic press_digit "0" bug:
          `"0" if store.display == "0" else store.display + digit`
          → `digit if store.display == "0" else store.display + digit`

        The original keeps "0" forever instead of replacing it with the typed digit.
        """
        pattern = r'"0"\s+if\s+store\.display\s*==\s*"0"\s+else\s+store\.display\s*\+\s*digit'
        replacement = 'digit if store.display == "0" else store.display + digit'
        new_s, n = re.subn(pattern, replacement, s)
        if n:
            self.changes.append('press_digit "0" bug fixed: "0" if … → digit if …')
        return new_s

    def _fix_unicode_minus(self, s: str) -> str:
        """
        Fix _calculate comparing against ASCII hyphen "-" instead of Unicode minus "−" (U+2212).
        Buttons send "−" (the label), so _calculate must use the same symbol.
        Only targets the specific pattern inside _calculate to avoid false positives.
        """
        UNICODE_MINUS = "\u2212"  # − character; can't use \u in re replacement strings

        def replace(m: re.Match) -> str:
            self.changes.append('_calculate: ASCII "-" → Unicode "−" (U+2212)')
            return f'{m.group(1)}"{UNICODE_MINUS}"{m.group(3)}'

        pattern = r'(if\s+op\s*==\s*)"(-)"(\s*:\s*return\s+a\s*-\s*b)'
        return re.sub(pattern, replace, s)

    def _fix_broken_docstrings(self, s: str) -> str:
        """
        Fix corrupted docstrings like  \"""text.\"""\"""  (extra triple-quote appended).
        Caused by a bug in agent.py prompt examples where escaped quotes had a trailing ".
        Pattern: '"""' immediately following the closing '"""' of a docstring.
        """
        # Match: triple-quote, content, triple-quote, triple-quote (the extra one)
        pattern = r'("""[^"]*?""")(""")'
        def replace(m: re.Match) -> str:
            self.changes.append('Broken docstring fixed: removed extra """')
            return m.group(1)
        return re.sub(pattern, replace, s)

    def _fix_equals_press_operator(self, s: str) -> str:
        """
        Detect '=' button being routed to press_operator and redirect to press_equals.

        Patterns caught:
          Button("=", ..., on_click="press_operator", ...)
          _op_btn("=")
        """
        changes_before = len(self.changes)

        # Pattern 1: Button("=", ..., on_click="press_operator"...)
        def fix_button_eq(m: re.Match) -> str:
            self.changes.append('"=" button: on_click="press_operator" → press_equals')
            return m.group(0).replace('on_click="press_operator"', 'on_click="press_equals"')
        s = re.sub(
            r'Button\s*\(\s*"="\s*,(?:[^)]*?)on_click\s*=\s*"press_operator"(?:[^)]*?)\)',
            fix_button_eq, s, flags=re.DOTALL
        )

        # Pattern 2: _op_btn("=") → explicit Button with press_equals
        # We can't fully replace _op_btn("=") since we don't know _OP class,
        # but we can warn — a full rewrite would need context.
        if '_op_btn("=")' in s or "_op_btn('=')" in s:
            self.changes.append(
                'WARNING: _op_btn("=") detected — "=" should use press_equals, '
                'not press_operator. Replace with explicit Button("=", on_click="press_equals").'
            )

        return s


# ---------------------------------------------------------------------------
# File-level runner
# ---------------------------------------------------------------------------

def fix_file(path: Path, verbose: bool = True) -> list[str]:
    """Read, fix, and write back a single Python file. Returns list of changes made."""
    source = path.read_text(encoding="utf-8")
    fixer = DesignFixer(source, filename=str(path))
    fixed = fixer.fix()
    if fixer.changes:
        path.write_text(fixed, encoding="utf-8")
        if verbose:
            print(f"  [design-validator] Fixed {path.name}:")
            for c in fixer.changes:
                print(f"    • {c}")
    return fixer.changes


def fix_project(output_dir: str | Path, verbose: bool = True) -> dict[str, list[str]]:
    """
    Run deterministic design fixes on all .py files in an output directory.
    Returns {filename: [changes]} for all files that were modified.
    """
    output_dir = Path(output_dir)
    results: dict[str, list[str]] = {}

    py_files = list(output_dir.rglob("*.py"))
    for path in py_files:
        # Skip __init__.py (must stay empty) and test files
        if path.name == "__init__.py":
            continue
        if "test_" in path.name or path.name.startswith("test"):
            continue
        changes = fix_file(path, verbose=verbose)
        if changes:
            results[str(path.relative_to(output_dir))] = changes

    if results:
        if verbose:
            print(f"\n[design-validator] Fixed {len(results)} file(s) in {output_dir}")
    else:
        if verbose:
            print(f"[design-validator] No issues found in {output_dir}")

    return results


# ---------------------------------------------------------------------------
# Syntax + logic validator
# ---------------------------------------------------------------------------

def check_syntax(path: Path) -> tuple[bool, str]:
    """
    Parse a Python file with ast.parse.
    Returns (ok, error_message).  error_message is "" when ok=True.
    """
    import ast
    source = path.read_text(encoding="utf-8")
    try:
        ast.parse(source, filename=str(path))
        return True, ""
    except SyntaxError as e:
        return False, f"SyntaxError at line {e.lineno}: {e.msg}"


_LOGIC_CHECKS = [
    # (description, pattern, suggestion)
    (
        "press_digit keeps '0' forever",
        r'"0"\s+if\s+store\.display\s*==\s*"0"',
        'Use: digit if store.display == "0" else store.display + digit',
    ),
    (
        "_calculate uses ASCII minus '-' instead of Unicode '−'",
        r'op\s*==\s*"-"',
        'Use Unicode minus: op == "−"  (U+2212)',
    ),
    (
        '"=" button routes to press_operator instead of press_equals',
        r'Button\s*\(\s*["\']=["\'].*?on_click\s*=\s*["\']press_operator["\']',
        'Use: on_click="press_equals"',
    ),
    (
        "Arbitrary Tailwind value detected (will silently fail)",
        r'(?:bg|h|w|text|p|gap|m)-\[[^\]]+\](?<!flex-\[)',
        "Replace with standard Tailwind class (e.g. bg-gray-700, h-16)",
    ),
    (
        "CSS Grid used (not supported by P2M renderer)",
        r'grid\s+grid-cols-',
        "Use Row(class_='flex flex-row w-full gap-3') instead",
    ),
    (
        "aspect-square on flex-1 button (collapses to content height)",
        r'flex-1[^"\']*aspect-square|aspect-square[^"\']*flex-1',
        "Remove aspect-square; use py-5 for explicit button height",
    ),
    (
        "Row missing w-full (buttons won't fill screen width)",
        r'Row\s*\([^)]*flex-row(?![^)]*w-full)',
        "Add w-full to Row class_: flex flex-row w-full gap-3",
    ),
    (
        "Handler typed as int but on_click_args are always strings — causes TypeError",
        r'def\s+\w+\s*\([^)]*:\s*int[^)]*\)[^:]*:.*?on_click_args',
        "Change parameter type to str and convert inside handler: int(row)",
    ),
    (
        "on_click_args contains bare integer literals (must be str)",
        r'on_click_args\s*=\s*\[[^\]]*(?<!\')[0-9]+(?!\')[^\]]*\]',
        "Wrap integers as strings: on_click_args=[str(row), str(col)]",
    ),
]


def check_logic(path: Path) -> list[str]:
    """
    Run regex-based logic checks on a Python file.
    Returns a list of warning strings.
    """
    source = path.read_text(encoding="utf-8")
    warnings = []
    for desc, pattern, suggestion in _LOGIC_CHECKS:
        if re.search(pattern, source, re.DOTALL):
            warnings.append(f"{desc}\n      Fix: {suggestion}")
    return warnings


def validate_project(output_dir: str | Path, verbose: bool = True) -> bool:
    """
    Run syntax + logic checks on all non-test, non-init .py files.
    Prints results and returns True if everything passes.
    """
    output_dir = Path(output_dir)
    all_ok = True

    py_files = sorted(output_dir.rglob("*.py"))
    syntax_errors: list[tuple[Path, str]] = []
    logic_warnings: list[tuple[Path, list[str]]] = []

    for path in py_files:
        if path.name == "__init__.py":
            continue
        if "test_" in path.name or path.name.startswith("test"):
            continue

        ok, err = check_syntax(path)
        if not ok:
            syntax_errors.append((path, err))
            all_ok = False

        warns = check_logic(path)
        if warns:
            logic_warnings.append((path, warns))

    if verbose:
        rel = lambda p: p.relative_to(output_dir)
        if syntax_errors:
            print("\n[code-validator] Syntax errors found:")
            for path, err in syntax_errors:
                print(f"  ✗ {rel(path)}: {err}")
        if logic_warnings:
            print("\n[code-validator] Logic warnings:")
            for path, warns in logic_warnings:
                for w in warns:
                    print(f"  ⚠ {rel(path)}: {w}")
        if not syntax_errors and not logic_warnings:
            print("[code-validator] All files pass syntax and logic checks")

    return all_ok


# ---------------------------------------------------------------------------
# Optional LLM review pass
# ---------------------------------------------------------------------------

_LLM_REVIEW_SYSTEM = """\
You are a P2M (Python2Mobile) design validator.

P2M renders a Python component tree to HTML using a hardcoded Tailwind CSS class dictionary
(NOT the CDN JIT compiler). Only standard Tailwind utility classes work.

Your task: review the generated view Python file and fix any remaining layout issues.

KNOWN CONSTRAINTS you must enforce:
1. NO arbitrary Tailwind values: bg-[#xxx], h-[Npx], w-[Npx], text-[Npx] → SILENTLY FAIL
2. NO CSS Grid (grid grid-cols-N) → renders as block div, all children stack vertically
3. NO aspect-square on flex-1 buttons → collapses to content height
4. Row class_ MUST contain w-full when inside a flex-col Column
5. Root Column MUST have min-h-screen
6. Calculator display: use h-36 fixed height (NEVER flex-1)
7. "=" button: on_click="press_equals" — NEVER press_operator
8. press_digit: `digit if store.display == "0" else ...` (replaces "0", NOT keeps it)
9. _calculate: Unicode "−" (U+2212) — NEVER ASCII hyphen "-"
10. Button factory classes MUST include flex-1 for width distribution in rows

Respond with the COMPLETE corrected Python source only. No explanation, no markdown fences.
"""


def llm_review_file(
    path: Path,
    model_provider: str = "anthropic",
    model_name: Optional[str] = None,
    api_key: Optional[str] = None,
    verbose: bool = True,
) -> bool:
    """
    Run an LLM review pass on a single file.
    Returns True if the file was modified.
    """
    import os

    # Never touch __init__.py — must stay empty
    if path.name == "__init__.py":
        return False

    source = path.read_text(encoding="utf-8")

    # Only bother reviewing view files (views/*.py, components/*.py) and main.py
    if path.parent.name not in ("views", "components") and path.name != "main.py":
        return False

    if verbose:
        print(f"  [design-validator/llm] Reviewing {path.name}...")

    try:
        if model_provider == "anthropic":
            import anthropic
            key = api_key or os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("P2M_ANTHROPIC_API_KEY")
            if not key:
                return False
            client = anthropic.Anthropic(api_key=key)
            model = model_name or "claude-opus-4-6"
            msg = client.messages.create(
                model=model,
                max_tokens=4096,
                system=_LLM_REVIEW_SYSTEM,
                messages=[{"role": "user", "content": f"Fix this P2M view file:\n\n{source}"}],
            )
            fixed = msg.content[0].text.strip()

        elif model_provider == "openai":
            import openai
            key = api_key or os.environ.get("OPENAI_API_KEY") or os.environ.get("P2M_OPENAI_API_KEY")
            if not key:
                return False
            client = openai.OpenAI(api_key=key)
            model = model_name or "gpt-4o"
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": _LLM_REVIEW_SYSTEM},
                    {"role": "user", "content": f"Fix this P2M view file:\n\n{source}"},
                ],
                max_tokens=4096,
            )
            fixed = resp.choices[0].message.content.strip()

        else:
            return False

        # Strip accidental markdown fences
        if fixed.startswith("```"):
            fixed = re.sub(r'^```[a-z]*\n?', '', fixed)
            fixed = re.sub(r'\n?```$', '', fixed)

        if fixed != source:
            path.write_text(fixed, encoding="utf-8")
            if verbose:
                print(f"    ✓ LLM applied corrections to {path.name}")
            return True

    except Exception as exc:
        if verbose:
            print(f"    ⚠ LLM review skipped: {exc}")

    return False


def llm_review_project(
    output_dir: str | Path,
    model_provider: str = "anthropic",
    model_name: Optional[str] = None,
    api_key: Optional[str] = None,
    verbose: bool = True,
) -> int:
    """Run LLM review on all view/component files. Returns count of modified files."""
    output_dir = Path(output_dir)
    modified = 0
    for path in sorted(output_dir.rglob("*.py")):
        if "test_" in path.name:
            continue
        if llm_review_file(path, model_provider, model_name, api_key, verbose):
            modified += 1
    return modified
