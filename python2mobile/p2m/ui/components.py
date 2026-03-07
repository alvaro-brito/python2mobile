"""
P2M UI Components - Declarative component library
"""

from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class Component:
    """Base component class"""
    
    component_type: str
    props: Dict[str, Any] = field(default_factory=dict)
    children: List["Component"] = field(default_factory=list)
    
    def add(self, child: "Component") -> "Component":
        """Add a child component"""
        self.children.append(child)
        return self
    
    def build(self) -> Dict[str, Any]:
        """Build component tree as dictionary"""
        return {
            "type": self.component_type,
            "props": self.props,
            "children": [child.build() if isinstance(child, Component) else child 
                        for child in self.children],
        }
    
    def __repr__(self) -> str:
        return f"<{self.component_type} {self.props}>"


class Container(Component):
    """Container component - wrapper for other components"""
    
    def __init__(self, class_: str = "", direction: str = "column", scroll: bool = False, **props):
        super().__init__(
            component_type="Container",
            props={
                "class": class_,
                "direction": direction,
                "scroll": scroll,
                **props,
            }
        )


class Text(Component):
    """Text component - displays text content"""
    
    def __init__(self, value: str, class_: str = "", **props):
        super().__init__(
            component_type="Text",
            props={
                "value": value,
                "class": class_,
                **props,
            }
        )


class Button(Component):
    """Button component - clickable button"""

    def __init__(
        self,
        label: str,
        class_: str = "",
        on_click=None,
        on_click_args: Optional[List] = None,
        **props,
    ):
        # on_click can be a callable or a string (handler name)
        if callable(on_click):
            on_click_name = on_click.__name__
        else:
            on_click_name = on_click  # already a string or None

        super().__init__(
            component_type="Button",
            props={
                "label": label,
                "class": class_,
                "on_click": on_click_name,
                "on_click_args": on_click_args or [],
                **props,
            },
        )


class Input(Component):
    """Input component - text input field"""

    def __init__(
        self,
        placeholder: str = "",
        class_: str = "",
        on_change=None,
        value: str = "",
        input_type: str = "text",
        **props,
    ):
        if callable(on_change):
            on_change_name = on_change.__name__
        else:
            on_change_name = on_change  # string or None

        super().__init__(
            component_type="Input",
            props={
                "placeholder": placeholder,
                "class": class_,
                "on_change": on_change_name,
                "value": value,
                "input_type": input_type,
                **props,
            },
        )


class Image(Component):
    """Image component - displays images"""
    
    def __init__(self, src: str, class_: str = "", alt: str = "", **props):
        super().__init__(
            component_type="Image",
            props={
                "src": src,
                "class": class_,
                "alt": alt,
                **props,
            }
        )


class List(Component):
    """List component - renders list of items"""
    
    def __init__(self, items: List[Any], render_item: Optional[Callable] = None, 
                 class_: str = "", **props):
        super().__init__(
            component_type="List",
            props={
                "items": items,
                "render_item": render_item.__name__ if render_item else None,
                "class": class_,
                **props,
            }
        )
        self._render_item = render_item
        self._items = items
    
    def get_renderer(self) -> Optional[Callable]:
        """Get the item renderer"""
        return self._render_item
    
    def get_items(self) -> List[Any]:
        """Get items"""
        return self._items


class Navigator(Component):
    """Navigator component - handles navigation between screens"""
    
    def __init__(self, routes: Dict[str, Callable], initial: str = "", **props):
        super().__init__(
            component_type="Navigator",
            props={
                "initial": initial,
                **props,
            }
        )
        self._routes = routes
    
    def get_routes(self) -> Dict[str, Callable]:
        """Get routes"""
        return self._routes


class Screen(Component):
    """Screen component - represents a screen/page"""
    
    def __init__(self, name: str, class_: str = "", **props):
        super().__init__(
            component_type="Screen",
            props={
                "name": name,
                "class": class_,
                **props,
            }
        )


class Modal(Component):
    """Modal component - displays modal dialog"""
    
    def __init__(self, title: str = "", class_: str = "", visible: bool = False, **props):
        super().__init__(
            component_type="Modal",
            props={
                "title": title,
                "class": class_,
                "visible": visible,
                **props,
            }
        )


class ScrollView(Component):
    """ScrollView component - scrollable container"""

    def __init__(self, class_: str = "", **props):
        super().__init__(
            component_type="ScrollView",
            props={
                "class": class_,
                **props,
            }
        )


class Carousel(Component):
    """Carousel component - horizontal scrollable row of items"""

    def __init__(self, class_: str = "", **props):
        super().__init__(
            component_type="Carousel",
            props={"class": class_, **props},
        )


class Row(Component):
    """Row component - horizontal layout"""
    
    def __init__(self, class_: str = "", **props):
        super().__init__(
            component_type="Row",
            props={
                "class": class_,
                "direction": "row",
                **props,
            }
        )


class Column(Component):
    """Column component - vertical layout"""
    
    def __init__(self, class_: str = "", **props):
        super().__init__(
            component_type="Column",
            props={
                "class": class_,
                "direction": "column",
                **props,
            }
        )


class Card(Component):
    """Card component - card container"""
    
    def __init__(self, class_: str = "", **props):
        super().__init__(
            component_type="Card",
            props={
                "class": class_,
                **props,
            }
        )


class Badge(Component):
    """Badge component - small label"""
    
    def __init__(self, label: str, class_: str = "", **props):
        super().__init__(
            component_type="Badge",
            props={
                "label": label,
                "class": class_,
                **props,
            }
        )


class Icon(Component):
    """Icon component - displays icon"""
    
    def __init__(self, name: str, class_: str = "", size: int = 24, **props):
        super().__init__(
            component_type="Icon",
            props={
                "name": name,
                "class": class_,
                "size": size,
                **props,
            }
        )
