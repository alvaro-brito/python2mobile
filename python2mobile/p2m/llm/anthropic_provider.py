"""
P2M LLM Anthropic Provider - Claude API integration
"""

import os
from typing import Optional
from p2m.llm.base import LLMProvider, LLMResponse


class AnthropicProvider(LLMProvider):
    """Anthropic (Claude) API provider"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-opus-20240229"):
        super().__init__(api_key=api_key, model=model)
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
    
    def validate_config(self) -> bool:
        """Validate Anthropic configuration"""
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")
        if not self.model:
            raise ValueError("Model not specified")
        return True
    
    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 4096, **kwargs) -> str:
        """Generate text using Claude API"""
        try:
            from anthropic import Anthropic
        except ImportError:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")
        
        self.validate_config()
        
        client = Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system="You are a helpful assistant for generating mobile app code.",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            **kwargs
        )
        
        return response.content[0].text
    
    def generate_with_response(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate text and return LLMResponse object"""
        try:
            from anthropic import Anthropic
        except ImportError:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")
        
        self.validate_config()
        
        client = Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model=self.model,
            system="You are a helpful assistant for generating mobile app code.",
            messages=[
                {"role": "user", "content": prompt}
            ],
            **kwargs
        )
        
        return LLMResponse(
            content=response.content[0].text,
            model=self.model,
            usage={
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.input_tokens + response.usage.output_tokens,
            }
        )
