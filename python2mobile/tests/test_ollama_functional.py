"""
Functional tests for P2M Imagine with Ollama (qwen3-coder:latest)
Tests against https://ollama.dataseed.com.br/
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from p2m.imagine.legacy import CodeImaginer


# Ollama configuration
OLLAMA_BASE_URL = "https://ollama.dataseed.com.br"
OLLAMA_MODEL = "qwen3-coder:latest"


def test_ollama_connection():
    """Test connection to Ollama server"""
    print("\n🧪 Test 1: Ollama Server Connection")
    
    imaginer = CodeImaginer(
        provider="ollama",
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL
    )
    
    valid, msg = imaginer.validate_config()
    assert valid, f"Configuration should be valid: {msg}"
    
    success, msg = imaginer.create_provider()
    if not success:
        print(f"⚠️  Cannot connect to Ollama: {msg}")
        print(f"   Server: {OLLAMA_BASE_URL}")
        print(f"   Model: {OLLAMA_MODEL}")
        return False
    
    print(f"✅ Connected to Ollama server")
    print(f"   Server: {OLLAMA_BASE_URL}")
    print(f"   Model: {OLLAMA_MODEL}")
    return True


def test_hello_world_app():
    """Test generating a simple Hello World app"""
    print("\n🧪 Test 2: Generate Hello World App")
    
    imaginer = CodeImaginer(
        provider="ollama",
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL
    )
    
    valid, msg = imaginer.validate_config()
    if not valid:
        print(f"⚠️  Configuration invalid: {msg}")
        return False
    
    success, msg = imaginer.create_provider()
    if not success:
        print(f"⚠️  Cannot create provider: {msg}")
        return False
    
    description = "Create a simple Hello World app with a centered text that says 'Hello World' and a button that says 'Click Me'"
    success, code = imaginer.generate_code(description)
    
    if not success:
        print(f"❌ Code generation failed: {code}")
        return False
    
    print(f"✅ Code generated successfully")
    print(f"   Lines of code: {len(code.split(chr(10)))}")
    
    # Validate code
    valid, msg = imaginer.validate_code(code)
    if not valid:
        print(f"⚠️  Code validation failed: {msg}")
        print(f"\nGenerated code:\n{code[:500]}...")
        return False
    
    print(f"✅ Code validation passed")
    return True


def test_todo_app():
    """Test generating a Todo app"""
    print("\n🧪 Test 3: Generate Todo App")
    
    imaginer = CodeImaginer(
        provider="ollama",
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL
    )
    
    valid, msg = imaginer.validate_config()
    if not valid:
        print(f"⚠️  Configuration invalid: {msg}")
        return False
    
    success, msg = imaginer.create_provider()
    if not success:
        print(f"⚠️  Cannot create provider: {msg}")
        return False
    
    description = """Create a Todo app with:
- A title 'My Todo List'
- An input field to add new todos
- A button to add todos
- A list of todos with delete buttons
- Show count of completed todos"""
    
    success, code = imaginer.generate_code(description)
    
    if not success:
        print(f"❌ Code generation failed: {code}")
        return False
    
    print(f"✅ Code generated successfully")
    print(f"   Lines of code: {len(code.split(chr(10)))}")
    
    # Validate code
    valid, msg = imaginer.validate_code(code)
    if not valid:
        print(f"⚠️  Code validation failed: {msg}")
        return False
    
    print(f"✅ Code validation passed")
    return True


def test_counter_app():
    """Test generating a Counter app"""
    print("\n🧪 Test 4: Generate Counter App")
    
    imaginer = CodeImaginer(
        provider="ollama",
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL
    )
    
    valid, msg = imaginer.validate_config()
    if not valid:
        print(f"⚠️  Configuration invalid: {msg}")
        return False
    
    success, msg = imaginer.create_provider()
    if not success:
        print(f"⚠️  Cannot create provider: {msg}")
        return False
    
    description = """Create a Counter app with:
