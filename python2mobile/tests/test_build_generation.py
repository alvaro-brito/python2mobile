"""
Tests for p2m build code generation.

Validates that CodeGenerator produces correct output files for all supported
platforms (Flutter, React Native, Web, Android, iOS) using the real test apps
from tests-p2m/.

Coverage:
- Project file loading from multi-directory app structures
- Output file existence and structure for each target
- Key content assertions per platform
- generate() dispatcher with valid/invalid targets
- All 5 targets against both todo_app and ecommerce_app
"""

import sys
import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

# Framework path
FRAMEWORK_PATH = Path(__file__).parent.parent
TESTS_P2M_PATH = FRAMEWORK_PATH.parent / "tests-p2m"

if str(FRAMEWORK_PATH) not in sys.path:
    sys.path.insert(0, str(FRAMEWORK_PATH))

from p2m.build.generator import CodeGenerator


# ──────────────────────────────────────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def generator():
    """CodeGenerator instance with a mocked LLM provider (not used for generation)."""
    with patch("p2m.build.generator.LLMFactory") as mock_factory:
        mock_factory.create.return_value = MagicMock()
        config = MagicMock()
        config.llm.provider = "openai"
        config.llm.api_key = "test-key"
        config.llm.model = "gpt-4o"
        config.llm.base_url = ""
        config.llm.x_api_key = ""
        gen = CodeGenerator(config)
    return gen


@pytest.fixture
def todo_files(generator):
    """Python files loaded from tests-p2m/todo_app."""
    return generator.load_project_files(str(TESTS_P2M_PATH / "todo_app"))


@pytest.fixture
def ecommerce_files(generator):
    """Python files loaded from tests-p2m/ecommerce_app."""
    return generator.load_project_files(str(TESTS_P2M_PATH / "ecommerce_app"))


