"""
LLM Provider Manager for handling different LLM providers and their configurations.
"""

from typing import Dict, Any, Optional
from config import LLM_PROVIDERS


class LLMProviderManager:
    """Manages LLM provider configurations and creates provider strings for Crawl4AI."""
    
    def __init__(self):
        self.providers = LLM_PROVIDERS
    
    def get_provider_list(self) -> Dict[str, str]:
        """Get a dictionary of provider keys and display names."""
        return {key: config["name"] for key, config in self.providers.items()}
    
    def get_models_for_provider(self, provider_key: str) -> Dict[str, str]:
        """Get available models for a specific provider."""
        if provider_key not in self.providers:
            raise ValueError(f"Unknown provider: {provider_key}")
        return self.providers[provider_key]["models"]
    
    def get_provider_info(self, provider_key: str) -> Dict[str, Any]:
        """Get complete information about a provider."""
        if provider_key not in self.providers:
            raise ValueError(f"Unknown provider: {provider_key}")
        return self.providers[provider_key]
    
    def create_provider_string(self, provider_key: str, model_key: str) -> str:
        """Create the provider string format expected by Crawl4AI/LiteLLM."""
        if provider_key not in self.providers:
            raise ValueError(f"Unknown provider: {provider_key}")
        
        if model_key not in self.providers[provider_key]["models"]:
            raise ValueError(f"Unknown model {model_key} for provider {provider_key}")
        
        # Handle special cases for provider string format
        if provider_key == "openai":
            return f"openai/{model_key}"
        elif provider_key == "gemini":
            return f"gemini/{model_key}"
        elif provider_key == "deepseek":
            return f"deepseek/{model_key}"
        elif provider_key == "anthropic":
            return f"anthropic/{model_key}"
        elif provider_key == "mistral":
            return f"mistral/{model_key}"
        elif provider_key == "xai":
            return f"xai/{model_key}"
        else:
            # Default format
            return f"{provider_key}/{model_key}"
    
    def validate_api_key(self, api_key: str) -> bool:
        """Basic validation for API key format."""
        if not api_key or len(api_key.strip()) < 10:
            return False
        return True
    
    def get_default_model(self, provider_key: str) -> str:
        """Get the default/recommended model for a provider."""
        if provider_key not in self.providers:
            raise ValueError(f"Unknown provider: {provider_key}")
        
        models = self.providers[provider_key]["models"]
        # Return the first model as default
        return list(models.keys())[0]
    
    def get_cost_info(self, provider_key: str, model_key: str) -> str:
        """Get cost information for a provider/model combination."""
        cost_info = {
            "openai": {
                "gpt-4o": "💰💰💰 Premium pricing",
                "gpt-4o-mini": "💰 Very cost-effective",
                "gpt-4-turbo": "💰💰💰 Premium pricing",
                "gpt-3.5-turbo": "💰 Low cost"
            },
            "gemini": {
                "gemini-2.5-pro": "💰💰 Moderate cost",
                "gemini-2.5-flash": "💰 Low cost, fast",
                "gemini-1.5-pro": "💰💰 Moderate cost",
                "gemini-1.5-flash": "💰 Low cost"
            },
            "deepseek": {
                "deepseek-v3": "💰 Very cost-effective",
                "deepseek-r1": "💰 Very cost-effective",
                "deepseek-v2.5": "💰 Very cost-effective",
                "deepseek-coder-v2": "💰 Very cost-effective"
            },
            "anthropic": {
                "claude-3.5-sonnet": "💰💰💰 Premium pricing",
                "claude-3.5-haiku": "💰 Low cost, fast",
                "claude-3-opus": "💰💰💰💰 Highest cost",
                "claude-3-sonnet": "💰💰 Moderate cost"
            },
            "mistral": {
                "mistral-large-2": "💰💰 Moderate cost",
                "mistral-medium-3": "💰💰 Moderate cost",
                "mistral-small-3": "💰 Low cost",
                "codestral": "💰 Low cost"
            },
            "xai": {
                "grok-3": "💰💰 Moderate cost",
                "grok-3-reasoning": "💰💰💰 Higher cost",
                "grok-beta": "💰💰 Moderate cost"
            }
        }
        
        return cost_info.get(provider_key, {}).get(model_key, "💰 Cost varies") 