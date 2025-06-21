#!/usr/bin/env python3
"""
Test script for LLM Provider Manager functionality.
Run this to validate the provider configuration system before using the main app.
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.llm_provider_manager import LLMProviderManager

def test_provider_manager():
    """Test the LLM Provider Manager functionality."""
    print("🧪 Testing LLM Provider Manager...")
    print("=" * 50)
    
    # Initialize provider manager
    manager = LLMProviderManager()
    
    # Test 1: Get provider list
    print("\n1️⃣ Testing provider list:")
    providers = manager.get_provider_list()
    for key, name in providers.items():
        print(f"   {key} -> {name}")
    
    # Test 2: Test each provider's models
    print("\n2️⃣ Testing provider models:")
    for provider_key in providers.keys():
        try:
            models = manager.get_models_for_provider(provider_key)
            print(f"   {providers[provider_key]}:")
            for model_key, model_name in models.items():
                cost = manager.get_cost_info(provider_key, model_key)
                print(f"     - {model_key}: {model_name} ({cost})")
        except Exception as e:
            print(f"   ❌ Error with {provider_key}: {e}")
    
    # Test 3: Test provider strings
    print("\n3️⃣ Testing provider string generation:")
    test_cases = [
        ("openai", "gpt-4o"),
        ("gemini", "gemini-2.5-flash"),
        ("deepseek", "deepseek-v3"),
        ("anthropic", "claude-3.5-sonnet"),
        ("mistral", "mistral-large-2"),
        ("xai", "grok-3")
    ]
    
    for provider, model in test_cases:
        try:
            provider_string = manager.create_provider_string(provider, model)
            print(f"   {provider}/{model} -> {provider_string}")
        except Exception as e:
            print(f"   ❌ Error with {provider}/{model}: {e}")
    
    # Test 4: Test API key validation
    print("\n4️⃣ Testing API key validation:")
    test_keys = [
        ("", False),
        ("short", False),
        ("sk-1234567890abcdef", True),
        ("AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", True),
        ("sk-ant-1234567890abcdef", True)
    ]
    
    for key, expected in test_keys:
        result = manager.validate_api_key(key)
        status = "✅" if result == expected else "❌"
        print(f"   {status} '{key[:10]}...' -> {result} (expected {expected})")
    
    # Test 5: Test error handling
    print("\n5️⃣ Testing error handling:")
    try:
        manager.get_provider_info("nonexistent")
        print("   ❌ Should have raised error for nonexistent provider")
    except ValueError:
        print("   ✅ Correctly raised error for nonexistent provider")
    
    try:
        manager.create_provider_string("openai", "nonexistent-model")
        print("   ❌ Should have raised error for nonexistent model")
    except ValueError:
        print("   ✅ Correctly raised error for nonexistent model")
    
    print("\n" + "=" * 50)
    print("🎉 Provider Manager tests completed!")
    print("\nNext steps:")
    print("1. Get an API key from your preferred provider")
    print("2. Run: streamlit run app.py")
    print("3. Select your provider and model in the UI")
    print("4. Start crawling!")

if __name__ == "__main__":
    test_provider_manager() 