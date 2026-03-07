"""
Test suite for real-world P2M applications
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from p2m.core import Render, RenderEngine


def test_todo_app():
    """Test todo app example"""
    print("\n🧪 Test 1: Todo App Example")
    
    try:
        # Import the example
        sys.path.insert(0, str(Path(__file__).parent.parent / "examples"))
        import example_todo_app
        
        # Execute the view
        component_tree = Render.execute(example_todo_app.create_view)
        
        assert component_tree is not None
        assert component_tree["type"] == "Container"
        
        # Render to HTML
        engine = RenderEngine()
        html = engine.render(component_tree, mobile_frame=False)
        
        assert html is not None
        assert "My Todo App" in html
        assert "Todo List" in html
        
        print("✅ Todo app test passed")
        print(f"   Generated HTML: {len(html)} bytes")
        return True
    except Exception as e:
        print(f"❌ Todo app test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_ecommerce_app():
    """Test e-commerce app example"""
    print("\n🧪 Test 2: E-commerce App Example")
    
    try:
        # Import the example
        sys.path.insert(0, str(Path(__file__).parent.parent / "examples"))
        import example_ecommerce_app
        
        # Execute the view
        component_tree = Render.execute(example_ecommerce_app.create_view)
        
        assert component_tree is not None
        assert component_tree["type"] == "Container"
        
        # Render to HTML
        engine = RenderEngine()
        html = engine.render(component_tree, mobile_frame=False)
        
        assert html is not None
        assert "TechStore" in html
        assert "Featured Products" in html
        
        print("✅ E-commerce app test passed")
        print(f"   Generated HTML: {len(html)} bytes")
        return True
    except Exception as e:
        print(f"❌ E-commerce app test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_todo_app_with_mobile_frame():
    """Test todo app with mobile frame"""
    print("\n🧪 Test 3: Todo App with Mobile Frame")
    
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent / "examples"))
        import example_todo_app
        
        component_tree = Render.execute(example_todo_app.create_view)
        
        # Render with mobile frame
        engine = RenderEngine()
        html = engine.render(component_tree, mobile_frame=True)
        
        assert html is not None
        assert "mobile-frame" in html
        assert "375px" in html
        assert "My Todo App" in html
        
        print("✅ Todo app with mobile frame test passed")
        print(f"   Generated HTML: {len(html)} bytes")
        return True
    except Exception as e:
        print(f"❌ Todo app with mobile frame test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_ecommerce_app_with_mobile_frame():
    """Test e-commerce app with mobile frame"""
    print("\n🧪 Test 4: E-commerce App with Mobile Frame")
    
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent / "examples"))
        import example_ecommerce_app
        
        component_tree = Render.execute(example_ecommerce_app.create_view)
        
        # Render with mobile frame
        engine = RenderEngine()
        html = engine.render(component_tree, mobile_frame=True)
        
        assert html is not None
        assert "mobile-frame" in html
        assert "TechStore" in html
        
        print("✅ E-commerce app with mobile frame test passed")
        print(f"   Generated HTML: {len(html)} bytes")
        return True
    except Exception as e:
        print(f"❌ E-commerce app with mobile frame test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_app_structure():
    """Test app component structure"""
    print("\n🧪 Test 5: App Component Structure")
    
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent / "examples"))
        import example_todo_app
        
        component_tree = Render.execute(example_todo_app.create_view)
        
        # Verify structure
        assert component_tree["type"] == "Container"
        assert len(component_tree["children"]) > 0
        
        # Count different component types
        def count_components(comp, comp_type):
            count = 0
            if comp.get("type") == comp_type:
                count += 1
            for child in comp.get("children", []):
                if isinstance(child, dict):
                    count += count_components(child, comp_type)
            return count
        
        text_count = count_components(component_tree, "Text")
        button_count = count_components(component_tree, "Button")
        card_count = count_components(component_tree, "Card")
        
        assert text_count > 0, "Should have Text components"
        assert button_count > 0, "Should have Button components"
        
        print(f"✅ App structure test passed")
        print(f"   Text components: {text_count}")
        print(f"   Button components: {button_count}")
        print(f"   Card components: {card_count}")
        return True
    except Exception as e:
        print(f"❌ App structure test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 P2M Real-World Apps Test Suite")
    print("="*60)
    
    tests = [
        test_todo_app,
        test_ecommerce_app,
        test_todo_app_with_mobile_frame,
        test_ecommerce_app_with_mobile_frame,
        test_app_structure,
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
