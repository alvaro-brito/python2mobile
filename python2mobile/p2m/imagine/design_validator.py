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

    def _fix_password_input_type(self, s: str) -> str:
        """
        Add input_type="password" to Input() calls whose placeholder/value/on_change
        suggest a password field but are missing the attribute.
        Matches: placeholder="Password"|"Senha"|"PIN"|"Secret" etc.
        """
        # Match the FULL Input() call so we can check all arguments, not just up to placeholder
        _PASSWORD_HINTS = re.compile(
            r'Input\s*\([^)]*placeholder\s*=\s*["\'](?:password|senha|pin|secret|passcode|contraseña)["\'][^)]*\)',
            re.IGNORECASE | re.DOTALL,
        )

        def add_input_type(m: re.Match) -> str:
            snippet = m.group(0)
            if 'input_type' in snippet:
                return snippet  # already set — do not add duplicate
            # Insert input_type="password" before the closing )
            self.changes.append('Added input_type="password" to password Input field')
            # Strip trailing ) and re-add with the new kwarg
            return snippet[:-1].rstrip() + ',\n        input_type="password"\n    )'

        return _PASSWORD_HINTS.sub(add_input_type, s)

    def _fix_unterminated_strings(self, s: str) -> str:
        """
        Fix unterminated string literals caused by the LLM inserting a newline
        inside a string argument (common with long class_ values).

        Strategy: if ast.parse fails with 'unterminated string literal' at line N,
        join line N with line N+1 (strip the newline + leading whitespace between
        them).  Repeat until the error goes away or a different error type appears.
        """
        import ast

        max_passes = 20  # safety cap
        for _ in range(max_passes):
            try:
                ast.parse(s)
                return s  # clean
            except SyntaxError as e:
                msg = (e.msg or "").lower()
                if not any(k in msg for k in ("unterminated string", "eol while scanning", "eof while scanning")):
                    return s  # different error — leave for LLM fixer
                lineno = (e.lineno or 1) - 1  # 0-based
                lines = s.splitlines(keepends=True)
                if lineno >= len(lines) - 1:
                    return s  # can't join past end of file
                # Join the broken line with the continuation line
                merged = lines[lineno].rstrip("\n\r") + " " + lines[lineno + 1].lstrip()
                lines = lines[:lineno] + [merged] + lines[lineno + 2:]
                s = "".join(lines)
                self.changes.append(f"Unterminated string literal at line {lineno + 1} fixed (continuation joined)")
        return s

    def fix(self) -> str:
        s = self.source
        s = self._fix_broken_docstrings(s)    # must run first — syntax errors block other analysis
        s = self._fix_unterminated_strings(s) # join LLM-split string literals before other passes
        s = self._fix_password_input_type(s)
        s = self._fix_arbitrary_bg(s)
        s = self._fix_arbitrary_h(s)
        s = self._fix_arbitrary_w(s)
        s = self._fix_arbitrary_text(s)
        s = self._fix_flex_without_direction(s)
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

    def _fix_flex_without_direction(self, s: str) -> str:
        """
        Fix Container/Card/ScrollView that has 'flex' but neither 'flex-col' nor 'flex-row'.
        In Tailwind, bare 'flex' defaults to flex-direction: row, making children appear
        side by side instead of stacked — a very common LLM mistake on form containers.

        Adds 'flex-col' when the class contains 'flex' but no direction token.
        Only touches Container/Card classes, not Column/Row (they already have direction).
        """
        # Match Container/Card/ScrollView class strings
        def fix_flex(m: re.Match) -> str:
            tag = m.group(1)
            quote = m.group(2)
            cls = m.group(3)
            # Must have 'flex' but NOT 'flex-col', 'flex-row', 'flex-wrap', 'flex-1', 'flex-[', 'flex-none'
            if re.search(r'\bflex\b', cls) and not re.search(r'\bflex-(?:col|row|wrap|1|none|\[)', cls):
                new_cls = re.sub(r'\bflex\b', 'flex flex-col', cls)
                self.changes.append(
                    f'{tag}: bare "flex" → "flex flex-col" (was defaulting to flex-row)'
                )
                return f'{tag}(class_={quote}{new_cls}{quote}'
            return m.group(0)

        return re.sub(
            r'(Container|Card|ScrollView)\(class_=(["\'])([^"\']*flex[^"\']*)\2',
            fix_flex, s
        )

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


