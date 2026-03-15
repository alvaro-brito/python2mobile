"""
P2M CLI - Command-line interface
"""

import click
import os
from pathlib import Path
from p2m.config import Config
from p2m.core.runtime import Render
from p2m.core.render_engine import RenderEngine
from p2m.core.validator import CodeValidator
from p2m.build.generator import CodeGenerator
from p2m.build.agent_generator import AgentCodeGenerator, agent_available, print_run_instructions
from p2m.imagine import imagine_command, run_imagine_agent, agent_available as imagine_agent_available
import sys


@click.group()
def cli():
    """Python2Mobile - Write mobile apps in pure Python"""
    pass


@cli.command()
@click.option("--port", default=None, type=int, help="Dev server port (default: from p2m.toml or 3000)")
@click.option("--no-frame", is_flag=True, help="Disable mobile frame")
@click.option("--skip-validation", is_flag=True, help="Skip code validation")
def run(port: int, no_frame: bool, skip_validation: bool):
    """Run app in development mode with hot reload"""

    click.echo("🚀 Python2Mobile Dev Server")

    # Load config
    config = Config()

    # Port priority: CLI flag > p2m.toml > default 3000
    if port is None:
        port = config.devserver.port

    # Validate code before running
    if not skip_validation:
        click.echo("🔍 Validating code...")
        validator = CodeValidator()
        is_valid, errors, warnings = validator.validate_project(".", entry_file=config.project.entry)
        
        if errors:
            click.echo("\n❌ Validation failed:")
            for error in errors:
                click.echo(f"   {error}")
            click.echo("\n💡 Fix the errors above or use --skip-validation to ignore", err=True)
            return
        
        if warnings:
            click.echo(f"\n⚠️  {len(warnings)} warning(s) found:")
            for warning in warnings:
                click.echo(f"   {warning}")
        
        if not errors:
            click.echo("✅ Code validation passed\n")
    
    click.echo(f"📱 Starting on http://localhost:{port}")

    # Load and execute the entry point
    entry_file = config.project.entry

    if not Path(entry_file).exists():
        click.echo(f"❌ Entry file not found: {entry_file}", err=True)
        return

    try:
        import sys
        import importlib.util

        # Add project directory to sys.path so multi-file imports work
        project_dir = str(Path(entry_file).parent.absolute())
        if project_dir not in sys.path:
            sys.path.insert(0, project_dir)

        # Load the app module
        spec = importlib.util.spec_from_file_location("p2m_app", entry_file)
        module = importlib.util.module_from_spec(spec)
        sys.modules["p2m_app"] = module
        spec.loader.exec_module(module)

        # Ensure create_view exists
        if not hasattr(module, "create_view"):
            click.echo("❌ create_view() function not found in entry file", err=True)
            return

        # Initial render
        component_tree = Render.execute(module.create_view)
        engine = RenderEngine()
        html = engine.render(component_tree, mobile_frame=not no_frame)

        # Start dev server — pass view_func for live re-renders
        from p2m.devserver.server import start_server
        click.echo(f"🌐 Dev server running at http://localhost:{port}")
        click.echo(f"📱 Open in browser to see your app")
        click.echo(f"🔥 Interactive mode — events are handled server-side\n")
        start_server(html, port=port, view_func=module.create_view, project_dir=project_dir)
        
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        import traceback
        traceback.print_exc()


@cli.command()
@click.option("--target", type=click.Choice(["flutter", "react-native", "android", "ios"]),
              default="flutter", help="Build target")
@click.option("--force", is_flag=True, help="Force rebuild")
@click.option("--skip-validation", is_flag=True, help="Skip code validation")
@click.option("--skip-tests", is_flag=True, help="Skip unit tests")
@click.option("--no-agent", is_flag=True, help="Use legacy LLM generator instead of Agno agent")
@click.option("--skip-validate-fix", is_flag=True,
              help="Skip Stage 3 Validate & Fix (run toolchain + AI fixer)")
@click.option("--max-fix-iterations", default=5, show_default=True,
              help="Max number of fix cycles in Stage 3")
@click.option("--skip-preflight", is_flag=True,
              help="Skip platform prerequisite checks (flutter, swift, node, java)")
