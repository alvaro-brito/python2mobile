"""
P2M AST Walker - Analyzes component tree structure
"""

import ast
from typing import Any, Dict, List, Optional


class ASTWalker:
    """Walks and analyzes component tree"""
    
    def __init__(self):
        self.components: List[Dict[str, Any]] = []
        self.handlers: Dict[str, Any] = {}
    
    def walk(self, component_tree: Dict[str, Any]) -> Dict[str, Any]:
        """Walk component tree and extract structure"""
        self.components = []
        self.handlers = {}
        
        self._walk_component(component_tree)
        
        return {
            "components": self.components,
            "handlers": self.handlers,
        }
    
    def _walk_component(self, component: Dict[str, Any], parent_id: str = "root") -> None:
        """Recursively walk component tree"""
        component_type = component.get("type", "unknown")
        props = component.get("props", {})
        children = component.get("children", [])
        
        # Extract component info
        component_info = {
            "type": component_type,
            "props": props,
            "children_count": len(children),
        }
        
        self.components.append(component_info)
        
        # Extract handlers
        for key, value in props.items():
            if key.startswith("on_") and value:
                handler_name = value
                self.handlers[handler_name] = {
                    "component": component_type,
                    "event": key,
                }
        
        # Walk children
        for child in children:
            if isinstance(child, dict):
                self._walk_component(child, parent_id)
    
    def extract_handlers(self, component_tree: Dict[str, Any]) -> Dict[str, Any]:
        """Extract all event handlers from component tree"""
        handlers = {}
        self._extract_handlers_recursive(component_tree, handlers)
        return handlers
    
    def _extract_handlers_recursive(self, component: Dict[str, Any], 
                                   handlers: Dict[str, Any]) -> None:
        """Recursively extract handlers"""
        props = component.get("props", {})
        
        for key, value in props.items():
            if key.startswith("on_") and value:
                handlers[value] = {
                    "component": component.get("type"),
                    "event": key,
                }
        
        children = component.get("children", [])
        for child in children:
            if isinstance(child, dict):
                self._extract_handlers_recursive(child, handlers)
    
    def analyze_structure(self, component_tree: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze component tree structure"""
        analysis = {
            "total_components": 0,
            "component_types": {},
            "depth": 0,
            "handlers": {},
        }
        
        self._analyze_recursive(component_tree, analysis, 0)
        return analysis
    
    def _analyze_recursive(self, component: Dict[str, Any], 
                          analysis: Dict[str, Any], depth: int) -> None:
        """Recursively analyze structure"""
        component_type = component.get("type", "unknown")
        
        # Update counts
        analysis["total_components"] += 1
        analysis["component_types"][component_type] = analysis["component_types"].get(component_type, 0) + 1
        analysis["depth"] = max(analysis["depth"], depth)
        
        # Extract handlers
        props = component.get("props", {})
        for key, value in props.items():
            if key.startswith("on_") and value:
                analysis["handlers"][value] = {
                    "component": component_type,
                    "event": key,
                }
        
        # Analyze children
        children = component.get("children", [])
        for child in children:
            if isinstance(child, dict):
                self._analyze_recursive(child, analysis, depth + 1)


class CodeExtractor:
    """Extracts Python code information for LLM"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.tree: Optional[ast.AST] = None
        self.functions: Dict[str, str] = {}
        self.imports: List[str] = []
        self.classes: Dict[str, str] = {}
    
    def extract(self) -> Dict[str, Any]:
        """Extract code information"""
        with open(self.file_path, "r") as f:
            code = f.read()
        
        self.tree = ast.parse(code)
        self._extract_imports()
        self._extract_functions()
        self._extract_classes()
        
        return {
            "file": self.file_path,
            "imports": self.imports,
            "functions": self.functions,
            "classes": self.classes,
            "raw_code": code,
        }
    
    def _extract_imports(self) -> None:
        """Extract import statements"""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    self.imports.append(f"from {module} import {alias.name}")
    
    def _extract_functions(self) -> None:
        """Extract function definitions"""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                self.functions[node.name] = ast.get_source_segment(
                    open(self.file_path).read(), node
                ) or ""
    
    def _extract_classes(self) -> None:
        """Extract class definitions"""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                self.classes[node.name] = ast.get_source_segment(
                    open(self.file_path).read(), node
                ) or ""
