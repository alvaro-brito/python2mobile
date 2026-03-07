"""
Tests for the `p2m build` test-gate step.

Verifies that:
- build aborts when tests/ contains failing tests
- build proceeds when tests/ passes (or is absent)
- --skip-tests bypasses the gate
- --help exposes the new flag

All subprocess tests run in a minimal temp project dir to avoid touching
the framework's own test suite.
"""

import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

_TOML = textwrap.dedent("""\
    [project]
    name = "test_proj"
    version = "0.1.0"
    entry = "main.py"
    [build]
    target = ["android"]
    generator = "flutter"
    llm_provider = "openai"
    llm_model = "gpt-4o"
    output_dir = "./build"
    cache = false
    [devserver]
    port = 3000
    hot_reload = true
    mobile_frame = true
    [style]
    system = "tailwind"
""")

_MAIN_PY = textwrap.dedent("""\
    from p2m.core import Render
    from p2m.ui import Column, Text

    def create_view():
        root = Column()
        root.add(Text("Hello"))
        return root.build()

    def main():
        Render.execute(create_view)
""")


def _make_project(tmp_path: Path, test_content: str = None) -> Path:
    (tmp_path / "p2m.toml").write_text(_TOML)
    (tmp_path / "main.py").write_text(_MAIN_PY)
    if test_content is not None:
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        (tests_dir / "__init__.py").write_text("")
        (tests_dir / "test_app.py").write_text(test_content)
    return tmp_path


def _build(tmp_path: Path, *extra_args):
    """Invoke `python -m p2m.cli build` in *tmp_path* and return CompletedProcess."""
    return subprocess.run(
        [sys.executable, "-m", "p2m.cli", "build", *extra_args],
        capture_output=True, text=True, cwd=str(tmp_path),
    )


# ── Help flag ─────────────────────────────────────────────────────────────────

class TestBuildHelp:
    def test_skip_tests_flag_in_help(self):
        proc = subprocess.run(
            ["p2m", "build", "--help"], capture_output=True, text=True
        )
        assert proc.returncode == 0
        assert "--skip-tests" in proc.stdout

    def test_skip_validation_still_present(self):
        proc = subprocess.run(
            ["p2m", "build", "--help"], capture_output=True, text=True
        )
        assert "--skip-validation" in proc.stdout


# ── Test gate behaviour ───────────────────────────────────────────────────────

class TestBuildTestGate:
    def test_failing_tests_abort_build(self, tmp_path):
        _make_project(tmp_path, test_content="def test_fail():\n    assert False\n")
        proc = _build(tmp_path, "--skip-validation", "--target", "flutter")
        assert proc.returncode != 0
        combined = proc.stdout + proc.stderr
        assert "Tests failed" in combined

    def test_failing_tests_message_mentions_skip_tests(self, tmp_path):
        _make_project(tmp_path, test_content="def test_fail():\n    assert False\n")
        proc = _build(tmp_path, "--skip-validation", "--target", "flutter")
        combined = proc.stdout + proc.stderr
        assert "--skip-tests" in combined

    def test_passing_tests_allow_build(self, tmp_path):
        _make_project(tmp_path, test_content="def test_ok():\n    assert True\n")
        proc = _build(tmp_path, "--skip-validation", "--target", "flutter")
        combined = proc.stdout + proc.stderr
        assert "Tests failed" not in combined
        assert "All tests passed" in combined

    def test_no_tests_dir_warns_and_continues(self, tmp_path):
        _make_project(tmp_path, test_content=None)  # no tests/ dir
        proc = _build(tmp_path, "--skip-validation", "--target", "flutter")
        combined = proc.stdout + proc.stderr
        assert "No tests/" in combined or "skipping tests" in combined

    def test_skip_tests_bypasses_failing_tests(self, tmp_path):
        _make_project(tmp_path, test_content="def test_fail():\n    assert False\n")
        proc = _build(tmp_path, "--skip-validation", "--skip-tests", "--target", "flutter")
        combined = proc.stdout + proc.stderr
        assert "Tests failed" not in combined


# ── Ordering ─────────────────────────────────────────────────────────────────

class TestBuildOrder:
    def test_validation_runs_before_tests(self, tmp_path):
        """Syntax error in main.py → validation fires before tests run."""
        (tmp_path / "p2m.toml").write_text(_TOML)
        (tmp_path / "main.py").write_text("def create_view(\n")  # syntax error
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        (tests_dir / "__init__.py").write_text("")
        (tests_dir / "test_app.py").write_text("def test_fail():\n    assert False\n")

        proc = _build(tmp_path, "--target", "flutter")
        combined = proc.stdout + proc.stderr
        assert "Validation failed" in combined
        assert "Running unit tests" not in combined

    def test_tests_run_after_validation(self, tmp_path):
        """With passing tests, 'Running unit tests' appears after validation passes."""
        _make_project(tmp_path, test_content="def test_ok():\n    assert True\n")
        proc = _build(tmp_path, "--skip-validation", "--target", "flutter")
        combined = proc.stdout + proc.stderr
        assert "Running unit tests" in combined
        assert "All tests passed" in combined
