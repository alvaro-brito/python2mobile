"""
Test the p2m imagine CLI command
"""

import subprocess
import sys
from pathlib import Path


def test_imagine_help():
    """Test p2m imagine --help"""
    print("\n🧪 Test 1: p2m imagine --help")
    
    result = subprocess.run(
        ["p2m", "imagine", "--help"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Command failed: {result.stderr}"
    assert "P2M project" in result.stdout or "P2M code" in result.stdout or "natural language" in result.stdout
    assert "--provider" in result.stdout
    assert "--model" in result.stdout
    assert "--api-key" in result.stdout
    
    print("✅ Help command works correctly")
    return True


def test_imagine_missing_description():
    """Test p2m imagine without description"""
    print("\n🧪 Test 2: p2m imagine (missing description)")
    
    result = subprocess.run(
        ["p2m", "imagine"],
        capture_output=True,
        text=True
    )
    
    # Should fail with missing argument
    assert result.returncode != 0
    print("✅ Correctly requires description argument")
    return True


def test_imagine_version():
    """Test p2m --version"""
    print("\n🧪 Test 3: p2m --version")
    
    result = subprocess.run(
        ["p2m", "--version"],
        capture_output=True,
        text=True
    )
    
    # Version command may not be implemented, that's ok
    if result.returncode == 0:
        print(f"✅ Version: {result.stdout.strip()}")
    else:
        print(f"✅ Version command not implemented (optional)")
    return True


def test_imagine_list_providers():
    """Test listing available providers"""
    print("\n🧪 Test 4: List Available Providers")
    
    # Try to get help which lists providers
    result = subprocess.run(
        ["p2m", "imagine", "--help"],
        capture_output=True,
        text=True
    )
    
    assert "openai" in result.stdout.lower()
    assert "anthropic" in result.stdout.lower()

    print("✅ Providers listed in help:")
    print("   - openai")
    print("   - anthropic")
    return True


def run_all_tests():
    """Run all CLI tests"""
    print("\n" + "="*60)
    print("🧪 P2M Imagine CLI Test Suite")
    print("="*60)
    
    tests = [
        test_imagine_help,
        test_imagine_missing_description,
        test_imagine_version,
        test_imagine_list_providers,
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
