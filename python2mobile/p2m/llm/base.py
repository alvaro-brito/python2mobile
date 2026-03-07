"""
P2M LLM Base - Abstract interface for LLM providers
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key
        self.model = model
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text from prompt"""
        pass
    
    @abstractmethod
    def validate_config(self) -> bool:
        """Validate provider configuration"""
        pass
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} model={self.model}>"


class LLMResponse:
    """LLM response wrapper"""
    
    def __init__(self, content: str, model: str, usage: Optional[Dict[str, int]] = None):
        self.content = content
        self.model = model
        self.usage = usage or {}
    
    def __str__(self) -> str:
        return self.content
    
    def __repr__(self) -> str:
        return f"<LLMResponse model={self.model} tokens={self.usage.get('total_tokens', 0)}>"