@pytest.fixture
def outdir():
    """Fresh temporary directory for each test's build output."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


# ──────────────────────────────────────────────────────────────────────────────
# Project file loading
# ──────────────────────────────────────────────────────────────────────────────

class TestProjectFileLoading:
    """load_project_files() behavior."""

    def test_loads_main_py_todo(self, generator):
        """todo_app: main.py at the project root is loaded."""
        files = generator.load_project_files(str(TESTS_P2M_PATH / "todo_app"))
        assert "main.py" in files

    def test_loads_main_py_ecommerce(self, generator):
        """ecommerce_app: main.py at the project root is loaded."""
        files = generator.load_project_files(str(TESTS_P2M_PATH / "ecommerce_app"))
        assert "main.py" in files

    def test_todo_main_has_create_view(self, generator):
        """todo_app/main.py contains the create_view function."""
        files = generator.load_project_files(str(TESTS_P2M_PATH / "todo_app"))
        assert "create_view" in files["main.py"]

    def test_todo_main_has_event_handlers(self, generator):
        """todo_app/main.py registers handlers: add_todo, clear_done, nav_go."""
        files = generator.load_project_files(str(TESTS_P2M_PATH / "todo_app"))
        assert "add_todo" in files["main.py"]
        assert "clear_done" in files["main.py"]
        assert "nav_go" in files["main.py"]

    def test_ecommerce_main_has_handlers(self, generator):
        """ecommerce_app/main.py registers search, cart, checkout handlers."""
        files = generator.load_project_files(str(TESTS_P2M_PATH / "ecommerce_app"))
        assert "search_products" in files["main.py"]
        assert "confirm_order" in files["main.py"]
        assert "nav_checkout" in files["main.py"]

    def test_returns_dict_of_strings(self, generator):
        """load_project_files returns Dict[str, str]."""
        files = generator.load_project_files(str(TESTS_P2M_PATH / "todo_app"))
        assert isinstance(files, dict)
        for key, value in files.items():
            assert isinstance(key, str)
            assert isinstance(value, str)

    def test_ignores_test_prefix_files(self, generator, tmp_path):
        """Files starting with 'test_' are excluded."""
        (tmp_path / "main.py").write_text("# app")
        (tmp_path / "test_unit.py").write_text("# test")
        files = generator.load_project_files(str(tmp_path))
        assert "main.py" in files
        assert "test_unit.py" not in files

    def test_loads_subdirectory_py_files(self, generator):
        """
        load_project_files recursively loads all .py files from subdirectories
        including state/, views/, and components/.
        """
        files = generator.load_project_files(str(TESTS_P2M_PATH / "todo_app"))
        # main.py at root plus subdirectory module files
        assert "main.py" in files
        # At least one subdirectory file should be loaded
        subdirectory_files = [k for k in files.keys() if "/" in k or "\\" in k]
        assert len(subdirectory_files) > 0, "Expected subdirectory .py files to be loaded"

    def test_ecommerce_loads_subdirectory_files(self, generator):
        """ecommerce_app subdirectory files (state/, views/, components/) are loaded."""
        files = generator.load_project_files(str(TESTS_P2M_PATH / "ecommerce_app"))
        assert "main.py" in files
        subdirectory_files = [k for k in files.keys() if "/" in k or "\\" in k]
        assert len(subdirectory_files) > 0, "Expected subdirectory .py files to be loaded"

    def test_multiple_root_py_files(self, generator, tmp_path):
        """Multiple root-level .py files are all loaded."""
        (tmp_path / "main.py").write_text("# main")
        (tmp_path / "utils.py").write_text("# utils")
        (tmp_path / "config.py").write_text("# config")
        files = generator.load_project_files(str(tmp_path))
        assert "main.py" in files
        assert "utils.py" in files
        assert "config.py" in files

    def test_empty_project_dir(self, generator, tmp_path):
        """Empty directory returns an empty dict."""
        files = generator.load_project_files(str(tmp_path))
        assert files == {}


# ──────────────────────────────────────────────────────────────────────────────
# Flutter generation
# ──────────────────────────────────────────────────────────────────────────────

class TestFlutterGeneration:
    """generate_flutter() / generate('flutter', ...) output validation."""

    def test_creates_pubspec_yaml(self, generator, todo_files, outdir):
        generator.generate_flutter(todo_files, str(outdir))
        assert (outdir / "pubspec.yaml").exists()

    def test_creates_lib_main_dart(self, generator, todo_files, outdir):
        generator.generate_flutter(todo_files, str(outdir))
        assert (outdir / "lib" / "main.dart").exists()

    def test_pubspec_has_flutter_sdk(self, generator, todo_files, outdir):
        generator.generate_flutter(todo_files, str(outdir))
        content = (outdir / "pubspec.yaml").read_text()
        assert "flutter:" in content
        assert "sdk: flutter" in content

    def test_pubspec_has_http(self, generator, todo_files, outdir):
        generator.generate_flutter(todo_files, str(outdir))
        content = (outdir / "pubspec.yaml").read_text()
        assert "http:" in content

    def test_pubspec_has_shared_preferences(self, generator, todo_files, outdir):
        generator.generate_flutter(todo_files, str(outdir))
        content = (outdir / "pubspec.yaml").read_text()
        assert "shared_preferences:" in content

    def test_pubspec_has_valid_app_name(self, generator, todo_files, outdir):
        generator.generate_flutter(todo_files, str(outdir))
        content = (outdir / "pubspec.yaml").read_text()
        assert "name: p2m_app" in content

    def test_main_dart_imports_flutter(self, generator, todo_files, outdir):
        generator.generate_flutter(todo_files, str(outdir))
        content = (outdir / "lib" / "main.dart").read_text()
        assert "import 'package:flutter/material.dart'" in content

    def test_main_dart_has_main_entry(self, generator, todo_files, outdir):
        generator.generate_flutter(todo_files, str(outdir))
        content = (outdir / "lib" / "main.dart").read_text()
        assert "void main()" in content
        assert "runApp" in content

    def test_main_dart_has_material_app(self, generator, todo_files, outdir):
        generator.generate_flutter(todo_files, str(outdir))
        content = (outdir / "lib" / "main.dart").read_text()
        assert "MaterialApp" in content

    def test_main_dart_has_stateful_widget(self, generator, todo_files, outdir):
        generator.generate_flutter(todo_files, str(outdir))
        content = (outdir / "lib" / "main.dart").read_text()
        assert "StatefulWidget" in content

    def test_main_dart_has_build_method(self, generator, todo_files, outdir):
        generator.generate_flutter(todo_files, str(outdir))
        content = (outdir / "lib" / "main.dart").read_text()
        assert "Widget build(BuildContext context)" in content

    def test_flutter_ecommerce(self, generator, ecommerce_files, outdir):
        """Flutter generation works for ecommerce_app too."""
        generator.generate_flutter(ecommerce_files, str(outdir))
        assert (outdir / "pubspec.yaml").exists()
        assert (outdir / "lib" / "main.dart").exists()

    def test_output_dir_created_if_missing(self, generator, todo_files, tmp_path):
        """generate_flutter creates the output directory if it does not exist."""
        nested = tmp_path / "deep" / "nested" / "build"
        generator.generate_flutter(todo_files, str(nested))
        assert nested.exists()


# ──────────────────────────────────────────────────────────────────────────────
# React Native generation
# ──────────────────────────────────────────────────────────────────────────────

class TestReactNativeGeneration:
    """generate_react_native() / generate('react-native', ...) output validation."""

    def test_creates_package_json(self, generator, todo_files, outdir):
        generator.generate_react_native(todo_files, str(outdir))
        assert (outdir / "package.json").exists()

    def test_creates_app_tsx(self, generator, todo_files, outdir):
        generator.generate_react_native(todo_files, str(outdir))
        assert (outdir / "App.tsx").exists()

    def test_package_json_valid_json(self, generator, todo_files, outdir):
        generator.generate_react_native(todo_files, str(outdir))
        content = json.loads((outdir / "package.json").read_text())
        assert isinstance(content, dict)

    def test_package_json_has_react_native(self, generator, todo_files, outdir):
        generator.generate_react_native(todo_files, str(outdir))
        content = json.loads((outdir / "package.json").read_text())
        assert "react-native" in content["dependencies"]

    def test_package_json_has_react(self, generator, todo_files, outdir):
        generator.generate_react_native(todo_files, str(outdir))
        content = json.loads((outdir / "package.json").read_text())
        assert "react" in content["dependencies"]

    def test_package_json_has_typescript_devdep(self, generator, todo_files, outdir):
        generator.generate_react_native(todo_files, str(outdir))
        content = json.loads((outdir / "package.json").read_text())
        assert "typescript" in content["devDependencies"]

    def test_package_json_scripts(self, generator, todo_files, outdir):
        generator.generate_react_native(todo_files, str(outdir))
        content = json.loads((outdir / "package.json").read_text())
        assert "start" in content["scripts"]
        assert "android" in content["scripts"]
        assert "ios" in content["scripts"]

    def test_app_tsx_imports_react(self, generator, todo_files, outdir):
        generator.generate_react_native(todo_files, str(outdir))
        content = (outdir / "App.tsx").read_text()
        assert "import React" in content

    def test_app_tsx_imports_react_native(self, generator, todo_files, outdir):
        generator.generate_react_native(todo_files, str(outdir))
        content = (outdir / "App.tsx").read_text()
        assert "react-native" in content

    def test_app_tsx_default_export(self, generator, todo_files, outdir):
        generator.generate_react_native(todo_files, str(outdir))
        content = (outdir / "App.tsx").read_text()
        assert "export default" in content

    def test_app_tsx_safe_area_view(self, generator, todo_files, outdir):
        generator.generate_react_native(todo_files, str(outdir))
        content = (outdir / "App.tsx").read_text()
        assert "SafeAreaView" in content

    def test_rn_ecommerce(self, generator, ecommerce_files, outdir):
        """React Native generation works for ecommerce_app."""
        generator.generate_react_native(ecommerce_files, str(outdir))
        assert (outdir / "App.tsx").exists()
        content = json.loads((outdir / "package.json").read_text())
        assert "react-native" in content["dependencies"]


# ──────────────────────────────────────────────────────────────────────────────
# Web generation
# ──────────────────────────────────────────────────────────────────────────────

class TestWebGeneration:
    """generate_web() / generate('web', ...) output validation."""

    def test_creates_index_html(self, generator, todo_files, outdir):
        generator.generate_web(todo_files, str(outdir))
        assert (outdir / "index.html").exists()

    def test_index_html_doctype(self, generator, todo_files, outdir):
        generator.generate_web(todo_files, str(outdir))
        content = (outdir / "index.html").read_text()
        assert "<!DOCTYPE html>" in content

    def test_index_html_structure(self, generator, todo_files, outdir):
        generator.generate_web(todo_files, str(outdir))
        content = (outdir / "index.html").read_text()
        assert "<html" in content
        assert "</html>" in content
        assert "<head" in content
        assert "<body" in content

    def test_index_html_charset(self, generator, todo_files, outdir):
        generator.generate_web(todo_files, str(outdir))
        content = (outdir / "index.html").read_text()
        assert "charset" in content.lower()

    def test_index_html_viewport_meta(self, generator, todo_files, outdir):
        generator.generate_web(todo_files, str(outdir))
        content = (outdir / "index.html").read_text()
        assert "viewport" in content

    def test_index_html_python2mobile_brand(self, generator, todo_files, outdir):
        generator.generate_web(todo_files, str(outdir))
        content = (outdir / "index.html").read_text()
        assert "Python2Mobile" in content

    def test_index_html_has_script(self, generator, todo_files, outdir):
        generator.generate_web(todo_files, str(outdir))
        content = (outdir / "index.html").read_text()
        assert "<script" in content

    def test_index_html_has_style(self, generator, todo_files, outdir):
        generator.generate_web(todo_files, str(outdir))
        content = (outdir / "index.html").read_text()
        assert "<style" in content

    def test_web_ecommerce(self, generator, ecommerce_files, outdir):
        """Web generation works for ecommerce_app."""
        generator.generate_web(ecommerce_files, str(outdir))
        assert (outdir / "index.html").exists()


# ──────────────────────────────────────────────────────────────────────────────
# Android generation
# ──────────────────────────────────────────────────────────────────────────────

class TestAndroidGeneration:
    """generate_android() / generate('android', ...) output validation."""

    def test_creates_build_gradle(self, generator, todo_files, outdir):
        generator.generate_android(todo_files, str(outdir))
        assert (outdir / "build.gradle").exists()

    def test_creates_android_manifest(self, generator, todo_files, outdir):
        generator.generate_android(todo_files, str(outdir))
        assert (outdir / "AndroidManifest.xml").exists()

    def test_creates_main_activity_kt(self, generator, todo_files, outdir):
        generator.generate_android(todo_files, str(outdir))
        assert (outdir / "MainActivity.kt").exists()

    def test_creates_activity_main_xml(self, generator, todo_files, outdir):
        generator.generate_android(todo_files, str(outdir))
        assert (outdir / "activity_main.xml").exists()

    def test_manifest_has_internet_permission(self, generator, todo_files, outdir):
        generator.generate_android(todo_files, str(outdir))
        content = (outdir / "AndroidManifest.xml").read_text()
        assert "android.permission.INTERNET" in content

    def test_manifest_has_main_activity(self, generator, todo_files, outdir):
        generator.generate_android(todo_files, str(outdir))
        content = (outdir / "AndroidManifest.xml").read_text()
        assert "MainActivity" in content
        assert "android.intent.action.MAIN" in content

    def test_manifest_has_package(self, generator, todo_files, outdir):
        generator.generate_android(todo_files, str(outdir))
        content = (outdir / "AndroidManifest.xml").read_text()
        assert 'package="com.p2m.app"' in content

    def test_main_activity_package(self, generator, todo_files, outdir):
        generator.generate_android(todo_files, str(outdir))
        content = (outdir / "MainActivity.kt").read_text()
        assert "package com.p2m.app" in content

    def test_main_activity_class(self, generator, todo_files, outdir):
        generator.generate_android(todo_files, str(outdir))
        content = (outdir / "MainActivity.kt").read_text()
        assert "class MainActivity" in content
        assert "AppCompatActivity" in content

    def test_main_activity_on_create(self, generator, todo_files, outdir):
        generator.generate_android(todo_files, str(outdir))
        content = (outdir / "MainActivity.kt").read_text()
        assert "onCreate" in content

    def test_build_gradle_kotlin_android(self, generator, todo_files, outdir):
        generator.generate_android(todo_files, str(outdir))
        content = (outdir / "build.gradle").read_text()
        assert "kotlin-android" in content

    def test_build_gradle_compile_sdk(self, generator, todo_files, outdir):
        generator.generate_android(todo_files, str(outdir))
        content = (outdir / "build.gradle").read_text()
        assert "compileSdk" in content

    def test_build_gradle_appcompat(self, generator, todo_files, outdir):
        generator.generate_android(todo_files, str(outdir))
        content = (outdir / "build.gradle").read_text()
        assert "appcompat" in content

    def test_layout_xml_is_valid(self, generator, todo_files, outdir):
        generator.generate_android(todo_files, str(outdir))
        content = (outdir / "activity_main.xml").read_text()
        assert '<?xml version="1.0"' in content
        assert "layout_width" in content

    def test_android_ecommerce(self, generator, ecommerce_files, outdir):
        """Android generation works for ecommerce_app."""
        generator.generate_android(ecommerce_files, str(outdir))
        assert (outdir / "MainActivity.kt").exists()
        assert (outdir / "AndroidManifest.xml").exists()


# ──────────────────────────────────────────────────────────────────────────────
# iOS generation
# ──────────────────────────────────────────────────────────────────────────────

class TestIOSGeneration:
    """generate_ios() / generate('ios', ...) output validation."""

    def test_creates_package_swift(self, generator, todo_files, outdir):
        generator.generate_ios(todo_files, str(outdir))
        assert (outdir / "Package.swift").exists()

    def test_creates_content_view_swift(self, generator, todo_files, outdir):
        generator.generate_ios(todo_files, str(outdir))
        assert (outdir / "ContentView.swift").exists()

    def test_creates_app_swift(self, generator, todo_files, outdir):
        generator.generate_ios(todo_files, str(outdir))
        assert (outdir / "App.swift").exists()

    def test_package_swift_targets_ios14(self, generator, todo_files, outdir):
        generator.generate_ios(todo_files, str(outdir))
        content = (outdir / "Package.swift").read_text()
        assert ".iOS(.v14)" in content

    def test_package_swift_has_swift_tools_version(self, generator, todo_files, outdir):
        generator.generate_ios(todo_files, str(outdir))
        content = (outdir / "Package.swift").read_text()
        assert "swift-tools-version" in content

    def test_content_view_imports_swiftui(self, generator, todo_files, outdir):
        generator.generate_ios(todo_files, str(outdir))
        content = (outdir / "ContentView.swift").read_text()
        assert "import SwiftUI" in content

    def test_content_view_struct(self, generator, todo_files, outdir):
        generator.generate_ios(todo_files, str(outdir))
        content = (outdir / "ContentView.swift").read_text()
        assert "struct ContentView" in content

    def test_content_view_body_property(self, generator, todo_files, outdir):
        generator.generate_ios(todo_files, str(outdir))
        content = (outdir / "ContentView.swift").read_text()
        assert "var body: some View" in content

    def test_content_view_has_state(self, generator, todo_files, outdir):
        generator.generate_ios(todo_files, str(outdir))
        content = (outdir / "ContentView.swift").read_text()
        assert "@State" in content

    def test_app_swift_has_main_attribute(self, generator, todo_files, outdir):
        generator.generate_ios(todo_files, str(outdir))
        content = (outdir / "App.swift").read_text()
        assert "@main" in content

    def test_app_swift_imports_swiftui(self, generator, todo_files, outdir):
        generator.generate_ios(todo_files, str(outdir))
        content = (outdir / "App.swift").read_text()
        assert "import SwiftUI" in content

    def test_app_swift_window_group(self, generator, todo_files, outdir):
        generator.generate_ios(todo_files, str(outdir))
        content = (outdir / "App.swift").read_text()
        assert "WindowGroup" in content

    def test_ios_ecommerce(self, generator, ecommerce_files, outdir):
        """iOS generation works for ecommerce_app."""
        generator.generate_ios(ecommerce_files, str(outdir))
        assert (outdir / "ContentView.swift").exists()
        assert (outdir / "App.swift").exists()


# ──────────────────────────────────────────────────────────────────────────────
# generate() dispatcher
# ──────────────────────────────────────────────────────────────────────────────

class TestGenerateDispatcher:
    """The generate() method routes to the correct target generator."""

    def test_flutter(self, generator, todo_files, outdir):
        generator.generate("flutter", todo_files, str(outdir))
        assert (outdir / "pubspec.yaml").exists()

    def test_react_native(self, generator, todo_files, outdir):
        generator.generate("react-native", todo_files, str(outdir))
        assert (outdir / "App.tsx").exists()

    def test_web(self, generator, todo_files, outdir):
        generator.generate("web", todo_files, str(outdir))
        assert (outdir / "index.html").exists()

    def test_android(self, generator, todo_files, outdir):
        generator.generate("android", todo_files, str(outdir))
        assert (outdir / "MainActivity.kt").exists()

    def test_ios(self, generator, todo_files, outdir):
        generator.generate("ios", todo_files, str(outdir))
        assert (outdir / "ContentView.swift").exists()

    def test_invalid_target_raises_value_error(self, generator, todo_files, outdir):
        with pytest.raises(ValueError, match="Unsupported target"):
            generator.generate("xamarin", todo_files, str(outdir))

    def test_unsupported_target_message_includes_target(self, generator, todo_files, outdir):
        with pytest.raises(ValueError, match="xamarin"):
            generator.generate("xamarin", todo_files, str(outdir))

    def test_case_insensitive_flutter(self, generator, todo_files, outdir):
        """Target strings are lowercased before dispatch."""
        generator.generate("Flutter", todo_files, str(outdir))
        assert (outdir / "pubspec.yaml").exists()

    def test_case_insensitive_android(self, generator, todo_files, outdir):
        generator.generate("ANDROID", todo_files, str(outdir))
        assert (outdir / "MainActivity.kt").exists()

    def test_supported_targets_constant(self):
        """SUPPORTED_TARGETS lists all 5 expected platforms."""
        assert set(CodeGenerator.SUPPORTED_TARGETS) == {
            "flutter", "react-native", "web", "android", "ios"
        }


# ──────────────────────────────────────────────────────────────────────────────
# All targets × both apps
# ──────────────────────────────────────────────────────────────────────────────

class TestAllTargetsBothApps:
    """Generate all 5 targets for both todo_app and ecommerce_app."""

    @pytest.mark.parametrize("target", CodeGenerator.SUPPORTED_TARGETS)
    def test_todo_app_all_targets(self, generator, todo_files, target):
        """todo_app generates without error for every supported target."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator.generate(target, todo_files, tmpdir)
            assert len(list(Path(tmpdir).iterdir())) > 0, (
                f"No output files created for target '{target}'"
            )

    @pytest.mark.parametrize("target", CodeGenerator.SUPPORTED_TARGETS)
    def test_ecommerce_app_all_targets(self, generator, ecommerce_files, target):
        """ecommerce_app generates without error for every supported target."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator.generate(target, ecommerce_files, tmpdir)
            assert len(list(Path(tmpdir).iterdir())) > 0, (
                f"No output files created for target '{target}'"
            )

    @pytest.mark.parametrize("target,expected_file", [
        ("flutter",      "pubspec.yaml"),
        ("react-native", "App.tsx"),
        ("web",          "index.html"),
        ("android",      "MainActivity.kt"),
        ("ios",          "ContentView.swift"),
    ])
    def test_key_output_file_per_target(self, generator, todo_files, target, expected_file):
        """Each target produces its primary output file for todo_app."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator.generate(target, todo_files, tmpdir)
            # Flutter nests main.dart under lib/
            if target == "flutter":
                assert (Path(tmpdir) / "lib" / "main.dart").exists()
            else:
                assert (Path(tmpdir) / expected_file).exists()
