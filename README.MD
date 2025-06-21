# 🚀 Dynamic AI Web Crawler

A powerful, configurable web crawler that uses AI to extract structured data from websites. Now supports multiple LLM providers for maximum flexibility and cost optimization!

## ✨ New Feature: Multi-LLM Provider Support

Choose from 6 different LLM providers to power your web crawling:

### 🤖 Supported Providers

| Provider | Models | Cost | Best For |
|----------|--------|------|----------|
| **OpenAI** | GPT-4o, GPT-4o Mini, GPT-4 Turbo | 💰💰💰 | General purpose, high quality |
| **Google Gemini** | 2.5 Pro, 2.5 Flash, 1.5 Pro | 💰💰 | Fast processing, good balance |
| **DeepSeek** | V3, R1, V2.5, Coder V2 | 💰 | Cost-effective, coding tasks |
| **Anthropic Claude** | 3.5 Sonnet, 3.5 Haiku, 3 Opus | 💰💰💰 | Analysis, reasoning, safety |
| **Mistral AI** | Large 2, Medium 3, Small 3 | 💰💰 | European provider, open models |
| **xAI Grok** | Grok 3, Grok 3 Reasoning | 💰💰 | Real-time data, creativity |

## 🔧 Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Crawler-main
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get API Keys:**
   Choose your preferred LLM provider and get an API key:
   
   - **OpenAI**: https://platform.openai.com/api-keys
   - **Google Gemini**: https://aistudio.google.com/app/apikey
   - **DeepSeek**: https://platform.deepseek.com/api_keys
   - **Anthropic**: https://console.anthropic.com/account/keys
   - **Mistral AI**: https://console.mistral.ai/api-keys/
   - **xAI**: https://console.x.ai/team

## 🚀 Quick Start

1. **Run the application:**
   ```bash
   streamlit run app.py
   ```

2. **Configure your crawler:**
   - Enter target URL and CSS selector
   - Choose your LLM provider and model
   - Enter your API key
   - Customize data extraction fields
   - Set crawling limits (optional)

3. **Start crawling:**
   Click "Start Crawling" and watch the live progress!

## 💡 Provider Selection Guide

### 🔸 For Beginners
- **Gemini 2.5 Flash**: Great balance of cost, speed, and quality
- **DeepSeek V3**: Extremely cost-effective for testing

### 🔸 For Production
- **OpenAI GPT-4o**: Highest quality results
- **Claude 3.5 Sonnet**: Best for complex analysis
- **Gemini 2.5 Pro**: Good balance for large-scale crawling

### 🔸 For Budget-Conscious
- **DeepSeek R1**: Best value for reasoning tasks
- **Gemini 2.5 Flash**: Fast and affordable
- **Claude 3.5 Haiku**: Anthropic's cost-effective option

## 📊 Features

### Core Functionality
- ✅ **Multi-Provider LLM Support**: Choose from 6 different providers
- ✅ **Dynamic Configuration**: Customize everything from the UI
- ✅ **Real-time Progress**: Live logging of crawling progress
- ✅ **Data Export**: Download results as CSV
- ✅ **Page Limiting**: Control crawling scope
- ✅ **Error Handling**: Robust error management

### LLM Provider Features
- ✅ **Cost Estimation**: Visual cost indicators for each model
- ✅ **Performance Info**: Speed vs. quality trade-offs
- ✅ **API Key Validation**: Basic validation before crawling
- ✅ **Provider Information**: Detailed help for each provider

## 🛠️ Configuration

### Basic Configuration
```python
# In config.py
DEFAULT_LLM_PROVIDER = "gemini"  # Change default provider
DEFAULT_LLM_MODEL = "gemini-2.5-flash"  # Change default model
```

### Adding New Providers
To add a new LLM provider, update the `LLM_PROVIDERS` dictionary in `config.py`:

```python
LLM_PROVIDERS["new_provider"] = {
    "name": "New Provider",
    "models": {
        "model-1": "Model 1 Description",
        "model-2": "Model 2 Description"
    },
    "api_key_name": "New Provider API Key",
    "help_text": "Instructions for getting API key"
}
```

