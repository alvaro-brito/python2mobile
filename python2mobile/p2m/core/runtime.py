"""
P2M Runtime Engine - Executes Python code in a safe sandbox
"""

import sys
import ast
import inspect
from typing import Any, Callable, Dict, Optional
from pathlib import Path


class Runtime:
    """Safe Python runtime for executing user code"""
    
    def __init__(self, sandbox: bool = True):
        self.sandbox = sandbox
        self.globals: Dict[str, Any] = {}
        self.locals: Dict[str, Any] = {}
        self._setup_sandbox()
    
    def _setup_sandbox(self) -> None:
        """Setup sandbox environment with allowed builtins"""
        if self.sandbox:
            # Restricted builtins for safety
            allowed_builtins = {
                "abs", "all", "any", "ascii", "bin", "bool", "bytearray",
                "bytes", "chr", "dict", "dir", "divmod", "enumerate", "filter",
                "float", "format", "frozenset", "getattr", "hasattr", "hash",
                "hex", "id", "int", "isinstance", "issubclass", "iter", "len",
                "list", "map", "max", "min", "next", "object", "oct", "ord",
                "pow", "print", "range", "repr", "reversed", "round", "set",
                "slice", "sorted", "str", "sum", "tuple", "type", "zip",
            }
            
            self.globals["__builtins__"] = {
                name: __builtins__[name] for name in allowed_builtins
                if name in __builtins__
            }
        else:
            self.globals["__builtins__"] = __builtins__
    
    def execute(self, code: str, globals_dict: Optional[Dict[str, Any]] = None) -> Any:
        """Execute Python code in the sandbox"""
        try:
            # Validate syntax
            ast.parse(code)
            
            # Merge globals
            exec_globals = {**self.globals}
            if globals_dict:
                exec_globals.update(globals_dict)
            
            # Execute
            exec(code, exec_globals, self.locals)
            return self.locals
        except SyntaxError as e:
            raise RuntimeError(f"Syntax error in code: {e}")
        except Exception as e:
            raise RuntimeError(f"Runtime error: {e}")
    
    def execute_function(self, func: Callable, *args, **kwargs) -> Any:
        """Execute a function with given arguments"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise RuntimeError(f"Function execution error: {e}")
    
    def load_module(self, module_path: str) -> Dict[str, Any]:
        """Load and execute a Python module"""
        path = Path(module_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Module not found: {module_path}")
        
        if not path.suffix == ".py":
            raise ValueError(f"Invalid module file: {module_path}")
        
        with open(path, "r") as f:
            code = f.read()
        
        return self.execute(code)


class Render:
    """Main entry point for rendering P2M applications"""
    
    _runtime: Optional[Runtime] = None
    _component_tree: Optional[Any] = None
    
    @classmethod
    def execute(cls, view_func: Callable, sandbox: bool = True) -> Any:
        """Execute a view function and render the component tree"""
        cls._runtime = Runtime(sandbox=sandbox)
        
        try:
            # Call the view function
            component_tree = cls._runtime.execute_function(view_func)
            cls._component_tree = component_tree
            return component_tree
        except Exception as e:
            raise RuntimeError(f"Failed to execute view: {e}")
    
    @classmethod
    def get_component_tree(cls) -> Optional[Any]:
        """Get the current component tree"""
        return cls._component_tree
    
    @classmethod
    def render_html(cls) -> str:
        """Render component tree to HTML"""
        from p2m.core.render_engine import RenderEngine
        
        if cls._component_tree is None:
            raise RuntimeError("No component tree to render. Call execute() first.")
        
        engine = RenderEngine()
        return engine.render(cls._component_tree)
    
    @classmethod
    def render_json(cls) -> Dict[str, Any]:
        """Render component tree to JSON (for mobile apps)"""
        from p2m.core.ast_walker import ASTWalker
        
        if cls._component_tree is None:
            raise RuntimeError("No component tree to render. Call execute() first.")
        
        walker = ASTWalker()
        return walker.walk(cls._component_tree)
