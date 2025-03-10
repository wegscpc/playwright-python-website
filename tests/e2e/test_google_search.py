import pytest
import time
import random
import os
from typing import Dict, Any, Callable, Generator
from playwright.sync_api import Page, expect, BrowserContext

from page_objects.google_page import get_google_page_actions

@pytest.fixture(scope="function")
def browser_context(context: BrowserContext) -> None:
    """
    Sets up browser context with stealth settings.
    """
    # Set permissions to appear more natural
    context.grant_permissions(['geolocation'])
    
    # Add common headers
    context.set_extra_http_headers({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="122", "Chromium";v="122"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"'
    })

@pytest.fixture(scope="function")
def search_delay() -> Generator[None, None, None]:
    """
    Adds delay between test runs to avoid triggering automated testing detection.
    """
    yield
    # Random delay between 3-5 seconds between tests
    time.sleep(random.uniform(3, 5))

def test_google_search_components(page: Page, browser_context: None, search_delay: None) -> None:
    """
    Component-level test for Google search functionality.
    Tests individual components with proper delays to avoid CAPTCHA.
    
    Args:
        page: Page object
        browser_context: Fixture that sets up stealth browser settings
        search_delay: Fixture that adds delay between tests
    """
    # Configure viewport for more human-like appearance
    page.set_viewport_size({
        "width": random.randint(1024, 1920),
        "height": random.randint(768, 1080)
    })
    
    # Test 1: Page Load and Initial State
    page.goto("https://www.google.com", wait_until="networkidle")
    google_actions = get_google_page_actions(page)
    
    # Check for CAPTCHA before proceeding
    if google_actions["is_captcha_present"]():
        pytest.skip("CAPTCHA detected on initial load - manual intervention needed")
    
    # Test 2: Search Execution
    search_term = "playwright python automation"
    try:
        google_actions["perform_search"](search_term)
        
        # Test 3: Results Verification
        results = google_actions["get_search_results"]()
        assert len(results) > 0, "No search results found"
        
        # Verify relevance of results
        relevant_terms = ["playwright", "python", "automation"]
        has_relevant_result = any(
            all(term.lower() in result.lower() for term in relevant_terms)
            for result in results[:5]
        )
        assert has_relevant_result, f"No relevant results found for: {search_term}"
        
    except Exception as e:
        if "CAPTCHA detected" in str(e):
            # Save current page state for debugging
            page.screenshot(path="debug/captcha_screenshot.png")
            pytest.skip(f"CAPTCHA detected: {str(e)}")
        else:
            raise e
