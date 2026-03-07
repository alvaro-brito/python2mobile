"""
Test suite for P2M configuration system
"""

import sys
import tempfile
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from p2m.config import Config, ProjectConfig, BuildConfig, DevServerConfig, StyleConfig, LLMConfig


def test_default_config():
    """Test default configuration"""
    print("\n🧪 Test 1: Default Configuration")
    
    try:
        config = Config()
        
        assert config.project is not None
        assert config.project.name == "MyApp"
        assert config.project.version == "0.1.0"
        assert config.project.entry == "main.py"
        
        assert config.build is not None
        assert config.build.generator == "flutter"
        assert config.build.llm_provider == "openai"
        
        assert config.devserver is not None
        assert config.devserver.port == 3000
        assert config.devserver.hot_reload == True
        
        print("✅ Default config test passed")
        return True
    except Exception as e:
        print(f"❌ Default config test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config_save_and_load():
    """Test saving and loading configuration"""
    print("\n🧪 Test 2: Config Save and Load")
    
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "p2m.toml"
            
            # Create and save config
            config = Config()
            config.project.name = "TestApp"
            config.project.version = "1.0.0"
            config.build.generator = "react-native"
            config.save(str(config_path))
            
            assert config_path.exists()
            
            # Load config
            loaded_config = Config(str(config_path))
            
            assert loaded_config.project.name == "TestApp"
            assert loaded_config.project.version == "1.0.0"
            assert loaded_config.build.generator == "react-native"
            
            print("✅ Config save and load test passed")
            return True
    except Exception as e:
        print(f"❌ Config save and load test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_llm_config():
    """Test LLM configuration"""
    print("\n🧪 Test 3: LLM Configuration")
    
    try:
        config = Config()
        
        llm_config = config.get_llm_config()
        
        assert llm_config is not None
        assert llm_config.provider == "openai"
        assert llm_config.model == "gpt-4o"
        
        print("✅ LLM config test passed")
        return True
    except Exception as e:
        print(f"❌ LLM config test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_project_config_dataclass():
    """Test ProjectConfig dataclass"""
    print("\n🧪 Test 4: ProjectConfig Dataclass")
    
    try:
        project = ProjectConfig(
            name="MyProject",
            version="0.2.0",
            entry="app.py"
        )
        
        assert project.name == "MyProject"
        assert project.version == "0.2.0"
        assert project.entry == "app.py"
        
        print("✅ ProjectConfig dataclass test passed")
        return True
    except Exception as e:
        print(f"❌ ProjectConfig dataclass test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_build_config_dataclass():
    """Test BuildConfig dataclass"""
    print("\n🧪 Test 5: BuildConfig Dataclass")
    
    try:
        build = BuildConfig(
            target=["android", "ios", "web"],
            generator="react-native",
            llm_provider="anthropic",
            llm_model="claude-3-opus-20240229",
            output_dir="./dist",
            cache=True
        )
        
        assert build.target == ["android", "ios", "web"]
        assert build.generator == "react-native"
        assert build.llm_provider == "anthropic"
        assert build.cache == True
        
        print("✅ BuildConfig dataclass test passed")
        return True
    except Exception as e:
        print(f"❌ BuildConfig dataclass test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_devserver_config_dataclass():
    """Test DevServerConfig dataclass"""
    print("\n🧪 Test 6: DevServerConfig Dataclass")
    
    try:
        devserver = DevServerConfig(
            port=8000,
            hot_reload=True,
            mobile_frame=False
        )
        
        assert devserver.port == 8000
        assert devserver.hot_reload == True
        assert devserver.mobile_frame == False
        
        print("✅ DevServerConfig dataclass test passed")
        return True
    except Exception as e:
        print(f"❌ DevServerConfig dataclass test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_style_config_dataclass():
    """Test StyleConfig dataclass"""
    print("\n🧪 Test 7: StyleConfig Dataclass")
    
    try:
        style = StyleConfig(system="tailwind")
        
        assert style.system == "tailwind"
        
        print("✅ StyleConfig dataclass test passed")
        return True
    except Exception as e:
        print(f"❌ StyleConfig dataclass test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_llm_config_dataclass():
    """Test LLMConfig dataclass"""
    print("\n🧪 Test 8: LLMConfig Dataclass")
    
    try:
        llm = LLMConfig(
            provider="openai-compatible",
            api_key="test-key",
            model="custom-model",
            base_url="https://api.example.com/v1",
            x_api_key="optional-header"
        )
        
        assert llm.provider == "openai-compatible"
        assert llm.api_key == "test-key"
        assert llm.model == "custom-model"
        assert llm.base_url == "https://api.example.com/v1"
        assert llm.x_api_key == "optional-header"
        
        print("✅ LLMConfig dataclass test passed")
        return True
    except Exception as e:
        print(f"❌ LLMConfig dataclass test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 P2M Configuration System Test Suite")
    print("="*60)
    
    tests = [
        test_default_config,
        test_config_save_and_load,
        test_llm_config,
        test_project_config_dataclass,
        test_build_config_dataclass,
        test_devserver_config_dataclass,
        test_style_config_dataclass,
        test_llm_config_dataclass,
    ]
    
    results = []
    
    for test_func in tests:
        try:
            result = test_func()
            results.append((test_func.__name__, result))
        except Exception as e:
            results.append((test_func.__name__, False))
            print(f"❌ {test_func.__name__} failed: {e}")
    
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
