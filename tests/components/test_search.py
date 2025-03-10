import pytest
import os
from typing import Generator
from playwright.sync_api import Page, expect

@pytest.fixture(scope="function")
def mock_page(page: Page) -> Generator[Page, None, None]:
    """
    Fixture that loads our mock search page.
    """
    # Get absolute path to mock file
    mock_path = os.path.join(
        os.path.dirname(__file__),
        "mock_google.html"
    )
    page.goto(f"file://{mock_path}")
    yield page

def test_search_functionality(mock_page: Page) -> None:
    """
    Tests the search functionality using our mock page.
    This avoids issues with Google's CAPTCHA while still testing core functionality.
    """
    # Test search input
    search_input = mock_page.locator(".search-input")
    expect(search_input).to_be_visible()
    
    # Enter search term
    search_term = "playwright python automation"
    search_input.fill(search_term)
    
    # Submit search
    search_input.press("Enter")
    
    # Verify results appear
    results = mock_page.locator(".result-item")
    expect(results).to_have_count(3)  # We expect 3 mock results
    
    # Verify result content
    first_result = results.first
    expect(first_result.locator(".result-title")).to_contain_text("Playwright")
    expect(first_result.locator(".result-url")).to_contain_text("playwright.dev")

def test_search_no_results(mock_page: Page) -> None:
    """Tests the no results case."""
    search_input = mock_page.locator(".search-input")
    
    # Search for something not in our mock data
    search_input.fill("nonexistent search")
    search_input.press("Enter")
    
    # Verify no results message
    results = mock_page.locator(".result-item")
    expect(results).to_have_count(1)
    expect(results.locator(".result-title")).to_contain_text("No results found")
