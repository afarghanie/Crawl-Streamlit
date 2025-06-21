import streamlit as st
import asyncio
import pandas as pd
import sys
import nest_asyncio
import threading
from crawler_logic import crawl_venues
from utils.llm_provider_manager import LLMProviderManager
from config import DEFAULT_LLM_PROVIDER, DEFAULT_LLM_MODEL

# Fix for Windows asyncio subprocess issue
nest_asyncio.apply()

if sys.platform == "win32":
    # Use ProactorEventLoop for Windows
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="Dynamic AI Web Crawler")

# Initialize LLM Provider Manager
@st.cache_resource
def get_llm_provider_manager():
    return LLMProviderManager()

provider_manager = get_llm_provider_manager()

# --- Default Values (for user convenience) ---
DEFAULT_URL = "https://www.lamudi.co.id/jual/?q=jakarta"
DEFAULT_SELECTOR = "[class*='ListingCell'], [class*='PropertyCard'], [class*='listing-item']"
DEFAULT_KEYS = "title, harga, deskripsi, lokasi, jenis_properti, jumlah_tempat_tidur, jumlah_kamar_mandi, luas_properti_m2"
DEFAULT_PROMPT = """
You are an expert data extraction AI. Based on the provided HTML snippet of a property listing, extract the following pieces of information. Ensure the data is clean and accurate. If a piece of information is not present, leave it as null.

- **title**: The full title or name of the property listing.
- **harga**: The price of the property, formatted as a string (e.g., "Rp 2,5 Miliar", "Rp 500 Juta").
- **deskripsi**: The detailed description of the property.
- **lokasi**: The specific location or address of the property (e.g., "Jakarta Selatan", "Surabaya Pusat").
- **jenis_properti**: The type of property (e.g., "Apartemen", "Rumah", "Tanah", "Ruko").
- **jumlah_tempat_tidur**: The number of bedrooms in the property, as an integer.
- **jumlah_kamar_mandi**: The number of bathrooms in the property, as an integer.
- **luas_properti_m2**: The area of the property in square meters, as a numeric value.

Extract all available information from the HTML. If any field is not found, set it to null. For numeric fields, extract only the numbers without units.
"""

# --- UI Definition ---
st.title("🚀 Dynamic AI Web Crawler")
st.markdown("""
This application allows you to configure and run a web crawler powered by AI. 
You can customize the target website, data extraction rules, and AI behavior all from this interface.
""")

with st.sidebar:
    st.header("⚙️ Crawler Configuration")
    base_url = st.text_input("Target URL", value=DEFAULT_URL)
    css_selector = st.text_input("CSS Selector for Items", value=DEFAULT_SELECTOR)
    
    st.divider()
    
    # LLM Provider Selection
    st.header("🤖 LLM Provider Configuration")
    
    # Provider selection
    provider_options = provider_manager.get_provider_list()
    selected_provider = st.selectbox(
        "Choose LLM Provider",
        options=list(provider_options.keys()),
        format_func=lambda x: provider_options[x],
        index=list(provider_options.keys()).index(DEFAULT_LLM_PROVIDER) if DEFAULT_LLM_PROVIDER in provider_options else 0,
        help="Select which LLM provider to use for data extraction"
    )
    
    # Model selection based on provider
    if selected_provider:
        provider_info = provider_manager.get_provider_info(selected_provider)
        model_options = provider_info["models"]
        
        # Create a formatted display for models with cost info
        def format_model_option(model_key):
            model_name = model_options[model_key]
            cost_info = provider_manager.get_cost_info(selected_provider, model_key)
            return f"{model_name} - {cost_info}"
        
        selected_model = st.selectbox(
            f"Choose {provider_info['name']} Model",
            options=list(model_options.keys()),
            format_func=format_model_option,
            index=list(model_options.keys()).index(DEFAULT_LLM_MODEL) if DEFAULT_LLM_MODEL in model_options else 0,
            help="Select which model to use. Consider cost and performance trade-offs."
        )
        
        # API Key input
        api_key = st.text_input(
            provider_info["api_key_name"],
            type="password",
            help=provider_info["help_text"]
        )
        
        # Display provider info
        st.info(f"**Selected:** {provider_info['name']} - {model_options[selected_model]}")
        
        # Display cost information
        cost_info = provider_manager.get_cost_info(selected_provider, selected_model)
        st.caption(f"💡 **Cost:** {cost_info}")
    
    st.divider()
    
    # Page limit configuration
    st.subheader("📄 Page Configuration")
    use_page_limit = st.checkbox("Set maximum pages to crawl", value=False, help="Enable to limit the number of pages crawled")
    max_pages = st.number_input(
        "Maximum pages to crawl",
        min_value=1,
        max_value=100,
        value=10,
        help="Set to 0 or disable checkbox to crawl until no more data is available"
    ) if use_page_limit else None

    st.divider()

    st.header("🧠 AI & Data Configuration")
    system_prompt_input = st.text_area(
        "System Prompt for AI",
        value=DEFAULT_PROMPT,
        height=300,
        help="Instructions for the AI on how to extract data from the HTML content"
    )
    required_keys_input = st.text_input(
        "Data Keys (comma-separated)",
        value=DEFAULT_KEYS,
        help="The fields that should be extracted from each item"
    )
    output_filename = st.text_input(
        "Output CSV Filename",
        value="crawled_data.csv",
        help="Name of the file to save the results"
    )

    st.divider()
    start_button = st.button("Start Crawling", type="primary", use_container_width=True)

