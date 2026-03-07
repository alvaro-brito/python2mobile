"""
Tests for Carousel component and Modal display:none fix.
"""

import pytest
from p2m.ui import Carousel, Modal, Text, Column
from p2m.core.render_engine import RenderEngine


def _html(component):
    return RenderEngine().render_content(component.build())


class TestCarousel:
    def test_carousel_build_type(self):
        c = Carousel()
        tree = c.build()
        assert tree["type"] == "Carousel"

    def test_carousel_in_tag_map(self):
        """Carousel maps to <div> in the render engine."""
        html = _html(Carousel(class_="px-4"))
        assert "<div" in html

    def test_carousel_renders_horizontal_scroll(self):
        html = _html(Carousel())
        assert "overflow-x:auto" in html

    def test_carousel_has_flex_row(self):
        html = _html(Carousel())
        assert "flex-direction:row" in html

    def test_carousel_children_rendered(self):
        c = Carousel()
        c.add(Text("Item A"))
        c.add(Text("Item B"))
        html = _html(c)
        assert "Item A" in html
        assert "Item B" in html

    def test_carousel_class_applied(self):
        html = _html(Carousel(class_="px-4 gap-2"))
        # px-4 → padding-left:1rem; padding-right:1rem;
        assert "padding-left:1rem" in html

    def test_carousel_webkit_scrolling(self):
        html = _html(Carousel())
        assert "-webkit-overflow-scrolling:touch" in html


class TestModalDisplayNone:
    def test_modal_visible_no_display_none(self):
        html = _html(Modal(visible=True, class_="fixed inset-0"))
        assert "display:none" not in html

    def test_modal_hidden_has_display_none(self):
        html = _html(Modal(visible=False))
        assert "display:none" in html

    def test_modal_no_duplicate_style_attr(self):
        """Regression: Modal(visible=False) must not produce two style= attrs."""
        html = _html(Modal(visible=False, class_="fixed inset-0"))
        assert html.count("style=") == 1

    def test_modal_visible_with_class_styles(self):
        """visible=True + class should still render class styles."""
        html = _html(Modal(visible=True, class_="fixed inset-0"))
        # fixed → position:fixed; inset-0 → top:0; right:0; bottom:0; left:0;
        assert "position:fixed" in html

    def test_modal_hidden_with_class_and_display_none(self):
        """visible=False merges class styles with display:none in one style=."""
        html = _html(Modal(visible=False, class_="fixed inset-0"))
        assert "position:fixed" in html
        assert "display:none" in html
        assert html.count("style=") == 1

    def test_modal_children_hidden(self):
        """Children are still in the DOM (just hidden via CSS)."""
        m = Modal(visible=False)
        m.add(Text("Secret content"))
        html = _html(m)
        assert "Secret content" in html
        assert "display:none" in html
