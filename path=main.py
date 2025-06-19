import asyncio
import json
import os
from crawl4ai.crawler import Crawl4AI

# Assuming config.py and models/venue.py exist
from config import BASE_URL, CSS_SELECTOR, REQUIRED_KEYS
from models.venue import Venue
from utils.scraper_utils import fetch_and_process_page # Assuming this function exists and is used

# Set your LLM Provider environment variable before running
# os.environ["LLM_PROVIDER"] = "google" # Example for Google
# os.environ["LLM_MODEL"] = "models/gemini-1.5-flash-latest" # Example Google model

async def crawl_venues():
    """
    Main asynchronous function to crawl venues using Crawl4AI.
    """
    # Initialize Crawl4AI (assuming default settings are okay or configured elsewhere)
    # You might need to pass LLM settings here depending on crawl4ai config
    crawler = Crawl4AI()

    # Keep track of seen venue names to avoid duplicates
    seen_names = set()
    all_extracted_venues = []

    # --- Pagination Logic Starts Here ---
    page_number = 1
    max_pages_to_crawl = 5 # Example: Limit to the first 5 pages

    while page_number <= max_pages_to_crawl:
        # Construct the URL for the current page
        # This assumes the pagination uses a '?page=X' query parameter
        # You might need to adjust this based on the actual website's URL structure
        page_url = f"{BASE_URL.split('?')[0]}?page={page_number}"

        print(f"Loading page {page_number}...")

        # Fetch and process the current page
        # Pass the seen_names set to the processing function
        # The function should return processed venues and a boolean indicating if more results are likely
        extracted_venues_on_page, no_more_results = await fetch_and_process_page(
            page_url,
            CSS_SELECTOR,
            REQUIRED_KEYS,
            seen_names, # Pass the set to the processing function
            page_number=page_number # Pass the page number for logging/debugging
        )

        # Add the venues found on this page to the overall list
        all_extracted_venues.extend(extracted_venues_on_page)

        # If the processing function indicates no more results were found on this page, stop
        # This is a common way to handle the end of pagination
        if no_more_results:
             print(f"No new venues extracted on page {page_number}. Stopping pagination.")
             break

        # Move to the next page
        page_number += 1

    # --- Pagination Logic Ends Here ---

    print(f"\nTotal unique venues extracted: {len(all_extracted_venues)}")

    # You can now work with the 'all_extracted_venues' list,
    # which contains Pydantic Venue objects.

    # Example: Convert to list of dictionaries and save to CSV
    if all_extracted_venues:
        # Convert Pydantic models to dictionaries
        venue_data_for_csv = [venue.model_dump() for venue in all_extracted_venues] # Use model_dump() or dict()

        # --- CSV Saving Logic ---
        csv_filename = "complete_venues.csv"
        import csv

        # Determine fieldnames from the keys of the first dictionary
        # Ensure 'agent_name' and 'error' are handled if present in the original extraction but not in Venue model
        # We'll use the keys from the Venue model's fields for clean CSV columns
        csv_fieldnames = list(Venue.model_fields.keys())

        try:
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_fieldnames)
                writer.writeheader()
                for venue_dict in venue_data_for_csv:
                     # Filter the dictionary to only include keys present in csv_fieldnames
                     # This prevents extra keys like 'error' from appearing in the CSV if not in the model
                     filtered_venue_dict = {k: v for k, v in venue_dict.items() if k in csv_fieldnames}
                     writer.writerow(filtered_venue_dict)


            print(f"Successfully wrote data to {csv_filename}")

        except Exception as e:
            print(f"An error occurred while writing CSV: {e}")
        # --- End CSV Saving Logic ---

    else:
        print("No venues extracted to save to CSV.")


async def main():
    await crawl_venues()

if __name__ == "__main__":
    asyncio.run(main()) 