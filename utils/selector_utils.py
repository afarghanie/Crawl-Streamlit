import re
import litellm

# A list of common, non-descriptive words to ignore. This helps focus
# on the meaningful parts of a class name.
STOPWORDS = {
    'wrapper', 'container', 'main', 'active', 'button', 'btn', 'icon', 'image',
    'img', 'media', 'content', 'holder', 'inner', 'outer', 'slide', 'shadow',
    'light', 'dark', 'style', 'layout', 'grid', 'row', 'col', 'link', 'nav',
    'filter', 'used', 'splide', 'cell'  # Added 'cell' to fix previous issue
}

# A dictionary to suggest common alternative patterns.
# The keys are now treated as "primary" keywords that trigger a synonym-based override.
KEYWORD_SYNONYMS = {
    'listing': ['ListingCell', 'PropertyCard', 'listing-item'],
    'product': ['item', 'product-card', 'prd'],
    'search': ['result-item', 'search-result'],
    'card': ['panel', 'tile', 'card-container']
}

SYSTEM_PROMPT = """You are a CSS selector optimization expert. I'll show you examples of how to convert rigid CSS selectors into flexible, robust versions.

**Example 1:**
Original: [class^='ListingCellItem_cellItemWrapper__t2hO2']
Flexible: [class*='ListingCell'], [class*='PropertyCard'], [class*='listing-item']
Reasoning: Used partial class names and multiple fallbacks for different website patterns

**Example 2:**
Original: [class^='product-item-container-wrapper']
Flexible: [class*='product'], [class*='item'], [class*='container']
Reasoning: Broke down into key semantic parts and used contains operator

**Example 3:**
Original: [class^='search-result-card-main']
Flexible: [class*='card'], [class*='result'], [class*='search']
Reasoning: Extracted meaningful keywords and provided multiple matching options
"""

def _split_into_keywords(class_str: str) -> list[str]:
    """Splits a class string by delimiters and CamelCase."""
    # First, split by standard delimiters
    parts = re.split(r'__|_|-|\s', class_str)
    keywords = []
    for part in parts:
        if not part:
            continue
        # Then, split CamelCase and extend the list
        # e.g., "ListingCellItem" -> ["Listing", "Cell", "Item"]
        camel_case_split = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', part)
        keywords.extend(camel_case_split)
    return keywords

def _get_user_prompt(raw_selector: str) -> str:
    """Creates the user-facing prompt for the AI."""
    return f"""Now convert this selector: {raw_selector}

Requirements:
1. Use `*=` operator for flexibility.
2. Include 3-5 alternative selectors.
3. Focus on the most important class patterns.
4. You MUST ONLY return the flexible CSS selector string and nothing else. Do not add any explanation, reasoning, or markdown formatting. Just the selector string.
"""

def generate_flexible_selector_with_ai(
    raw_selector: str,
    api_key: str,
    llm_provider: str,
    llm_model: str,
) -> str:
    """
    Converts a raw, specific CSS selector into a more flexible one using an AI call,
    guided by an expert-level system prompt.

    Args:
        raw_selector: The raw CSS selector string from the user.
        api_key: The API key for the selected LLM provider.
        llm_provider: The name of the LLM provider (e.g., 'openai').
        llm_model: The specific model to use (e.g., 'gpt-4o').

    Returns:
        The AI-generated flexible selector string, or an error message.
    """
    if not all([raw_selector, api_key, llm_provider, llm_model]):
        return raw_selector

    try:
        model_string = f"{llm_provider}/{llm_model}"
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": _get_user_prompt(raw_selector)}
        ]
        
        response = litellm.completion(
            model=model_string,
            messages=messages,
            api_key=api_key,
            temperature=0.1,  # Lower temperature for more deterministic, factual output
        )
        
        ai_response = response.choices[0].message.content.strip()
        # Clean up potential markdown code blocks or other unwanted text from the AI
        return ai_response.replace("`", "").replace("css", "").strip()

    except Exception as e:
        print(f"Error generating flexible selector with AI: {e}")
        return f"Error: Could not generate selector. Please check API key and provider settings."

def generate_flexible_selector(raw_selector: str) -> str:
    """
    Converts a raw, specific CSS selector into a more flexible, rule-based selector
    based on expert-defined patterns, without using an AI API call.

    This function mimics an expert's reasoning with a two-tiered approach:
    1.  It first extracts all class names from the selector string.
    2.  For each class name, it breaks it into granular keywords (handling CamelCase, hyphens, etc.).
    3.  It checks if any keyword is a "primary" keyword (a key in `KEYWORD_SYNONYMS`).
    4.  **Expert Override**: If a primary keyword is found, it prioritizes the predefined
        synonyms for that keyword, assuming it's a known, important pattern.
    5.  **Fallback Deconstruction**: If no primary keyword is found, it falls back to a
        general deconstruction, taking all meaningful, non-stopword keywords.
    """
    if not raw_selector or not raw_selector.strip():
        return ""

    class_strings = set()
    simple_classes = re.findall(r'\.([a-zA-Z0-9_-]+)', raw_selector)
    class_strings.update(simple_classes)
    attr_classes = re.findall(r'\[class\s*.*?=\s*[\'"](.*?)[\'"]\]', raw_selector)
    for class_group in attr_classes:
        class_strings.update(class_group.split())

    if not class_strings:
        return raw_selector

    final_selectors = set()
    primary_synonyms_found = set()

    all_keywords_raw = []
    for s in class_strings:
        all_keywords_raw.extend(_split_into_keywords(s))
    
    # First pass: check for primary synonym triggers
    for keyword in all_keywords_raw:
        if keyword.lower() in KEYWORD_SYNONYMS:
            primary_synonyms_found.update(KEYWORD_SYNONYMS[keyword.lower()])
            
    # If we found expert synonyms, we prioritize them
    if primary_synonyms_found:
        final_selectors = primary_synonyms_found
    else:
        # Fallback: deconstruct and use all meaningful keywords
        for keyword in all_keywords_raw:
            kw_lower = keyword.lower()
            if kw_lower in STOPWORDS or not keyword.isalpha() or len(kw_lower) < 4:
                continue
            final_selectors.add(keyword)

    if not final_selectors:
         return raw_selector # Safety fallback

    return ", ".join(sorted([f"[class*='{kw}']" for kw in final_selectors])) 