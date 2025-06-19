import streamlit as st
import asyncio
import pandas as pd
import sys
import nest_asyncio
import threading
from crawler_logic import crawl_venues

# Fix for Windows asyncio subprocess issue
nest_asyncio.apply()

if sys.platform == "win32":
    # Use ProactorEventLoop for Windows
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="Dynamic AI Web Crawler")

# --- Default Values (for user convenience) ---
DEFAULT_URL = "https://www.oto.com/mobil-bekas/jakarta-pusat"
DEFAULT_SELECTOR = "[class^='card splide__slide shadow-light']"
DEFAULT_KEYS = "nama, harga, tahun, transmisi, jarak_tempuh, lokasi"
DEFAULT_PROMPT = """
You are an expert data extraction AI. Based on the provided HTML snippet of a used car listing, extract the following pieces of information. Ensure the data is clean and accurate. If a piece of information is not present, leave it as null.

- **nama**: The full name or title of the car model.
- **harga**: The price of the car, formatted as a string (e.g., "Rp 250 Juta").
- **tahun**: The manufacturing year of the car.
- **transmisi**: The type of transmission (e.g., "Otomatis", "Manual").
- **jarak_tempuh**: The mileage of the car (e.g., "10.000-15.000 km").
- **lokasi**: The city or general location of the car dealership.
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
    api_key = st.text_input("Your Google API Key", type="password")

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
    if not api_key:
        st.sidebar.error("API Key is required to run the crawler.")
    else:
        log_container.empty()
        result_area.empty()
        st.sidebar.info("Crawler started! See logs for progress.")

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
                        progress_callback=log_callback
                    ))
                finally:
                    loop.close()

            # Run the crawler in a separate thread
            results = run_async_crawler()

            if results:
                st.success(f"Crawling complete! Found {len(results)} unique items.")
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
                st.warning("Crawling finished, but no data was extracted.")

        except Exception as e:
            st.error(f"An error occurred during crawling: {e}")
            st.exception(e)  # Provides a full traceback for debugging 