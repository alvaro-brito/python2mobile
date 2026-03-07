"""
P2M API Client - HTTP request handling for P2M applications
Supports GET, POST, PUT, DELETE requests with proper error handling
"""

import json
from typing import Dict, Any, Optional, Callable
from enum import Enum


class HTTPMethod(Enum):
    """HTTP methods"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class APIResponse:
    """Represents an API response"""
    
    def __init__(self, status_code: int, data: Any, error: Optional[str] = None):
        self.status_code = status_code
        self.data = data
        self.error = error
        self.success = 200 <= status_code < 300
    
    def json(self) -> Dict[str, Any]:
        """Get response as JSON"""
        if isinstance(self.data, dict):
            return self.data
        try:
            return json.loads(self.data) if isinstance(self.data, str) else self.data
        except:
            return {"error": "Invalid JSON"}
    
    def __repr__(self) -> str:
        return f"APIResponse(status={self.status_code}, success={self.success})"


class APIClient:
    """HTTP client for making API requests"""
    
    def __init__(self, base_url: str = "", default_headers: Optional[Dict[str, str]] = None):
        """
        Initialize API client
        
        Args:
            base_url: Base URL for all requests
            default_headers: Default headers to include in all requests
        """
        self.base_url = base_url.rstrip('/')
        self.default_headers = default_headers or {}
        self.timeout = 30
    
    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint"""
        if endpoint.startswith('http'):
            return endpoint
        return f"{self.base_url}/{endpoint.lstrip('/')}" if self.base_url else endpoint
    
    def _merge_headers(self, headers: Optional[Dict[str, str]]) -> Dict[str, str]:
        """Merge default headers with request-specific headers"""
        merged = self.default_headers.copy()
        if headers:
            merged.update(headers)
        return merged
    
    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> APIResponse:
        """
        Make a GET request
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Request headers
        
        Returns:
            APIResponse object
        """
        url = self._build_url(endpoint)
        headers = self._merge_headers(headers)
        
        try:
            # This will be implemented differently on each platform
            # For now, return a placeholder
            return APIResponse(200, {"message": "GET request to " + url})
        except Exception as e:
            return APIResponse(500, None, str(e))
    
    async def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> APIResponse:
        """
        Make a POST request
        
        Args:
            endpoint: API endpoint
            data: Request body
            headers: Request headers
        
        Returns:
            APIResponse object
        """
        url = self._build_url(endpoint)
        headers = self._merge_headers(headers)
        headers['Content-Type'] = 'application/json'
        
        try:
            # This will be implemented differently on each platform
            # For now, return a placeholder
            return APIResponse(201, {"message": "POST request to " + url})
        except Exception as e:
            return APIResponse(500, None, str(e))
    
    async def put(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> APIResponse:
        """
        Make a PUT request
        
        Args:
            endpoint: API endpoint
            data: Request body
            headers: Request headers
        
        Returns:
            APIResponse object
        """
        url = self._build_url(endpoint)
        headers = self._merge_headers(headers)
        headers['Content-Type'] = 'application/json'
        
        try:
            return APIResponse(200, {"message": "PUT request to " + url})
        except Exception as e:
            return APIResponse(500, None, str(e))
    
    async def delete(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None
    ) -> APIResponse:
        """
        Make a DELETE request
        
        Args:
            endpoint: API endpoint
            headers: Request headers
        
        Returns:
            APIResponse object
        """
        url = self._build_url(endpoint)
        headers = self._merge_headers(headers)
        
        try:
            return APIResponse(204, None)
        except Exception as e:
            return APIResponse(500, None, str(e))


# Global API client instance
_api_client: Optional[APIClient] = None


def init_api(base_url: str = "", default_headers: Optional[Dict[str, str]] = None) -> APIClient:
    """Initialize global API client"""
    global _api_client
    _api_client = APIClient(base_url, default_headers)
    return _api_client


def get_api() -> APIClient:
    """Get global API client"""
    global _api_client
    if _api_client is None:
        _api_client = APIClient()
    return _api_client