# --- Output Area ---
st.subheader("📝 Live Log")
log_container = st.container(height=200, border=True)

st.subheader("📊 Crawling Results")
result_area = st.empty()
result_area.info("Results will be displayed here once the crawling is complete.")

# --- Backend Logic ---
if start_button:
    # Validation
    if not api_key:
        st.sidebar.error(f"{provider_info['api_key_name']} is required to run the crawler.")
    elif not provider_manager.validate_api_key(api_key):
        st.sidebar.error("Please enter a valid API key (minimum 10 characters).")
    else:
        log_container.empty()
        result_area.empty()
        st.sidebar.info(f"Crawler started using {provider_info['name']}! See logs for progress.")

        def log_callback(message):
            with log_container:
                st.info(message)

        try:
            # Create a new event loop for this thread
            def run_async_crawler():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    return loop.run_until_complete(crawl_venues(
                        base_url=base_url,
                        css_selector=css_selector,
                        api_key=api_key,
                        system_prompt=system_prompt_input,
                        required_keys_str=required_keys_input,
                        progress_callback=log_callback,
                        use_page_limit=use_page_limit,
                        max_pages=max_pages,
                        llm_provider=selected_provider,
                        llm_model=selected_model
                    ))
                finally:
                    loop.close()

            # Run the crawler in a separate thread
            results = run_async_crawler()

            if results:
                st.success(f"Crawling complete! Found {len(results)} unique items using {provider_info['name']} {model_options[selected_model]}.")
                df = pd.DataFrame(results)
                result_area.dataframe(df, use_container_width=True)

                csv_data = df.to_csv(index=False).encode('utf-8')
                st.sidebar.download_button(
                    label="📥 Download Results as CSV",
                    data=csv_data,
                    file_name=output_filename,
                    mime='text/csv',
                    use_container_width=True
                )
            else:
                st.warning("Crawling finished, but no data was extracted. Please check your configuration and try again.")

        except Exception as e:
            st.error(f"An error occurred during crawling: {e}")
            st.exception(e)  # Provides a full traceback for debugging

# --- Provider Information Section ---
with st.expander("ℹ️ LLM Provider Information"):
    st.markdown("""
    ### Supported LLM Providers
    
    This crawler supports multiple LLM providers through LiteLLM integration. Here's what you need to know:
    
    **🔑 API Keys**: Each provider requires its own API key. Click the help text next to each API key field for instructions.
    
    **💰 Cost Considerations**:
    - 💰 = Low cost (recommended for testing)
    - 💰💰 = Moderate cost 
    - 💰💰💰 = Higher cost
    - 💰💰💰💰 = Premium pricing
    
    **⚡ Performance**:
    - "Fast" models prioritize speed over accuracy
    - "Pro" models offer best quality but cost more
    - "Mini" models are cost-effective alternatives
    
    **🛡️ Privacy**: API keys are not stored and are only used for the current session.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **OpenAI**
        - Most established provider
        - Excellent for general tasks
        - GPT-4o recommended for quality
        - GPT-4o Mini for cost efficiency
        """)
        
        st.markdown("""
        **Google Gemini**
        - Great balance of cost and quality
        - Strong multimodal capabilities
        - Flash models are very fast
        - Pro models for complex tasks
        """)
        
        st.markdown("""
        **DeepSeek**
        - Extremely cost-effective
        - Open-source models
        - Great for coding tasks
        - R1 model for reasoning
        """)
    
    with col2:
        st.markdown("""
        **Anthropic Claude**
        - Excellent for analysis and reasoning
        - Strong safety measures
        - Haiku for speed, Opus for quality
        - Great for complex instructions
        """)
        
        st.markdown("""
        **Mistral AI**
        - European provider
        - Good balance of features
        - Codestral specialized for code
        - Open-source options available
        """)
        
        st.markdown("""
        **xAI Grok**
        - Real-time information access
        - Conversational and creative
        - Reasoning capabilities
        - Latest technology
        """) 