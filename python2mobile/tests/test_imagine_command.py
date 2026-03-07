"""
Test suite for p2m imagine command
"""

import sys
import tempfile
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from p2m.imagine.legacy import CodeImaginer
from p2m.imagine import imagine_command


def test_config_validation_openai():
    """Test OpenAI configuration validation"""
    print("\n🧪 Test 1: OpenAI Config Validation")
    
    imaginer = CodeImaginer(
        provider="openai",
        model="gpt-4o",
        api_key="sk-test"
    )
    
    valid, msg = imaginer.validate_config()
    assert valid, f"Should be valid: {msg}"
    print("✅ OpenAI config validation passed")
    return True


def test_config_validation_anthropic():
    """Test Anthropic configuration validation"""
    print("\n🧪 Test 2: Anthropic Config Validation")
    
    imaginer = CodeImaginer(
        provider="anthropic",
        model="claude-3-opus-20240229",
        api_key="sk-ant-test"
    )
    
    valid, msg = imaginer.validate_config()
    assert valid, f"Should be valid: {msg}"
    print("✅ Anthropic config validation passed")
    return True


def test_config_validation_ollama():
    """Test Ollama configuration validation"""
    print("\n🧪 Test 3: Ollama Config Validation")
    
    imaginer = CodeImaginer(
        provider="ollama",
        model="llama2",
        base_url="http://localhost:11434"
    )
    
    valid, msg = imaginer.validate_config()
    assert valid, f"Should be valid: {msg}"
    assert imaginer.base_url == "http://localhost:11434"
    print("✅ Ollama config validation passed")
    return True


def test_config_validation_compatible():
    """Test OpenAI-compatible configuration validation"""
    print("\n🧪 Test 4: OpenAI-Compatible Config Validation")
    
    imaginer = CodeImaginer(
        provider="openai-compatible",
        model="custom-model",
        api_key="test-key",
        base_url="https://api.example.com/v1"
    )
    
    valid, msg = imaginer.validate_config()
    assert valid, f"Should be valid: {msg}"
    print("✅ OpenAI-compatible config validation passed")
    return True


def test_missing_api_key():
    """Test missing API key validation"""
    print("\n🧪 Test 5: Missing API Key Validation")
    
    imaginer = CodeImaginer(
        provider="openai",
        model="gpt-4o",
        api_key=None  # No API key
    )
    
    # Clear environment variable if set
    import os
    old_key = os.environ.pop("OPENAI_API_KEY", None)
    
    try:
        valid, msg = imaginer.validate_config()
        assert not valid, "Should be invalid without API key"
        assert "OPENAI_API_KEY" in msg
        print(f"✅ Correctly detected missing API key: {msg}")
        return True
    finally:
        if old_key:
            os.environ["OPENAI_API_KEY"] = old_key


def test_missing_base_url():
    """Test missing base URL validation"""
    print("\n🧪 Test 6: Missing Base URL Validation")
    
    imaginer = CodeImaginer(
        provider="openai-compatible",
        model="custom-model",
        api_key="test-key",
        base_url=None  # No base URL
    )
    
    valid, msg = imaginer.validate_config()
    assert not valid, "Should be invalid without base_url"
    assert "base-url" in msg.lower()
    print(f"✅ Correctly detected missing base_url: {msg}")
    return True


def test_code_validation_valid():
    """Test code validation with valid code"""
    print("\n🧪 Test 7: Code Validation - Valid Code")
    
    valid_code = '''from p2m.core import Render
from p2m.ui import Container, Text

def create_view():
    container = Container(class_="bg-white p-4")
    text = Text("Hello World", class_="text-lg")
    container.add(text)
    return container.build()

def main():
    Render.execute(create_view)

if __name__ == "__main__":
    main()
'''
    
    imaginer = CodeImaginer(
        provider="openai",
        model="gpt-4o",
        api_key="test"
    )
    
    valid, msg = imaginer.validate_code(valid_code)
    assert valid, f"Should be valid: {msg}"
    print("✅ Valid code passed validation")
    return True