def build(target: str, force: bool, skip_validation: bool, skip_tests: bool, no_agent: bool,
          skip_validate_fix: bool, max_fix_iterations: int, skip_preflight: bool):
    """Build app for production (Flutter, React Native, Android, iOS)"""

    click.echo(f"🔨 Building for {target}...")

    # ── Platform prerequisite check ───────────────────────────────────────────
    if not skip_preflight:
        from p2m.build.preflight import check_platform, print_preflight_result
        preflight = check_platform(target)
        if preflight is not None:
            if preflight.ok:
                # Show one-line success per tool
                for c in preflight.checks:
                    ver = f" ({c.version})" if c.version else ""
                    click.echo(f"   ✅ {c.name}{ver}")
            else:
                click.echo(f"\n❌ Prerequisites missing for '{target}' — cannot build.\n")
                print_preflight_result(preflight)
                click.echo(
                    "💡 Install the missing tools above, then run `p2m build` again.\n"
                    "   (Use --skip-preflight to bypass this check.)",
                    err=True,
                )
                sys.exit(1)

    # Load config
    config = Config()

    # Validate code before building
    if not skip_validation:
        click.echo("🔍 Validating code...")
        validator = CodeValidator()
        is_valid, errors, warnings = validator.validate_project(".", entry_file=config.project.entry)

        if errors:
            click.echo("\n❌ Validation failed:")
            for error in errors:
                click.echo(f"   {error}")
            click.echo("\n💡 Fix the errors above or use --skip-validation to ignore", err=True)
            sys.exit(1)

        if warnings:
            click.echo(f"\n⚠️  {len(warnings)} warning(s) found:")
            for warning in warnings:
                click.echo(f"   {warning}")

        if not errors:
            click.echo("✅ Code validation passed\n")

    # Run unit tests before building
    if not skip_tests:
        tests_dir = Path("tests")
        if tests_dir.is_dir():
            import pytest
            click.echo("🧪 Running unit tests...")
            project_dir = str(Path(".").resolve())
            if project_dir not in sys.path:
                sys.path.insert(0, project_dir)
            result = pytest.main([str(tests_dir), "--tb=short", "-q"])
            if result != 0:
                click.echo("\n❌ Tests failed — build aborted.", err=True)
                click.echo("💡 Fix the failing tests or use --skip-tests to bypass", err=True)
                sys.exit(result)
            click.echo("✅ All tests passed\n")
        else:
            click.echo("⚠️  No tests/ directory found — skipping tests\n")

    # Create output directory
    output_dir = Path(config.build.output_dir) / target
    output_dir.mkdir(parents=True, exist_ok=True)

    # ── Agent-based generation (preferred when agno + API key are available) ──
    use_agent = (not no_agent) and agent_available(config) and target in AgentCodeGenerator.SUPPORTED_TARGETS

    if use_agent:
        click.echo(f"🤖 Using Agno agent for {target} generation...")
        try:
            agent_gen = AgentCodeGenerator(
                config,
                project_dir=".",
                validate_fix=not skip_validate_fix,
                max_fix_iterations=max_fix_iterations,
            )
            agent_gen.generate(target, str(output_dir))
            click.echo(f"✅ Build complete: {output_dir}")
            return
        except Exception as e:
            # Re-raise immediately — never silently fall back to the legacy generator.
            # The legacy generator produces incomplete output and masks real errors.
            # Fix the root cause instead.
            import traceback
            click.echo(f"❌ Agent build failed: {e}", err=True)
            click.echo(traceback.format_exc(), err=True)
            raise SystemExit(1)

    # ── Legacy LLM generator ──────────────────────────────────────────────────
    try:
        generator = CodeGenerator(config)
        project_files = generator.load_project_files(".")

        if not project_files:
            click.echo("❌ No Python files found in project", err=True)
            return

        click.echo(f"📝 Generating {target} code...")

        if target == "flutter":
            click.echo("📱 Generating Flutter (Dart) for Android/iOS...")
            generator.generate_flutter(project_files, str(output_dir))
        elif target == "react-native":
            click.echo("⚛️  Generating React Native (TypeScript)...")
            generator.generate_react_native(project_files, str(output_dir))
        elif target == "android":
            click.echo("🤖 Generating Android (Java + XML)...")
            generator.generate_android(project_files, str(output_dir))
        elif target == "ios":
            click.echo("🍎 Generating iOS (Swift)...")
            generator.generate_ios(project_files, str(output_dir))

        click.echo(f"✅ Build complete: {output_dir}")
        print_run_instructions(target, str(output_dir))

    except Exception as e:
        click.echo(f"❌ Build failed: {e}", err=True)
        import traceback
        traceback.print_exc()


