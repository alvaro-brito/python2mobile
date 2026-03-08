"""
P2M Code Validator - Validates P2M code for syntax and structure errors
"""

import ast
import sys
from typing import List, Tuple, Dict, Any
from pathlib import Path


class ValidationError:
    """Represents a validation error"""
    
    def __init__(self, file: str, line: int, column: int, message: str, severity: str = "error"):
        self.file = file
        self.line = line
        self.column = column
        self.message = message
        self.severity = severity  # "error", "warning", "info"
    
    def __str__(self) -> str:
        return f"{self.file}:{self.line}:{self.column} [{self.severity.upper()}] {self.message}"
    
    def __repr__(self) -> str:
        return self.__str__()


class CodeValidator:
    """Validates P2M code"""
    
    # Required imports for P2M apps
    REQUIRED_IMPORTS = {
        "Render": "from p2m.core import Render",
        "Container": "from p2m.ui import Container",
    }
    
    # Required functions
    REQUIRED_FUNCTIONS = [
        "create_view",
        "main",
    ]
    
    # Recommended patterns
    RECOMMENDED_PATTERNS = {
        "create_view_returns_build": "create_view should return component.build()",
        "main_calls_render": "main should call Render.execute(create_view)",
    }
    
    def __init__(self):
        self.errors: List[ValidationError] = []
        self.warnings: List[ValidationError] = []
    
    def validate_file(self, file_path: str) -> Tuple[bool, List[ValidationError], List[ValidationError]]:
        """
        Validate a single Python file
        
        Returns: (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Check syntax
            self._check_syntax(file_path, content)
            
            # Check imports
            self._check_imports(file_path, content)
            
            # Check functions
            self._check_functions(file_path, content)
            
            # Check patterns
            self._check_patterns(file_path, content)
            
        except Exception as e:
            self.errors.append(ValidationError(
                file_path, 0, 0,
                f"Failed to validate file: {str(e)}",
                "error"
            ))
        
        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings
    
    def validate_project(self, project_dir: str = ".", entry_file: str = "main.py") -> Tuple[bool, List[ValidationError], List[ValidationError]]:
        """
        Validate all Python files in a project.

        The entry point file gets full validation (syntax + imports + functions + patterns).
        All other module files get syntax-only validation.

        Returns: (is_valid, all_errors, all_warnings)
        """
        all_errors = []
        all_warnings = []

        project_path = Path(project_dir)
        entry_path = Path(entry_file)

        # Find all Python files
        py_files = list(project_path.glob("**/*.py"))

        if not py_files:
            all_errors.append(ValidationError(
                project_dir, 0, 0,
                "No Python files found in project",
                "error"
            ))
            return False, all_errors, all_warnings

        # Validate each file
        for py_file in py_files:
            # Skip __pycache__ and test files
            if "__pycache__" in str(py_file) or py_file.name.startswith("test_"):
                continue

            # Check if this is the entry point file.
            # Compare resolved absolute paths so views/main.py is never confused
            # with the root-level main.py.
            resolved_entry = (project_path / entry_file).resolve()
            is_entry = (py_file.resolve() == resolved_entry)

            if is_entry:
                # Full validation for entry point
                is_valid, errors, warnings = self.validate_file(str(py_file))
            else:
                # Syntax-only validation for module files
                is_valid, errors, warnings = self._validate_module(str(py_file))

            all_errors.extend(errors)
            all_warnings.extend(warnings)

        is_valid = len(all_errors) == 0
        return is_valid, all_errors, all_warnings

    def _validate_module(self, file_path: str) -> Tuple[bool, List[ValidationError], List[ValidationError]]:
        """
        Validate a module file (syntax-only, no import/function/pattern checks).

        Returns: (is_valid, errors, warnings)
        """
        errors = []
        warnings = []

        try:
            with open(file_path, 'r') as f:
                content = f.read()

            # Only check syntax for module files
            try:
                ast.parse(content)
            except SyntaxError as e:
                errors.append(ValidationError(
                    file_path, e.lineno or 0, e.offset or 0,
                    f"Syntax error: {e.msg}",
                    "error"
                ))
        except Exception as e:
            errors.append(ValidationError(
                file_path, 0, 0,
                f"Failed to validate file: {str(e)}",
                "error"
            ))

        is_valid = len(errors) == 0
        return is_valid, errors, warnings
    
    def _check_syntax(self, file_path: str, content: str) -> None:
        """Check Python syntax"""
        try:
            ast.parse(content)
        except SyntaxError as e:
            self.errors.append(ValidationError(
                file_path, e.lineno or 0, e.offset or 0,
                f"Syntax error: {e.msg}",
                "error"
            ))
    
    def _check_imports(self, file_path: str, content: str) -> None:
        """Check for required imports"""
        # Check for P2M imports
        has_render_import = "from p2m.core import Render" in content or "from p2m import" in content
        has_ui_import = "from p2m.ui import" in content
        
        if not has_render_import:
            self.warnings.append(ValidationError(
                file_path, 1, 0,
                "Missing P2M core import (from p2m.core import Render)",
                "warning"
            ))
        
        if not has_ui_import:
            self.warnings.append(ValidationError(
                file_path, 1, 0,
                "Missing P2M UI imports (from p2m.ui import ...)",
                "warning"
            ))
    
    def _check_functions(self, file_path: str, content: str) -> None:
        """Check for required functions"""
        try:
            tree = ast.parse(content)
            
            functions = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
            
            for required_func in self.REQUIRED_FUNCTIONS:
                if required_func not in functions:
                    self.errors.append(ValidationError(
                        file_path, 0, 0,
                        f"Missing required function: {required_func}()",
                        "error"
                    ))
        except:
            pass  # Already reported in syntax check
    
    def _check_patterns(self, file_path: str, content: str) -> None:
        """Check for recommended patterns"""
        
        # Check if create_view returns .build()
        if "def create_view" in content:
            # Look for .build() in the file
            if ".build()" not in content:
                self.warnings.append(ValidationError(
                    file_path, 0, 0,
                    "create_view should return component.build()",
                    "warning"
                ))
        
        # Check if main calls Render.execute
        if "def main" in content:
            if "Render.execute" not in content:
                self.warnings.append(ValidationError(
                    file_path, 0, 0,
                    "main should call Render.execute(create_view)",
                    "warning"
                ))
    
    def print_report(self, is_valid: bool, errors: List[ValidationError], warnings: List[ValidationError]) -> None:
        """Print validation report"""
        
        print("\n" + "="*70)
        print("📋 Code Validation Report")
        print("="*70)
        
        if errors:
            print(f"\n❌ Errors ({len(errors)}):")
            for error in errors:
                print(f"   {error}")
        
        if warnings:
            print(f"\n⚠️  Warnings ({len(warnings)}):")
            for warning in warnings:
                print(f"   {warning}")
        
        if is_valid and not warnings:
            print("\n✅ All validations passed!")
        elif is_valid:
            print(f"\n✅ Code is valid ({len(warnings)} warning(s))")
        else:
            print(f"\n❌ Validation failed ({len(errors)} error(s))")
        
        print("="*70 + "\n")
    
    def get_summary(self, is_valid: bool, errors: List[ValidationError], warnings: List[ValidationError]) -> str:
        """Get a summary of validation results"""
        
        if not is_valid:
            return f"❌ Validation failed: {len(errors)} error(s), {len(warnings)} warning(s)"
        elif warnings:
            return f"⚠️  Validation passed with {len(warnings)} warning(s)"
        else:
            return "✅ Validation passed"


def validate_project(project_dir: str = ".", entry_file: str = "main.py") -> Tuple[bool, List[ValidationError], List[ValidationError]]:
    """Validate a P2M project"""
    validator = CodeValidator()
    return validator.validate_project(project_dir, entry_file=entry_file)


def validate_file(file_path: str) -> Tuple[bool, List[ValidationError], List[ValidationError]]:
    """Validate a single P2M file"""
    validator = CodeValidator()
    return validator.validate_file(file_path)