## 📝 Usage Examples

### Real Estate Crawling
```
URL: https://www.lamudi.co.id/jual/?q=jakarta
CSS Selector: [class*='ListingCell'], [class*='PropertyCard']
Data Keys: title, price, location, bedrooms, bathrooms, area
Provider: Gemini 2.5 Flash (fast and cost-effective)
```

### E-commerce Product Data
```
URL: https://www.tokopedia.com/search?q=laptop
CSS Selector: [data-testid='divProductWrapper']
Data Keys: title, price, rating, seller, location, specifications
Provider: DeepSeek V3 (very cost-effective)
```

### News Article Extraction
```
URL: https://news.website.com/category
CSS Selector: .article-item, .news-card
Data Keys: title, summary, author, date, category, url
Provider: Claude 3.5 Sonnet (excellent for text analysis)
```

## 🔍 Advanced Features

### Custom System Prompts
Tailor the AI's behavior for your specific use case:

```
You are a specialized real estate data extractor. Focus on:
1. Accurate price extraction (handle currency formats)
2. Property type classification
3. Location normalization
4. Feature counting (rooms, bathrooms)

Always return null for missing data, never guess.
```

### Error Handling
The application includes comprehensive error handling:
- Invalid API keys
- Network timeouts
- Malformed responses
- Provider-specific errors

### Performance Optimization
- Automatic retry logic
- Intelligent chunking for large pages
- Concurrent processing where possible
- Memory-efficient data handling

## 🎯 Tips for Success

### 1. **Choose the Right Provider**
- **Testing**: Start with DeepSeek or Gemini Flash
- **Production**: Use OpenAI GPT-4o or Claude Sonnet
- **Budget**: DeepSeek offers incredible value

### 2. **Optimize CSS Selectors**
- Be specific but not too narrow
- Test selectors in browser dev tools
- Use multiple selectors separated by commas

### 3. **Craft Good Prompts**
- Be specific about data formats
- Handle edge cases explicitly
- Include examples when helpful

### 4. **Monitor Costs**
- Check provider pricing pages
- Use cost-effective models for testing
- Set page limits for expensive models

## 🛡️ Security & Privacy

- **API Keys**: Never stored, only used during session
- **Data**: Processed locally, not sent to third parties
- **Rate Limiting**: Respectful delays between requests
- **Error Logging**: No sensitive data in logs

## 🐛 Troubleshooting

### Common Issues

**API Key Invalid**
- Check key format and permissions
- Ensure billing is set up (for paid providers)
- Try regenerating the key

**No Data Extracted**
- Verify CSS selectors work
- Check if site requires login
- Adjust system prompt for better guidance

**Slow Performance**
- Use faster models (Flash, Haiku, Mini variants)
- Reduce page limits
- Simplify data extraction requirements

**Rate Limiting**
- Increase delays between requests
- Use providers with higher rate limits
- Consider paid tiers for higher limits

## 📚 Technical Details

### Architecture
```
app.py (Streamlit UI)
├── crawler_logic.py (Core crawling)
├── config.py (Provider configurations)
└── utils/
    └── llm_provider_manager.py (Provider management)
```

### Dependencies
- **Crawl4AI**: Web crawling engine
- **LiteLLM**: Multi-provider LLM interface
- **Streamlit**: Web interface
- **Pandas**: Data handling
- **Pydantic**: Data validation

### Provider String Format
The application uses LiteLLM's provider string format:
```
"openai/gpt-4o"
"gemini/gemini-2.5-flash"
"deepseek/deepseek-v3"
"anthropic/claude-3.5-sonnet"
```

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional LLM providers
- Better error handling
- Performance optimizations
- UI enhancements
- Documentation improvements

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Crawl4AI**: Powerful crawling framework
- **LiteLLM**: Universal LLM interface
- **Streamlit**: Beautiful web apps framework
- All the LLM providers for their amazing APIs

---

**Happy Crawling! 🕷️✨**

Need help? Check the provider information section in the app or create an issue in the repository.
