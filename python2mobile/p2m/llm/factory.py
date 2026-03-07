"""
P2M LLM Factory - Creates LLM provider instances
"""

from typing import Optional
from p2m.llm.base import LLMProvider
from p2m.llm.openai_provider import OpenAIProvider
from p2m.llm.anthropic_provider import AnthropicProvider
from p2m.llm.ollama_provider import OllamaProvider
from p2m.llm.compatible_provider import CompatibleProvider


class LLMFactory:
    """Factory for creating LLM provider instances"""
    
    @staticmethod
    def create(
        provider: str,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        x_api_key: Optional[str] = None,
    ) -> LLMProvider:
        """Create an LLM provider instance"""
        
        provider = provider.lower().strip()
        
        if provider == "openai":
            return OpenAIProvider(
                api_key=api_key,
                model=model or "gpt-4o",
            )
        
        elif provider == "anthropic" or provider == "claude":
            return AnthropicProvider(
                api_key=api_key,
                model=model or "claude-3-opus-20240229",
            )
        
        elif provider == "ollama":
            return OllamaProvider(
                base_url=base_url or "http://localhost:11434",
                model=model or "llama2",
            )
        
        elif provider == "openai-compatible" or provider == "compatible":
            if not base_url:
                raise ValueError("base_url required for OpenAI-compatible provider")
            if not api_key:
                raise ValueError("api_key required for OpenAI-compatible provider")
            if not model:
                raise ValueError("model required for OpenAI-compatible provider")
            
            return CompatibleProvider(
                base_url=base_url,
                api_key=api_key,
                model=model,
                x_api_key=x_api_key,
            )
        
        else:
            raise ValueError(f"Unknown LLM provider: {provider}")
    
    @staticmethod
    def get_available_providers() -> list:
        """Get list of available providers"""
        return [
            "openai",
            "anthropic",
            "ollama",
            "openai-compatible",
        ]
