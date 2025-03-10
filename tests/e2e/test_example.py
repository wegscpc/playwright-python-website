"""End-to-end tests for website functionality."""
from typing import Dict, Any
import pytest
from playwright.sync_api import Page, expect
from config.test_config import get_base_url, get_timeout
from page_objects.base_page import base_page
from utils.test_helpers import wait_for_network_idle

@pytest.mark.browser_specific
def test_search_functionality(page: Page) -> None:
    """Test search functionality on the website.
    
    This test verifies the search feature works across different browsers:
    - Chromium (Chrome, Edge)
    - Firefox
    - WebKit (Safari)
    """
    # Initialize page object
    page_actions = base_page(page)
    
    # Navigate to homepage
    page.goto(get_base_url())
    wait_for_network_idle(page)
    
    # Test search input
    search_input = ".search-input"
    search_button = ".search-button"
    results_container = ".search-results"
    
    # Fill and submit search
    page_actions["fill_input"](search_input, "test query")
    page_actions["click_element"](search_button)
    
    # Wait for network idle after search
    wait_for_network_idle(page)
    
    # Verify results appear
    results = page.locator(results_container)
    expect(results).to_contain_text("Result")

@pytest.mark.browser_specific
def test_navigation_menu(page: Page) -> None:
    """Test main navigation menu functionality.
    
    This test verifies the menu functionality across different browsers:
    - Chromium (Chrome, Edge)
    - Firefox
    - WebKit (Safari)
    """
    page_actions = base_page(page)
    
    # Navigate to homepage
    page.goto(get_base_url())
    
    # Test menu interactions
    menu_button = ".menu-toggle"
    nav_menu = ".navigation-menu"
    menu_items = ".nav-item"
    
    # Open menu
    page_actions["click_element"](menu_button)
    expect(page.locator(nav_menu)).to_be_visible()
    
    # Verify menu items
    items = page.locator(menu_items).all()
    assert len(items) > 0, "Menu should contain navigation items"

@pytest.mark.browser_specific
def test_form_submission(page: Page) -> None:
    """Test contact form submission.
    
    This test verifies form submission works across different browsers:
    - Chromium (Chrome, Edge)
    - Firefox
    - WebKit (Safari)
    """
    page_actions = base_page(page)
    
    # Navigate to contact page
    page.goto(f"{get_base_url()}/contact")
    wait_for_network_idle(page)
    
    # Fill form fields
    form_fields: Dict[str, str] = {
        "name": ".name-input",
        "email": ".email-input",
        "message": ".message-input"
    }
    
    page_actions["fill_input"](form_fields["name"], "Test User")
    page_actions["fill_input"](form_fields["email"], "test@example.com")
    page_actions["fill_input"](form_fields["message"], "Test message")
    
    # Submit form
    submit_button = ".submit-button"
    success_message = ".success-message"
    
    # Click submit and wait for network idle
    page_actions["click_element"](submit_button)
    wait_for_network_idle(page)
    
    # Verify success message appears
    expect(page.locator(success_message)).to_be_visible(timeout=get_timeout())
