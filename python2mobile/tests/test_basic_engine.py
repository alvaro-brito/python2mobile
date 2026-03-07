"""
Test suite for P2M core engine
"""

import sys
import json
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from p2m.core import Render, RenderEngine
from p2m.ui import Container, Text, Button, Input, Image, Row, Column, Card


def test_simple_container():
    """Test basic container rendering"""
    print("\n🧪 Test 1: Simple Container")
    
    def create_view():
        container = Container(class_="bg-white p-4")
        text = Text("Hello World", class_="text-gray-800 text-lg")
        container.add(text)
        return container.build()
    
    component_tree = Render.execute(create_view)
    
    assert component_tree is not None
    assert component_tree["type"] == "Container"
    assert len(component_tree["children"]) == 1
    assert component_tree["children"][0]["type"] == "Text"
    
    print("✅ Container test passed")
    return component_tree


def test_button_with_handler():
    """Test button with click handler"""
    print("\n🧪 Test 2: Button with Handler")
    
    def on_click():
        return "clicked"
    
    def create_view():
        container = Container()
        button = Button("Click Me", on_click=on_click)
        container.add(button)
        return container.build()
    
    component_tree = Render.execute(create_view)
    
    assert component_tree is not None
    assert component_tree["children"][0]["type"] == "Button"
    assert component_tree["children"][0]["props"]["label"] == "Click Me"
    assert component_tree["children"][0]["props"]["on_click"] == "on_click"
    
    print("✅ Button handler test passed")
    return component_tree


def test_complex_layout():
    """Test complex nested layout"""
    print("\n🧪 Test 3: Complex Nested Layout")
    
    def create_view():
        container = Container(class_="bg-gray-100 min-h-screen flex items-center justify-center")
        
        card = Card(class_="bg-white rounded-lg shadow-lg p-8")
        
        header = Text("Welcome", class_="text-2xl font-bold text-gray-800")
        card.add(header)
        
        description = Text("This is a test app", class_="text-gray-600 mt-4")
        card.add(description)
        
        button = Button("Get Started", class_="bg-blue-600 text-white mt-6 px-4 py-2 rounded")
        card.add(button)
        
        container.add(card)
        return container.build()
    
    component_tree = Render.execute(create_view)
    
    assert component_tree is not None
    assert component_tree["type"] == "Container"
    assert component_tree["children"][0]["type"] == "Card"
    
    # Check nested structure
    card = component_tree["children"][0]
    assert len(card["children"]) == 3
    assert card["children"][0]["type"] == "Text"
    assert card["children"][1]["type"] == "Text"
    assert card["children"][2]["type"] == "Button"
    
    print("✅ Complex layout test passed")
    return component_tree


def test_html_rendering():
    """Test HTML rendering"""
    print("\n🧪 Test 4: HTML Rendering")
    
    def create_view():
        container = Container(class_="bg-white p-4")
        text = Text("Hello World", class_="text-gray-800")
        container.add(text)
        return container.build()
    
    component_tree = Render.execute(create_view)
    engine = RenderEngine()
    html = engine.render(component_tree, mobile_frame=False)
    
    assert html is not None
    assert "<html" in html.lower()
    assert "Hello World" in html
    assert "background-color:#ffffff" in html
    
    print("✅ HTML rendering test passed")
    print(f"   Generated HTML length: {len(html)} bytes")
    return html


def test_mobile_frame():
    """Test mobile frame rendering"""
    print("\n🧪 Test 5: Mobile Frame Rendering")
    
    def create_view():
        container = Container(class_="bg-white p-4")
        text = Text("Mobile App", class_="text-center")
        container.add(text)
        return container.build()
    
    component_tree = Render.execute(create_view)
    engine = RenderEngine()
    html = engine.render(component_tree, mobile_frame=True)
    
    assert html is not None
    assert "mobile-frame" in html
    assert "390px" in html
    assert "844px" in html
    
    print("✅ Mobile frame test passed")
    return html


def test_multiple_components():
    """Test multiple components in sequence"""
    print("\n🧪 Test 6: Multiple Components")
    
    def create_view():
        container = Container(class_="space-y-4 p-4")
        
        for i in range(3):
            text = Text(f"Item {i+1}", class_="text-gray-800")
            container.add(text)
        
        return container.build()
    
    component_tree = Render.execute(create_view)
    
    assert component_tree is not None
    assert len(component_tree["children"]) == 3
    
    for i, child in enumerate(component_tree["children"]):
        assert child["type"] == "Text"
        assert f"Item {i+1}" in child["props"]["value"]
    
    print("✅ Multiple components test passed")
    return component_tree


def test_input_component():
    """Test input component"""
    print("\n🧪 Test 7: Input Component")
    
    def on_change(value):
        return value
    
    def create_view():
        container = Container()
        input_field = Input(placeholder="Enter text", on_change=on_change)
        container.add(input_field)
        return container.build()
    
    component_tree = Render.execute(create_view)
    
    assert component_tree is not None
    assert component_tree["children"][0]["type"] == "Input"
    assert component_tree["children"][0]["props"]["placeholder"] == "Enter text"
    assert component_tree["children"][0]["props"]["on_change"] == "on_change"
    
    print("✅ Input component test passed")
    return component_tree


def test_row_column_layout():
    """Test row and column layouts"""
    print("\n🧪 Test 8: Row and Column Layouts")
    
    def create_view():
        container = Container()
        
        row = Row(class_="space-x-4")
        row.add(Text("Left", class_="flex-1"))
        row.add(Text("Right", class_="flex-1"))
        
        column = Column(class_="space-y-4")
        column.add(Text("Top"))
        column.add(Text("Bottom"))
        
        container.add(row)
        container.add(column)
        return container.build()
    
    component_tree = Render.execute(create_view)
    
    assert component_tree is not None
    assert len(component_tree["children"]) == 2
    assert component_tree["children"][0]["type"] == "Row"
    assert component_tree["children"][1]["type"] == "Column"
    
    print("✅ Row and column layout test passed")
    return component_tree


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 P2M Core Engine Test Suite")
    print("="*60)
    
    tests = [
        test_simple_container,
        test_button_with_handler,
        test_complex_layout,
        test_html_rendering,
        test_mobile_frame,
        test_multiple_components,
        test_input_component,
        test_row_column_layout,
    ]
    
    results = []
    
    for test_func in tests:
        try:
            result = test_func()
            results.append((test_func.__name__, True, None))
        except Exception as e:
            results.append((test_func.__name__, False, str(e)))
            print(f"❌ {test_func.__name__} failed: {e}")
            import traceback
            traceback.print_exc()
    
    # Summary
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    for name, success, error in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
        if error:
            print(f"       Error: {error}")
    
    print(f"\n📈 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
