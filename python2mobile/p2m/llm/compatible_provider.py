"""
P2M LLM Compatible Provider - OpenAI-compatible API integration
"""

import requests
from typing import Optional
from p2m.llm.base import LLMProvider, LLMResponse


class CompatibleProvider(LLMProvider):
    """OpenAI-compatible API provider"""
    
    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: str,
        x_api_key: Optional[str] = None,
    ):
        super().__init__(api_key=api_key, model=model)
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.x_api_key = x_api_key
        self.api_endpoint = f"{self.base_url}/v1/chat/completions"
    
    def validate_config(self) -> bool:
        """Validate compatible provider configuration"""
        if not self.base_url:
            raise ValueError("base_url not specified")
        if not self.api_key:
            raise ValueError("api_key not specified")
        if not self.model:
            raise ValueError("model not specified")
        return True
    
    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 4096, **kwargs) -> str:
        """Generate text using OpenAI-compatible API"""
        self.validate_config()
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        
        # Add custom API key header if provided
        if self.x_api_key:
            headers["x-api-key"] = self.x_api_key
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant for generating mobile app code."},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        try:
            response = requests.post(
                self.api_endpoint,
                json=payload,
                headers=headers,
                timeout=300,
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"API error: {response.status_code} - {response.text}")
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except requests.RequestException as e:
            raise RuntimeError(f"API request failed: {e}")
    
    def generate_with_response(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate text and return LLMResponse object"""
        self.validate_config()
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        
        # Add custom API key header if provided
        if self.x_api_key:
            headers["x-api-key"] = self.x_api_key
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant for generating mobile app code."},
                {"role": "user", "content": prompt}
            ],
        }
        
        try:
            response = requests.post(
                self.api_endpoint,
                json=payload,
                headers=headers,
                timeout=300,
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"API error: {response.status_code} - {response.text}")
            
            result = response.json()
            
            return LLMResponse(
                content=result["choices"][0]["message"]["content"],
                model=self.model,
                usage={
                    "prompt_tokens": result.get("usage", {}).get("prompt_tokens", 0),
                    "completion_tokens": result.get("usage", {}).get("completion_tokens", 0),
                    "total_tokens": result.get("usage", {}).get("total_tokens", 0),
                }
            )
        except requests.RequestException as e:
            raise RuntimeError(f"API request failed: {e}")
