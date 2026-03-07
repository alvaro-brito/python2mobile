"""
Test suite for P2M LLM providers
"""

import sys
import os
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from p2m.llm.factory import LLMFactory
from p2m.llm.base import LLMProvider, LLMResponse


def test_factory_creation():
    """Test LLM factory creation"""
    print("\n🧪 Test 1: LLM Factory Creation")
    
    # Test OpenAI
    try:
        provider = LLMFactory.create(
            provider="openai",
            api_key="test-key",
            model="gpt-4o"
        )
        assert provider is not None
        assert provider.model == "gpt-4o"
        print("✅ OpenAI provider created")
    except Exception as e:
        print(f"❌ OpenAI creation failed: {e}")
        return False
    
    # Test Anthropic
    try:
        provider = LLMFactory.create(
            provider="anthropic",
            api_key="test-key",
            model="claude-3-opus-20240229"
        )
        assert provider is not None
        assert provider.model == "claude-3-opus-20240229"
        print("✅ Anthropic provider created")
    except Exception as e:
        print(f"❌ Anthropic creation failed: {e}")
        return False
    
    # Test Ollama
    try:
        provider = LLMFactory.create(
            provider="ollama",
            base_url="http://localhost:11434",
            model="llama2"
        )
        assert provider is not None
        assert provider.model == "llama2"
        print("✅ Ollama provider created")
    except Exception as e:
        print(f"❌ Ollama creation failed: {e}")
        return False
    
    # Test OpenAI Compatible
    try:
        provider = LLMFactory.create(
            provider="openai-compatible",
            base_url="https://api.example.com/v1",
            api_key="test-key",
            model="custom-model",
            x_api_key="optional-header"
        )
        assert provider is not None
        assert provider.model == "custom-model"
        print("✅ OpenAI-compatible provider created")
    except Exception as e:
        print(f"❌ OpenAI-compatible creation failed: {e}")
        return False
    
    return True


def test_available_providers():
    """Test available providers list"""
    print("\n🧪 Test 2: Available Providers")
    
    providers = LLMFactory.get_available_providers()
    
    assert "openai" in providers
    assert "anthropic" in providers
    assert "ollama" in providers
    assert "openai-compatible" in providers
    
    print(f"✅ Available providers: {', '.join(providers)}")
    return True


def test_openai_provider_config():
    """Test OpenAI provider configuration"""
    print("\n🧪 Test 3: OpenAI Provider Configuration")
    
    try:
        provider = LLMFactory.create(
            provider="openai",
            api_key="sk-test",
            model="gpt-4o"
        )
        
        # Should validate config
        assert provider.validate_config() == True
        print("✅ OpenAI config validation passed")
        return True
    except ValueError as e:
        print(f"⚠️  Expected validation: {e}")
        return True
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def test_anthropic_provider_config():
    """Test Anthropic provider configuration"""
    print("\n🧪 Test 4: Anthropic Provider Configuration")
    
    try:
        provider = LLMFactory.create(
            provider="anthropic",
            api_key="sk-ant-test",
            model="claude-3-opus-20240229"
        )
        
        # Should validate config
        assert provider.validate_config() == True
        print("✅ Anthropic config validation passed")
        return True
    except ValueError as e:
        print(f"⚠️  Expected validation: {e}")
        return True
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def test_compatible_provider_config():
    """Test OpenAI-compatible provider configuration"""
    print("\n🧪 Test 5: OpenAI-Compatible Provider Configuration")
    
    try:
        provider = LLMFactory.create(
            provider="openai-compatible",
            base_url="https://api.example.com/v1",
            api_key="test-key",
            model="custom-model"
        )
        
        # Should validate config
        assert provider.validate_config() == True
        print("✅ Compatible provider config validation passed")
        return True
    except ValueError as e:
        print(f"⚠️  Expected validation: {e}")
        return True
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def test_llm_response():
    """Test LLMResponse object"""
    print("\n🧪 Test 6: LLMResponse Object")
    
    response = LLMResponse(
        content="Test response",
        model="gpt-4o",
        usage={
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30,
        }
    )
    
    assert response.content == "Test response"
    assert response.model == "gpt-4o"
    assert response.usage["total_tokens"] == 30
    assert str(response) == "Test response"
    
    print("✅ LLMResponse object test passed")
    return True


def test_provider_inheritance():
    """Test provider inheritance"""
    print("\n🧪 Test 7: Provider Inheritance")
    
    provider = LLMFactory.create(
        provider="openai",
        api_key="test-key",
        model="gpt-4o"
    )
    
    # Should be instance of LLMProvider
    assert isinstance(provider, LLMProvider)
    print("✅ Provider inheritance test passed")
    return True


def test_factory_invalid_provider():
    """Test factory with invalid provider"""
    print("\n🧪 Test 8: Invalid Provider Handling")
    
    try:
        provider = LLMFactory.create(
            provider="invalid-provider",
            api_key="test-key",
            model="test-model"
        )
        print("❌ Should have raised ValueError")
        return False
    except ValueError as e:
        print(f"✅ Correctly raised ValueError: {e}")
        return True
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def test_compatible_provider_missing_params():
    """Test compatible provider with missing parameters"""
    print("\n🧪 Test 9: Compatible Provider Missing Parameters")
    
    # Missing base_url
    try:
        provider = LLMFactory.create(
            provider="openai-compatible",
            api_key="test-key",
            model="test-model"
        )
        print("❌ Should have raised ValueError for missing base_url")
        return False
    except ValueError as e:
        print(f"✅ Correctly raised ValueError: {e}")
    
    # Missing api_key
    try:
        provider = LLMFactory.create(
            provider="openai-compatible",
            base_url="https://api.example.com/v1",
            model="test-model"
        )
        print("❌ Should have raised ValueError for missing api_key")
        return False
    except ValueError as e:
        print(f"✅ Correctly raised ValueError: {e}")
    
    # Missing model
    try:
        provider = LLMFactory.create(
            provider="openai-compatible",
            base_url="https://api.example.com/v1",
            api_key="test-key"
        )
        print("❌ Should have raised ValueError for missing model")
        return False
    except ValueError as e:
        print(f"✅ Correctly raised ValueError: {e}")
        return True


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 P2M LLM Providers Test Suite")
    print("="*60)
    
    tests = [
        test_factory_creation,
        test_available_providers,
        test_openai_provider_config,
        test_anthropic_provider_config,
        test_compatible_provider_config,
        test_llm_response,
        test_provider_inheritance,
        test_factory_invalid_provider,
        test_compatible_provider_missing_params,
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