def _fix_missing_utils_imports(output_dir: Path, verbose: bool = True) -> dict[str, list[str]]:
    """
    Scan view/component files for calls to private helpers (_name) that are defined
    in utils.py but not imported.  Auto-injects 'from utils import ...' as needed.

    Returns {relative_filename: [change descriptions]} for every file patched.
    """
    import ast as _ast

    utils_path = output_dir / "utils.py"
    if not utils_path.exists():
        return {}

    # Collect all helpers defined in utils.py
    try:
        utils_tree = _ast.parse(utils_path.read_text(encoding="utf-8"))
    except SyntaxError:
        return {}

    utils_helpers: set[str] = {
        node.name
        for node in _ast.walk(utils_tree)
        if isinstance(node, (_ast.FunctionDef, _ast.AsyncFunctionDef))
        and node.name.startswith("_")
    }
    if not utils_helpers:
        return {}

    results: dict[str, list[str]] = {}

    # Scan view and component files (skip main.py, utils.py, state/, tests/)
    for path in sorted(output_dir.rglob("*.py")):
        if path.name in ("__init__.py", "utils.py"):
            continue
        # Skip the top-level entry point (main.py at project root), but NOT views/main.py
        if path.name == "main.py" and path.parent == output_dir:
            continue
        if "test_" in path.name or path.name.startswith("test"):
            continue
        if path.parent.name in ("state", "tests", "__pycache__"):
            continue

        source = path.read_text(encoding="utf-8")
        try:
            tree = _ast.parse(source)
        except SyntaxError:
            continue

        # Names already imported or defined in this file
        local_names: set[str] = set()
        for node in _ast.walk(tree):
            if isinstance(node, (_ast.FunctionDef, _ast.AsyncFunctionDef)):
                local_names.add(node.name)
            elif isinstance(node, _ast.Import):
                for alias in node.names:
                    local_names.add(alias.asname or alias.name.split(".")[0])
            elif isinstance(node, _ast.ImportFrom):
                for alias in node.names:
                    local_names.add(alias.asname or alias.name)

        # Find called helpers missing from local scope but present in utils.py
        missing: set[str] = set()
        for node in _ast.walk(tree):
            if isinstance(node, _ast.Call):
                func = node.func
                if (
                    isinstance(func, _ast.Name)
                    and func.id.startswith("_")
                    and func.id not in local_names
                    and func.id in utils_helpers
                ):
                    missing.add(func.id)

        if not missing:
            continue

        # Build the import line and inject after the last existing import line
        names_sorted = ", ".join(sorted(missing))
        import_line = f"from utils import {names_sorted}"

        # Check if a 'from utils import' line already exists (partial)
        existing_match = re.search(r"^from utils import (.+)$", source, re.MULTILINE)
        if existing_match:
            existing_names = {n.strip() for n in existing_match.group(1).split(",")}
            combined = sorted(existing_names | missing)
            new_line = f"from utils import {', '.join(combined)}"
            source = source[:existing_match.start()] + new_line + source[existing_match.end():]
        else:
            # Find the last import line and insert after it
            import_end = 0
            for node in _ast.walk(tree):
                if isinstance(node, (_ast.Import, _ast.ImportFrom)):
                    # node.end_lineno is available in Python 3.8+
                    end = getattr(node, "end_lineno", node.lineno)
                    if end > import_end:
                        import_end = end

            lines = source.splitlines(keepends=True)
            insert_at = import_end  # 0-based: after line at index import_end-1
            lines.insert(insert_at, import_line + "\n")
            source = "".join(lines)

        path.write_text(source, encoding="utf-8")
        change = f"Injected: {import_line}"
        results[str(path.relative_to(output_dir))] = [change]
        if verbose:
            print(f"  [design-validator] Fixed {path.name}: {change}")

    return results


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

    # Project-level fix: inject missing 'from utils import ...' in view files
    utils_fixes = _fix_missing_utils_imports(output_dir, verbose=verbose)
    results.update(utils_fixes)

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

