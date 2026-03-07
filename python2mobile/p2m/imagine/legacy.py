"""
P2M Imagine - Generate P2M code from natural language descriptions
"""

import os
import sys
from pathlib import Path
from typing import Optional
from p2m.llm.factory import LLMFactory
from p2m.config import Config


class CodeImaginer:
    """Generate P2M code from natural language descriptions"""
    
    SYSTEM_PROMPT = """You are an expert Python2Mobile developer. Generate clean, production-ready Python code for mobile apps using the P2M framework.

Guidelines:
1. Always import from p2m.core and p2m.ui
2. Create a create_view() function that returns component.build()
3. Use Tailwind CSS classes for styling
4. Add event handlers for interactive components
5. Keep code clean and well-organized
6. Use meaningful variable names
7. Add comments for complex logic
8. Ensure the code is complete and runnable

Always generate the complete, runnable code without any placeholders."""
    
    def __init__(self, provider: str, model: str, api_key: Optional[str] = None,
                 base_url: Optional[str] = None, x_api_key: Optional[str] = None):
        """Initialize the code imaginer"""
        self.provider = provider
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.x_api_key = x_api_key
        self.llm = None
    
    def validate_config(self) -> tuple[bool, str]:
        """Validate LLM configuration"""
        
        if self.provider.lower() == "openai":
            api_key = self.api_key or os.getenv("OPENAI_API_KEY")
            if not api_key:
                return False, "OPENAI_API_KEY not set. Set environment variable or use --api-key"
            self.api_key = api_key
        
        elif self.provider.lower() == "anthropic":
            api_key = self.api_key or os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                return False, "ANTHROPIC_API_KEY not set. Set environment variable or use --api-key"
            self.api_key = api_key
        
        elif self.provider.lower() == "ollama":
            if not self.base_url:
                self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        
        elif self.provider.lower() == "openai-compatible":
            if not self.base_url:
                return False, "--base-url required for OpenAI-compatible provider"
            api_key = self.api_key or os.getenv("P2M_COMPATIBLE_API_KEY")
            if not api_key:
                return False, "API key required. Set P2M_COMPATIBLE_API_KEY or use --api-key"
            self.api_key = api_key
        
        return True, "Configuration valid"
    
    def create_provider(self):
        """Create LLM provider instance"""
        try:
            self.llm = LLMFactory.create(
                provider=self.provider,
                api_key=self.api_key,
                model=self.model,
                base_url=self.base_url,
                x_api_key=self.x_api_key,
            )
            return True, "Provider created successfully"
        except Exception as e:
            return False, str(e)
    
    def generate_code(self, description: str) -> tuple[bool, str]:
        """Generate P2M code from description"""
        
        if not self.llm:
            success, msg = self.create_provider()
            if not success:
                return False, f"Failed to create provider: {msg}"
        
        try:
            prompt = f"""{self.SYSTEM_PROMPT}

User Request: {description}

Generate the complete P2M application code:"""
            
            print(f"\n🤖 Generating code using {self.provider} ({self.model})...")
            print(f"📝 Prompt: {description}\n")
            
            code = self.llm.generate(prompt, max_tokens=4096, temperature=0.7)
            
            # Clean up code (remove markdown code blocks if present)
            code = code.strip()
            if code.startswith("```python"):
                code = code[9:]
            if code.startswith("```"):
                code = code[3:]
            if code.endswith("```"):
                code = code[:-3]
            code = code.strip()
            
            return True, code
        
        except Exception as e:
            return False, f"Code generation failed: {str(e)}"
    
    def save_code(self, code: str, filename: str = "generated_app.py") -> tuple[bool, str]:
        """Save generated code to file"""
        try:
            output_path = Path(filename)
            with open(output_path, "w") as f:
                f.write(code)
            return True, str(output_path.absolute())
        except Exception as e:
            return False, str(e)
    
    def validate_code(self, code: str) -> tuple[bool, str]:
        """Validate generated code"""
        try:
            import ast
            ast.parse(code)
            
            # Check for required components
            if "from p2m" not in code:
                return False, "Code must import from p2m"
            
            if "create_view" not in code:
                return False, "Code must define create_view() function"
            
            if "return" not in code:
                return False, "create_view() must return component.build()"
            
            return True, "Code validation passed"
        except SyntaxError as e:
            return False, f"Syntax error: {e}"
        except Exception as e:
            return False, f"Validation error: {e}"


def imagine_command(description: str, provider: str = "openai", model: Optional[str] = None,
                   api_key: Optional[str] = None, base_url: Optional[str] = None,
                   x_api_key: Optional[str] = None, output: str = "generated_app.py",
                   validate: bool = True) -> tuple[bool, str, Optional[str]]:
    """
    Generate P2M code from natural language description
    
    Returns: (success, message, code_or_error)
    """
    
    # Set default model based on provider
    if not model:
        model_defaults = {
            "openai": "gpt-4o",
            "anthropic": "claude-3-opus-20240229",
            "ollama": "llama2",
            "openai-compatible": "default",
        }
        model = model_defaults.get(provider.lower(), "default")
    
    # Create imaginer
    imaginer = CodeImaginer(
        provider=provider,
        model=model,
        api_key=api_key,
        base_url=base_url,
        x_api_key=x_api_key,
    )
    
    # Validate configuration
    valid, msg = imaginer.validate_config()
    if not valid:
        return False, msg, None
    
    print(f"✅ Configuration valid")
    print(f"   Provider: {provider}")
    print(f"   Model: {model}")
    
    # Create provider
    success, msg = imaginer.create_provider()
    if not success:
        return False, msg, None
    
    print(f"✅ {msg}")
    
    # Generate code
    success, code = imaginer.generate_code(description)
    if not success:
        return False, code, None
    
    print(f"✅ Code generated successfully")
    
    # Validate code
    if validate:
        valid, msg = imaginer.validate_code(code)
        if not valid:
            return False, f"Code validation failed: {msg}", code
        print(f"✅ Code validation passed")
    
    # Save code
    success, filepath = imaginer.save_code(code, output)
    if not success:
        return False, f"Failed to save code: {filepath}", code
    
    print(f"✅ Code saved to: {filepath}")
    
    return True, f"Successfully generated code at {filepath}", code
