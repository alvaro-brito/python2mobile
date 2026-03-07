"""
P2M LLM OpenAI Provider - OpenAI API integration
"""

import os
from typing import Optional
from p2m.llm.base import LLMProvider, LLMResponse


class OpenAIProvider(LLMProvider):
    """OpenAI API provider"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o"):
        super().__init__(api_key=api_key, model=model)
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.base_url = "https://api.openai.com/v1"
    
    def validate_config(self) -> bool:
        """Validate OpenAI configuration"""
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not set")
        if not self.model:
            raise ValueError("Model not specified")
        return True
    
    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 4096, **kwargs) -> str:
        """Generate text using OpenAI API"""
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")
        
        self.validate_config()
        
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant for generating mobile app code."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        return response.choices[0].message.content
    
    def generate_with_response(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate text and return LLMResponse object"""
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")
        
        self.validate_config()
        
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant for generating mobile app code."},
                {"role": "user", "content": prompt}
            ],
            **kwargs
        )
        
        return LLMResponse(
            content=response.choices[0].message.content,
            model=self.model,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }
        )