def summarise_business_notes(output_dir: str | Path) -> list[str]:
    """
    Scan the generated project for business-relevant details a developer needs to know
    before running/testing the app:
      - Hardcoded credentials (username/password literals in authenticate/login handlers)
      - Default screen / navigation flow
      - Sample data counts
      - Input fields and their types
    Returns a list of human-readable note strings.
    """
    output_dir = Path(output_dir)
    notes: list[str] = []

    # 1. Credentials — scan main.py and all .py files for patterns like
    #    `if username == "..." and password == "..."`
    cred_pattern = re.compile(
        r'(?:username|user|login|email)\s*==\s*["\']([^"\']+)["\'].*?'
        r'(?:password|senha|secret|pin)\s*==\s*["\']([^"\']+)["\']',
        re.DOTALL | re.IGNORECASE,
    )
    for path in output_dir.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        for m in cred_pattern.finditer(source):
            notes.append(f"Login credentials  →  user: \"{m.group(1)}\"  |  password: \"{m.group(2)}\"")

    # 2. Default/initial screen
    screen_pattern = re.compile(r'current_screen\s*=\s*["\']([^"\']+)["\']')
    for path in [output_dir / "state" / "store.py", output_dir / "main.py"]:
        if path.exists():
            source = path.read_text(encoding="utf-8")
            m = screen_pattern.search(source)
            if m:
                notes.append(f"Initial screen     →  \"{m.group(1)}\"")
                break

    # 3. Sample data counts — scan store.py for lists
    store_py = output_dir / "state" / "store.py"
    if store_py.exists():
        source = store_py.read_text(encoding="utf-8")
        list_pattern = re.compile(r'(\w+)\s*=\s*\[(?:[^\[\]]*\{[^\}]+\}[^\[\]]*)+\]')
        for m in list_pattern.finditer(source):
            items = len(re.findall(r'\{', m.group(0)))
            if items > 0:
                notes.append(f"Sample data        →  {m.group(1)}: {items} item(s)")

    # 4. Password fields without input_type="password"
    pw_missing = []
    for path in output_dir.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        for m in re.finditer(
            r'Input\s*\([^)]*placeholder\s*=\s*["\'](?:password|senha|pin|secret)["\'](?![^)]*input_type)',
            source, re.IGNORECASE | re.DOTALL
        ):
            pw_missing.append(path.name)
    if pw_missing:
        notes.append(f"WARNING: password Input missing input_type=\"password\" in: {', '.join(set(pw_missing))}")

    return notes


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


def check_undefined_helpers(path: Path, project_root: Path) -> list[str]:
    """
    Detect calls to private helper functions (_name) in view/component files that are
    neither defined nor imported in that file.  These crash at runtime with NameError.

    Returns a list of warning strings.
    """
    import ast as _ast

    source = path.read_text(encoding="utf-8")
    try:
        tree = _ast.parse(source)
    except SyntaxError:
        return []

    # Collect names defined or imported in this file
    local_names: set[str] = set()
    for node in _ast.walk(tree):
        if isinstance(node, (_ast.FunctionDef, _ast.AsyncFunctionDef)):
            local_names.add(node.name)
        elif isinstance(node, _ast.Import):
            for alias in node.names:
                local_names.add(alias.asname or alias.name.split('.')[0])
        elif isinstance(node, _ast.ImportFrom):
            for alias in node.names:
                local_names.add(alias.asname or alias.name)
        elif isinstance(node, _ast.Assign):
            for target in node.targets:
                if isinstance(target, _ast.Name):
                    local_names.add(target.id)

    # Collect all called names that look like private helpers (_name)
    warnings = []
    for node in _ast.walk(tree):
        if isinstance(node, _ast.Call):
            func = node.func
            if isinstance(func, _ast.Name) and func.id.startswith('_') and func.id not in local_names:
                warnings.append(
                    f"'{func.id}()' called but not defined/imported in this file — will crash with NameError.\n"
                    f"      Fix: define it in this file OR create utils.py and import: from utils import {func.id}"
                )
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
        warns += check_undefined_helpers(path, output_dir)
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
# Syntax fixer loop (deterministic + LLM, up to N iterations)
# ---------------------------------------------------------------------------

def _collect_syntax_errors(output_dir: Path) -> list[tuple[Path, str]]:
    """Return (path, error_message) for every .py file with a syntax error."""
    errors: list[tuple[Path, str]] = []
    for path in sorted(output_dir.rglob("*.py")):
        if path.name == "__init__.py":
            continue
        if "test_" in path.name or path.name.startswith("test"):
            continue
        ok, err = check_syntax(path)
        if not ok:
            errors.append((path, err))
    return errors


_SYNTAX_FIX_SYSTEM = """\
You are a Python syntax error fixer for P2M (Python2Mobile) view files.
Fix ONLY the syntax error described — do not refactor or change logic.
The most common errors are:
  - Unterminated string literal: a class_ or other string argument was split across
    two lines without backslash continuation. Join the lines so the string stays on one line.
  - Unmatched parenthesis: an extra ) or missing ) from a nested call.
  - Missing colon, comma, or quote character.

Respond with the COMPLETE corrected Python source only.
No explanation, no markdown fences, no ```python``` block.
"""


