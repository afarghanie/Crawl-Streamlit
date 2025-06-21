# config.py


# BASE_URL = "https://www.carsome.id/beli-mobil-bekas"
# CSS_SELECTOR = "[class^='list-card__item']"

BASE_URL = "https://www.oto.com/mobil-bekas/jakarta-pusat"
CSS_SELECTOR = "[class^='card splide__slide shadow-light filter-listing-card used-car-card']"


REQUIRED_KEYS = [
    "title",
    "image_url",
    "brand",
    "model",
    "year",
    "km",
    "price",
    "currency", # e.g., IDR, USD
    "transmission",
    "fuel",
    "city",
    "seller_name"
    # "listing_id"
]

# LLM Provider Configurations
LLM_PROVIDERS = {
    "openai": {
        "name": "OpenAI",
        "models": {
            "gpt-4o": "GPT-4o (Latest)",
            "gpt-4o-mini": "GPT-4o Mini (Cost-effective)",
            "gpt-4-turbo": "GPT-4 Turbo",
            "gpt-3.5-turbo": "GPT-3.5 Turbo (Legacy)"
        },
        "api_key_name": "OpenAI API Key",
        "help_text": "Get your API key from https://platform.openai.com/api-keys"
    },
    "gemini": {
        "name": "Google Gemini",
        "models": {
            "gemini-2.5-pro": "Gemini 2.5 Pro (Latest)",
            "gemini-2.5-flash": "Gemini 2.5 Flash (Fast)",
            "gemini-1.5-pro": "Gemini 1.5 Pro",
            "gemini-1.5-flash": "Gemini 1.5 Flash"
        },
        "api_key_name": "Google API Key",
        "help_text": "Get your API key from https://aistudio.google.com/app/apikey"
    },
    "deepseek": {
        "name": "DeepSeek",
        "models": {
            "deepseek-v3": "DeepSeek V3 (Latest)",
            "deepseek-r1": "DeepSeek R1 (Reasoning)",
            "deepseek-v2.5": "DeepSeek V2.5",
            "deepseek-coder-v2": "DeepSeek Coder V2"
        },
        "api_key_name": "DeepSeek API Key",
        "help_text": "Get your API key from https://platform.deepseek.com/api_keys"
    },
    "anthropic": {
        "name": "Anthropic Claude",
        "models": {
            "claude-3.5-sonnet": "Claude 3.5 Sonnet (Latest)",
            "claude-3.5-haiku": "Claude 3.5 Haiku (Fast)",
            "claude-3-opus": "Claude 3 Opus (Most Capable)",
            "claude-3-sonnet": "Claude 3 Sonnet"
        },
        "api_key_name": "Anthropic API Key",
        "help_text": "Get your API key from https://console.anthropic.com/account/keys"
    },
    "mistral": {
        "name": "Mistral AI",
        "models": {
            "mistral-large-2": "Mistral Large 2 (Latest)",
            "mistral-medium-3": "Mistral Medium 3",
            "mistral-small-3": "Mistral Small 3",
            "codestral": "Codestral (Code)"
        },
        "api_key_name": "Mistral API Key",
        "help_text": "Get your API key from https://console.mistral.ai/api-keys/"
    },
    "xai": {
        "name": "xAI Grok",
        "models": {
            "grok-3": "Grok 3 (Latest)",
            "grok-3-reasoning": "Grok 3 Reasoning",
            "grok-beta": "Grok Beta"
        },
        "api_key_name": "xAI API Key",
        "help_text": "Get your API key from https://console.x.ai/team"
    }
}

# Default LLM Configuration
DEFAULT_LLM_PROVIDER = "gemini"
DEFAULT_LLM_MODEL = "gemini-2.5-flash"