def test_code_validation_syntax_error():
    """Test code validation with syntax error"""
    print("\n🧪 Test 8: Code Validation - Syntax Error")
    
    invalid_code = '''from p2m.core import Render
from p2m.ui import Container, Text

def create_view(
    # Missing closing parenthesis
    container = Container()
'''
    
    imaginer = CodeImaginer(
        provider="openai",
        model="gpt-4o",
        api_key="test"
    )
    
    valid, msg = imaginer.validate_code(invalid_code)
    assert not valid, "Should be invalid due to syntax error"
    assert "Syntax error" in msg
    print(f"✅ Correctly detected syntax error: {msg}")
    return True


def test_code_validation_missing_imports():
    """Test code validation with missing imports"""
    print("\n🧪 Test 9: Code Validation - Missing Imports")
    
    invalid_code = '''def create_view():
    container = Container()
    return container.build()
'''
    
    imaginer = CodeImaginer(
        provider="openai",
        model="gpt-4o",
        api_key="test"
    )
    
    valid, msg = imaginer.validate_code(invalid_code)
    assert not valid, "Should be invalid without p2m imports"
    assert "import from p2m" in msg.lower()
    print(f"✅ Correctly detected missing imports: {msg}")
    return True


def test_code_validation_missing_create_view():
    """Test code validation with missing create_view"""
    print("\n🧪 Test 10: Code Validation - Missing create_view")
    
    invalid_code = '''from p2m.core import Render
from p2m.ui import Container, Text

def main():
    print("Hello")
'''
    
    imaginer = CodeImaginer(
        provider="openai",
        model="gpt-4o",
        api_key="test"
    )
    
    valid, msg = imaginer.validate_code(invalid_code)
    assert not valid, "Should be invalid without create_view"
    assert "create_view" in msg
    print(f"✅ Correctly detected missing create_view: {msg}")
    return True


def test_save_code():
    """Test saving generated code"""
    print("\n🧪 Test 11: Save Generated Code")
    
    code = '''from p2m.core import Render
from p2m.ui import Container, Text

def create_view():
    container = Container(class_="bg-white p-4")
    text = Text("Hello World", class_="text-lg")
    container.add(text)
    return container.build()
'''
    
    imaginer = CodeImaginer(
        provider="openai",
        model="gpt-4o",
        api_key="test"
    )
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = Path(tmpdir) / "test_app.py"
        success, filepath = imaginer.save_code(code, str(output_file))
        
        assert success, f"Should save successfully: {filepath}"
        assert Path(filepath).exists(), "File should exist"
        
        # Verify content
        saved_code = Path(filepath).read_text()
        assert "create_view" in saved_code
        assert "Container" in saved_code
        
        print(f"✅ Code saved successfully to {filepath}")
    
    return True


def test_provider_creation():
    """Test LLM provider creation"""
    print("\n🧪 Test 12: LLM Provider Creation")
    
    imaginer = CodeImaginer(
        provider="openai",
        model="gpt-4o",
        api_key="sk-test"
    )
    
    imaginer.validate_config()
    success, msg = imaginer.create_provider()
    
    assert success, f"Should create provider: {msg}"
    assert imaginer.llm is not None
    print(f"✅ Provider created successfully: {msg}")
    return True


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 P2M Imagine Command Test Suite")
    print("="*60)
    
    tests = [
        test_config_validation_openai,
        test_config_validation_anthropic,
        test_config_validation_ollama,
        test_config_validation_compatible,
        test_missing_api_key,
        test_missing_base_url,
        test_code_validation_valid,
        test_code_validation_syntax_error,
        test_code_validation_missing_imports,
        test_code_validation_missing_create_view,
        test_save_code,
        test_provider_creation,
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
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