def fix_syntax_with_llm(
    files_with_errors: list[tuple[Path, str]],
    model_provider: str = "openai",
    model_name: Optional[str] = None,
    api_key: Optional[str] = None,
    verbose: bool = True,
) -> int:
    """
    Use an LLM to fix syntax errors in the given files.
    Returns the number of files successfully fixed.
    """
    import os
    import ast

    fixed_count = 0
    for path, error_msg in files_with_errors:
        source = path.read_text(encoding="utf-8")
        user_msg = f"Fix this Python syntax error:\n\nError: {error_msg}\n\nFile: {path.name}\n\n{source}"
        try:
            if model_provider == "anthropic":
                import anthropic
                key = api_key or os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("P2M_ANTHROPIC_API_KEY")
                if not key:
                    continue
                client = anthropic.Anthropic(api_key=key)
                name = model_name or "claude-sonnet-4-6"
                msg = client.messages.create(
                    model=name, max_tokens=4096,
                    system=_SYNTAX_FIX_SYSTEM,
                    messages=[{"role": "user", "content": user_msg}],
                )
                fixed = msg.content[0].text.strip()

            elif model_provider == "openai":
                import openai
                key = api_key or os.environ.get("OPENAI_API_KEY") or os.environ.get("P2M_OPENAI_API_KEY")
                if not key:
                    continue
                client = openai.OpenAI(api_key=key)
                name = model_name or "gpt-4o"
                resp = client.chat.completions.create(
                    model=name, max_tokens=4096,
                    messages=[
                        {"role": "system", "content": _SYNTAX_FIX_SYSTEM},
                        {"role": "user", "content": user_msg},
                    ],
                )
                fixed = resp.choices[0].message.content.strip()
            else:
                continue

            # Strip accidental markdown fences
            if fixed.startswith("```"):
                fixed = re.sub(r'^```[a-z]*\n?', '', fixed)
                fixed = re.sub(r'\n?```$', '', fixed)

            # Only write back if the result parses cleanly
            try:
                ast.parse(fixed)
                path.write_text(fixed, encoding="utf-8")
                fixed_count += 1
                if verbose:
                    print(f"    ✓ LLM fixed syntax in {path.name}")
            except SyntaxError:
                if verbose:
                    print(f"    ✗ LLM response still has syntax errors in {path.name} — skipping")

        except Exception as exc:
            if verbose:
                print(f"    ⚠ LLM syntax fix failed for {path.name}: {exc}")

    return fixed_count


def validate_and_fix_loop(
    output_dir: str | Path,
    model_provider: str = "openai",
    model_name: Optional[str] = None,
    api_key: Optional[str] = None,
    max_iterations: int = 5,
    verbose: bool = True,
) -> bool:
    """
    Run deterministic design fixes + syntax validation in a loop.
    If syntax errors remain after deterministic fixes, call the LLM to fix them.
    Repeats up to max_iterations times.  Returns True if all files are clean.
    """
    output_dir = Path(output_dir)

    for attempt in range(1, max_iterations + 1):
        prefix = f"[iter {attempt}/{max_iterations}]" if attempt > 1 else ""

        # Pass 1 — deterministic fixes (includes unterminated-string joiner)
        fix_project(output_dir, verbose=verbose)

        # Pass 2 — collect remaining syntax errors
        errors = _collect_syntax_errors(output_dir)

        if not errors:
            # Also run logic checks for warnings (non-blocking)
            _print_logic_warnings(output_dir, verbose)
            if verbose:
                if attempt > 1:
                    print(f"[code-validator] ✅ All files clean after {attempt} iteration(s)")
                else:
                    print("[code-validator] All files pass syntax and logic checks")
            return True

        if verbose:
            if attempt == 1:
                print("\n[code-validator] Syntax errors found:")
            else:
                print(f"\n[code-validator] {prefix} Still {len(errors)} file(s) with errors:")
            for path, err in errors:
                print(f"  ✗ {path.relative_to(output_dir)}: {err}")

        if attempt == max_iterations:
            break

        # Pass 3 — LLM fixer for remaining errors
        if verbose:
            print(f"[code-fixer] Attempt {attempt}/{max_iterations - 1}: fixing {len(errors)} file(s) with LLM...")
        fixed = fix_syntax_with_llm(errors, model_provider, model_name, api_key, verbose)
        if fixed == 0:
            if verbose:
                print("[code-fixer] No files could be fixed — stopping early.")
            break

    # Final: print remaining errors
    errors = _collect_syntax_errors(output_dir)
    if errors and verbose:
        print(f"\n⚠️  {len(errors)} file(s) still have syntax errors after {max_iterations} iteration(s).")
        print("   Run `p2m run --skip-validation` to see the full error, or fix manually.")
    return len(errors) == 0


def _print_logic_warnings(output_dir: Path, verbose: bool) -> None:
    """Print non-blocking logic warnings (no return value — informational only)."""
    if not verbose:
        return
    any_warn = False
    for path in sorted(output_dir.rglob("*.py")):
        if path.name == "__init__.py" or "test_" in path.name or path.name.startswith("test"):
            continue
        warns = check_logic(path)
        warns += check_undefined_helpers(path, output_dir)
        if warns:
            if not any_warn:
                print("\n[code-validator] Logic warnings:")
                any_warn = True
            for w in warns:
                print(f"  ⚠ {path.relative_to(output_dir)}: {w}")


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
