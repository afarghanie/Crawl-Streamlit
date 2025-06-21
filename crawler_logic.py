import asyncio
import json
from typing import List, Set, Dict, Any, Callable
from pydantic import create_model, Field
from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
    LLMExtractionStrategy,
)
from utils.llm_provider_manager import LLMProviderManager

def get_browser_config() -> BrowserConfig:
    """Returns the browser configuration for the crawler."""
    return BrowserConfig(
        browser_type="chromium",
        headless=False,  # Changed to non-headless to help with dynamic content
        verbose=True
    )

async def check_no_results(
    crawler: AsyncWebCrawler,
    url: str,
    session_id: str,
) -> bool:
    """Checks if the 'No Results Found' message is present on the page."""
    result = await crawler.arun(
        url=url,
        config=CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            session_id=session_id,
        ),
    )

    if result.success:
        if "No Results Found" in result.cleaned_html:
            return True
    return False

async def crawl_venues(
    base_url: str,
    css_selector: str,
    api_key: str,
    system_prompt: str,
    required_keys_str: str,
    progress_callback: Callable[[str], None],
    use_page_limit: bool = False,
    max_pages: int = None,
    llm_provider: str = "gemini",
    llm_model: str = "gemini-2.5-flash",
) -> List[Dict[str, Any]]:
    """
    Main function to crawl venue data with dynamic configuration.
    
    Args:
        base_url: The base URL to crawl
        css_selector: CSS selector for targeting venue elements
        api_key: API key for the LLM provider
        system_prompt: System prompt for the LLM
        required_keys_str: Comma-separated string of required data fields
        progress_callback: Function to call for progress updates
        use_page_limit: Whether to limit the number of pages crawled
        max_pages: Maximum number of pages to crawl (ignored if use_page_limit is False)
        llm_provider: LLM provider key (e.g., 'openai', 'gemini', 'deepseek')
        llm_model: LLM model key (e.g., 'gpt-4o', 'gemini-2.5-flash')
    
    Returns:
        List of extracted venue data dictionaries
    """
    # Initialize LLM provider manager
    provider_manager = LLMProviderManager()
    
    # Create the provider string for Crawl4AI
    try:
        provider_string = provider_manager.create_provider_string(llm_provider, llm_model)
        progress_callback(f"Using LLM: {provider_string}")
    except ValueError as e:
        progress_callback(f"Error with LLM configuration: {e}")
        return []
    
    # Convert the comma-separated string of keys into a clean list
    keys_list = [key.strip() for key in required_keys_str.split(',') if key.strip()]
    
    # Dynamically create a Pydantic model
    DynamicDataModel = create_model(
        'DynamicDataModel',
        **{key: (str | None, Field(default=None, description=f"Extracted {key}")) for key in keys_list}
    )

    # Initialize configurations
    browser_config = get_browser_config()
    llm_strategy = LLMExtractionStrategy(
        provider=provider_string,
        api_token=api_key,
        schema=DynamicDataModel.model_json_schema(),
        extraction_type="schema",
        instruction=system_prompt,
        input_format="markdown",
        verbose=True,
    )
    session_id = "dynamic_crawler_session"

    # Initialize state variables
    page_number = 1
    all_venues = []
    seen_ids = set()
    
    progress_callback("Starting the crawling process...")
    
    # Set page limit message
    if use_page_limit and max_pages:
        progress_callback(f"Page limit set: Will crawl maximum {max_pages} pages")
    else:
        progress_callback("No page limit: Will crawl until no more data is available")

    # Start the web crawler context
    async with AsyncWebCrawler(config=browser_config) as crawler:
        while True:
            # Check page limit
            if use_page_limit and max_pages and page_number > max_pages:
                progress_callback(f"Reached page limit ({max_pages} pages). Stopping crawl.")
                break
                
            url = f"{base_url}?page={page_number}"
            progress_callback(f"Processing page {page_number}...")

            # First, load the page without extraction to let dynamic content load
            initial_result = await crawler.arun(
                url=url,
                config=CrawlerRunConfig(
                    cache_mode=CacheMode.BYPASS,
                    session_id=session_id,
                ),
            )

            if not initial_result.success:
                progress_callback(f"Failed to load page {page_number}")
                break

            # Add a small delay to allow dynamic content to load
            await asyncio.sleep(5)

            # Now fetch with extraction strategy
            result = await crawler.arun(
                url=url,
                config=CrawlerRunConfig(
                    cache_mode=CacheMode.BYPASS,
                    extraction_strategy=llm_strategy,
                    css_selector=css_selector,
                    session_id=session_id,
                ),
            )

            if not (result.success and result.extracted_content):
                progress_callback(f"Error on page {page_number}: {result.error_message}")
                break

            # Parse extracted content
            try:
                extracted_data = json.loads(result.extracted_content)
            except json.JSONDecodeError:
                progress_callback(f"Failed to parse data from page {page_number}")
                break

            if not extracted_data:
                progress_callback(f"No venues found on page {page_number}")
                break

            # Process venues
            page_venues = []
            for venue in extracted_data:
                # Remove error field if it's False
                if venue.get("error") is False:
                    venue.pop("error", None)

                # Check for required fields
                if all(key in venue and venue[key] for key in keys_list):
                    # Use a composite key for deduplication
                    venue_id = str(venue)  # Simple hash of the entire venue dict
                    if venue_id not in seen_ids:
                        seen_ids.add(venue_id)
                        page_venues.append(venue)

            if page_venues:
                progress_callback(f"Extracted {len(page_venues)} venues from page {page_number}")
                all_venues.extend(page_venues)
            else:
                progress_callback(f"No valid venues found on page {page_number}")
                break

            page_number += 1
            await asyncio.sleep(2)  # Polite delay between requests

    progress_callback(f"Crawling complete! Total venues extracted: {len(all_venues)} from {page_number - 1} pages")
    return all_venues 