@cli.command()
@click.argument("name")
def new(name: str):
    """Create a new P2M project"""
    
    click.echo(f"📦 Creating new project: {name}")
    
    project_dir = Path(name)
    project_dir.mkdir(exist_ok=True)
    
    # Create main.py
    main_py = project_dir / "main.py"
    main_py.write_text("""from p2m.core import Render
from p2m.ui import Container, Text, Button

def click_button():
    print("Button clicked!")

def create_view():
    container = Container(class_="bg-gray-100 min-h-screen flex items-center justify-center")
    inner = Container(class_="text-center space-y-6 p-8 bg-white rounded-2xl shadow-lg")
    
    text = Text("Welcome to P2M", class_="text-gray-800 text-2xl font-bold")
    button = Button(
        "Click Me",
        class_="bg-blue-600 text-white font-semibold py-3 px-8 rounded-xl hover:bg-blue-700",
        on_click=click_button
    )
    
    inner.add(text).add(button)
    container.add(inner)
    return container.build()

def main():
    Render.execute(create_view)

if __name__ == "__main__":
    main()
""")
    
    # Create p2m.toml
    toml_file = project_dir / "p2m.toml"
    toml_file.write_text(f"""[project]
name = "{name}"
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
""")
    
    click.echo(f"✅ Project created: {project_dir}")
    click.echo(f"📝 Next steps:")
    click.echo(f"   cd {name}")
    click.echo(f"   p2m run")


@cli.command()
@click.argument("description")
@click.option("--provider", default="openai", help="LLM provider: openai, anthropic")
@click.option("--model", default=None, help="Model name (defaults based on provider)")
@click.option("--api-key", default=None, help="API key (or use environment variable)")
@click.option("-n", "--name", default=None, help="Project name and output directory (snake_case)")
@click.option("--output", default=None, help="Output directory (defaults to project name)")
@click.option("--no-agent", is_flag=True, help="Use legacy single-file generator instead of agent")
@click.option("--base-url", default=None, help="Base URL for OpenAI-compatible provider")
@click.option("--x-api-key", default=None, help="Custom API key header (openai-compatible)")
@click.option("--no-validate", is_flag=True, help="Skip validation (legacy mode only)")
def imagine(description: str, provider: str, model: str, api_key: str, name: str,
            output: str, no_agent: bool, base_url: str, x_api_key: str,
            no_validate: bool):
    """Generate a complete P2M project from a natural language description"""

    import re

    click.echo("🎨 Python2Mobile Imagine")
    click.echo(f"📝 Description: {description}\n")

    use_agent = not no_agent and imagine_agent_available(provider, api_key)

    if use_agent:
        # ── Resolve project name ──────────────────────────────────────────────
        if name:
            # Sanitise: lowercase, replace spaces/hyphens with underscores
            project_name = re.sub(r"[^a-z0-9_]", "_", name.strip().lower()).strip("_") or "p2m_app"
        elif output:
            project_name = re.sub(r"[^a-z0-9_]", "_", output.strip().lower()).strip("_") or "p2m_app"
        else:
            # Prompt user — no spaces allowed
            while True:
                raw = click.prompt("Project name (snake_case, no spaces)")
                project_name = re.sub(r"[^a-z0-9_]", "_", raw.strip().lower()).strip("_")
                if project_name:
                    if project_name != raw.strip():
                        click.echo(f"  → Sanitised to: {project_name}")
                    break
                click.echo("  Name cannot be empty. Try again.")

        output_dir = output or project_name

        click.echo(f"🤖 Using Agno agent ({provider})...")
        click.echo(f"   Project name : {project_name}")
        click.echo(f"   Output dir   : {output_dir}\n")

        Path(output_dir).mkdir(parents=True, exist_ok=True)

        try:
            run_imagine_agent(
                description=description,
                output_dir=output_dir,
                project_name=project_name,
                model_provider=provider,
                model_name=model,
                api_key=api_key,
            )
        except (ImportError, RuntimeError) as exc:
            click.echo(f"❌ Agent error: {exc}", err=True)
            sys.exit(1)

        # ── Validate + auto-fix loop (up to 5 iterations) ───────────────
        click.echo("\n🔧 Running design validator + code fixer...")
        from p2m.imagine.design_validator import validate_and_fix_loop, summarise_business_notes
        validate_and_fix_loop(
            output_dir,
            model_provider=provider,
            model_name=model,
            api_key=api_key,
            max_iterations=5,
            verbose=True,
        )

        # ── Business notes — show credentials, sample data, etc. ─────────
        notes = summarise_business_notes(output_dir)
        if notes:
            click.echo("\n📋 App notes (business particularities):")
            for note in notes:
                click.echo(f"   {note}")

        click.echo(f"\n✅ Project generated in: {output_dir}/")
        click.echo(f"\n💡 Next steps:")
        click.echo(f"   cd {output_dir}")
        click.echo(f"   p2m run")
        click.echo(f"   p2m test tests/")
        click.echo(f"   p2m build --target flutter")

    else:
        # ── Legacy mode: single generated_app.py ────────────────────────────
        if not no_agent:
            click.echo("ℹ️  agno not installed or API key missing — using legacy generator.")
            click.echo("   Install agno and set OPENAI_API_KEY for full project generation.\n")

        output_file = output or "generated_app.py"

        success, message, code = imagine_command(
            description=description,
            provider=provider,
            model=model,
            api_key=api_key,
            base_url=base_url,
            x_api_key=x_api_key,
            output=output_file,
            validate=not no_validate,
        )

        if success:
            click.echo(f"\n✅ {message}")
            click.echo(f"\n📋 Generated code preview:")
            click.echo("─" * 60)
            if code:
                lines = code.split("\n")
                for line in lines[:20]:
                    click.echo(line)
                if len(lines) > 20:
                    click.echo(f"... ({len(lines) - 20} more lines)")
            click.echo("─" * 60)
            click.echo(f"\n💡 Next steps:")
            click.echo(f"   1. Review the generated code: {output_file}")
            click.echo(f"   2. Run the app: p2m run {output_file}")
            click.echo(f"   3. Build for production: p2m build --target android")
        else:
            click.echo(f"❌ Error: {message}", err=True)
            if code:
                click.echo(f"\n📋 Generated code (with errors):\n{code}", err=True)
            sys.exit(1)


