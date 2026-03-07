"""
P2M LLM Ollama Provider - Local Ollama integration
"""

import requests
from typing import Optional
from p2m.llm.base import LLMProvider, LLMResponse


class OllamaProvider(LLMProvider):
    """Ollama local LLM provider"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        super().__init__(model=model)
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.api_endpoint = f"{self.base_url}/api/generate"
    
    def validate_config(self) -> bool:
        """Validate Ollama configuration"""
        if not self.model:
            raise ValueError("Model not specified")
        
        # Check if Ollama is running
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code != 200:
                raise ValueError(f"Ollama server not responding: {response.status_code}")
        except requests.ConnectionError:
            raise ValueError(f"Cannot connect to Ollama at {self.base_url}")
        
        return True
    
    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 4096, **kwargs) -> str:
        """Generate text using Ollama"""
        self.validate_config()
        
        try:
            response = requests.post(
                self.api_endpoint,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "temperature": temperature,
                    "num_predict": max_tokens,
                    "stream": False,
                },
                timeout=300,
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"Ollama API error: {response.status_code}")
            
            result = response.json()
            return result.get("response", "")
        except requests.RequestException as e:
            raise RuntimeError(f"Ollama request failed: {e}")
    
    def generate_with_response(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate text and return LLMResponse object"""
        self.validate_config()
        
        try:
            response = requests.post(
                self.api_endpoint,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=300,
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"Ollama API error: {response.status_code}")
            
            result = response.json()
            
            return LLMResponse(
                content=result.get("response", ""),
                model=self.model,
                usage={
                    "prompt_tokens": result.get("prompt_eval_count", 0),
                    "completion_tokens": result.get("eval_count", 0),
                    "total_tokens": result.get("prompt_eval_count", 0) + result.get("eval_count", 0),
                }
            )
        except requests.RequestException as e:
            raise RuntimeError(f"Ollama request failed: {e}")