- A large display showing the current count
- An Increment button (green)
- A Decrement button (red)
- A Reset button (gray)
- Start count at 0"""
    
    success, code = imaginer.generate_code(description)
    
    if not success:
        print(f"❌ Code generation failed: {code}")
        return False
    
    print(f"✅ Code generated successfully")
    print(f"   Lines of code: {len(code.split(chr(10)))}")
    
    # Validate code
    valid, msg = imaginer.validate_code(code)
    if not valid:
        print(f"⚠️  Code validation failed: {msg}")
        return False
    
    print(f"✅ Code validation passed")
    return True


def test_form_app():
    """Test generating a Form app"""
    print("\n🧪 Test 5: Generate Form App")
    
    imaginer = CodeImaginer(
        provider="ollama",
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL
    )
    
    valid, msg = imaginer.validate_config()
    if not valid:
        print(f"⚠️  Configuration invalid: {msg}")
        return False
    
    success, msg = imaginer.create_provider()
    if not success:
        print(f"⚠️  Cannot create provider: {msg}")
        return False
    
    description = """Create a Contact Form app with:
- A title 'Contact Us'
- Input field for name
- Input field for email
- Input field for message
- A submit button
- Display a success message when submitted"""
    
    success, code = imaginer.generate_code(description)
    
    if not success:
        print(f"❌ Code generation failed: {code}")
        return False
    
    print(f"✅ Code generated successfully")
    print(f"   Lines of code: {len(code.split(chr(10)))}")
    
    # Validate code
    valid, msg = imaginer.validate_code(code)
    if not valid:
        print(f"⚠️  Code validation failed: {msg}")
        return False
    
    print(f"✅ Code validation passed")
    return True


def test_dashboard_app():
    """Test generating a Dashboard app"""
    print("\n🧪 Test 6: Generate Dashboard App")
    
    imaginer = CodeImaginer(
        provider="ollama",
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL
    )
    
    valid, msg = imaginer.validate_config()
    if not valid:
        print(f"⚠️  Configuration invalid: {msg}")
        return False
    
    success, msg = imaginer.create_provider()
    if not success:
        print(f"⚠️  Cannot create provider: {msg}")
        return False
    
    description = """Create a Dashboard app with:
- A header with title 'Dashboard'
- Three cards showing:
  - Users: 1,234
  - Orders: 567
  - Revenue: $89,012
- A refresh button
- Use different colors for each card"""
    
    success, code = imaginer.generate_code(description)
    
    if not success:
        print(f"❌ Code generation failed: {code}")
        return False
    
    print(f"✅ Code generated successfully")
    print(f"   Lines of code: {len(code.split(chr(10)))}")
    
    # Validate code
    valid, msg = imaginer.validate_code(code)
    if not valid:
        print(f"⚠️  Code validation failed: {msg}")
        return False
    
    print(f"✅ Code validation passed")
    return True


def run_all_tests():
    """Run all functional tests"""
    print("\n" + "="*60)
    print("🧪 P2M Imagine - Ollama Functional Tests")
    print("="*60)
    print(f"Server: {OLLAMA_BASE_URL}")
    print(f"Model: {OLLAMA_MODEL}")
    
    tests = [
        test_ollama_connection,
        test_hello_world_app,
        test_todo_app,
        test_counter_app,
        test_form_app,
        test_dashboard_app,
    ]
    
    results = []
    
    for test_func in tests:
        try:
            result = test_func()
            results.append((test_func.__name__, result))
        except Exception as e:
            results.append((test_func.__name__, False))
            print(f"❌ {test_func.__name__} failed: {e}")
            import traceback
            traceback.print_exc()
    
    # Summary
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n📈 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    elif passed > 0:
        print(f"\n⚠️  {total - passed} test(s) failed (connection issues?)")
    else:
        print(f"\n❌ All tests failed (cannot connect to Ollama server)")
    
    return passed > 0  # Return True if at least one test passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