@cli.command()
@click.argument("path", default=".", required=False)
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
def test(path, verbose):
    """Run project tests with pytest"""
    import pytest
    project_dir = str(Path(path).resolve())
    if project_dir not in sys.path:
        sys.path.insert(0, project_dir)
    pytest_args = [path, "--tb=short"]
    if verbose:
        pytest_args.append("-v")
    click.echo(f"🧪 Running tests in {path}...")
    result = pytest.main(pytest_args)
    sys.exit(result)


@cli.command()
def info():
    """Show project information"""

    config = Config()

    click.echo("📱 Python2Mobile Project Info")
    click.echo(f"  Name: {config.project.name}")
    click.echo(f"  Version: {config.project.version}")
    click.echo(f"  Entry: {config.project.entry}")
    click.echo(f"  Build Target: {', '.join(config.build.target)}")
    click.echo(f"  Generator: {config.build.generator}")
    click.echo(f"  LLM Provider: {config.llm.provider}")
    click.echo(f"  LLM Model: {config.llm.model}")

    import p2m as _p2m
    import importlib.util as _ilu
    click.echo("")
    click.echo("🔧 Installation")
    click.echo(f"  Source  : {Path(_p2m.__file__).parent.parent}")
    click.echo(f"  Python  : {sys.executable}")
    click.echo(f"  CLI     : {_ilu.find_spec('p2m.cli').origin}")


@cli.command(name="list")
def list_installations():
    """List all p2m installations found in sys.path"""
    import importlib.util as _ilu

    click.echo("🔍 Searching for p2m installations...\n")

    seen = set()
    found = []

    for path_entry in sys.path:
        p = Path(path_entry) / "p2m" / "__init__.py"
        if p.exists():
            resolved = str(p.resolve())
            if resolved not in seen:
                seen.add(resolved)
                found.append(p.parent.parent)

    if not found:
        click.echo("  No p2m installations found in sys.path.")
        return

    import p2m as _active
    active_dir = str(Path(_active.__file__).parent.parent.resolve())

    for install_dir in found:
        marker = " ◀ active" if str(install_dir.resolve()) == active_dir else ""
        click.echo(f"  {install_dir}{marker}")

    if len(found) > 1:
        click.echo("\n💡 To switch, activate the desired virtualenv or adjust PYTHONPATH.")


def main():
    """Main CLI entry point"""
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\n\n⏸️  Interrupted by user", err=True)
        sys.exit(130)
    except Exception as e:
        click.echo(f"\n❌ Unexpected error: {e}", err=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
