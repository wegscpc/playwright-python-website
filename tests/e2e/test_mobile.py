"""Mobile-specific end-to-end tests using Playwright."""
from typing import Dict, Any, Optional, Generator, Callable
import pytest
from playwright.sync_api import Page, expect, Browser, BrowserContext
from utils.test_helpers import wait_for_network_idle
from config.test_config import get_base_url, get_mobile_devices, get_timeout
from page_objects.base_page import base_page

def get_device_config(device_name: str) -> Dict[str, Any]:
    """Get device configuration for mobile testing.
    
    Args:
        device_name: Name of the device to get configuration for
        
    Returns:
        Device configuration dictionary
    """
    return get_mobile_devices()[device_name]

@pytest.fixture
def mobile_context(browser: Browser, request: pytest.FixtureRequest) -> Generator[BrowserContext, None, None]:
    """Create a mobile browser context with specified device emulation.

    Args:
        browser: Playwright browser instance
        request: Pytest request object containing device name
    """
    device_config = get_device_config(request.param)
    context = browser.new_context(**device_config)
    try:
        yield context
    finally:
        context.close()

@pytest.fixture
def mobile_page(mobile_context: BrowserContext) -> Generator[Page, None, None]:
    """Create a page in the mobile context.
    
    Args:
        mobile_context: Mobile browser context with device emulation
    """
    page = mobile_context.new_page()
    try:
        yield page
    finally:
        page.close()

def verify_menu_state(page: Page, is_visible: bool) -> None:
    """Verify mobile menu state.
    
    Args:
        page: Playwright page object
        is_visible: Expected visibility state
    """
    nav_menu = page.locator(".navigation-menu")
    menu_toggle = page.locator(".menu-toggle")
    
    # Check menu visibility class and attributes
    expect(menu_toggle).to_have_attribute("aria-expanded", str(is_visible).lower())
    expect(nav_menu).to_have_attribute("aria-hidden", str(not is_visible).lower())
    
    if is_visible:
        expect(nav_menu).to_have_class("navigation-menu navigation-menu--visible")
    else:
        expect(nav_menu).not_to_have_class("navigation-menu--visible")

@pytest.mark.skip(reason="Menu state verification is unstable due to initialization timing")
@pytest.mark.browser_specific
@pytest.mark.parametrize("mobile_context", get_mobile_devices().keys(), indirect=True)
def test_mobile_navigation(mobile_page: Page) -> None:
    """Test mobile navigation menu functionality."""
    page_actions = base_page(mobile_page)
    
    # Navigate to homepage and wait for load
    mobile_page.goto(get_base_url())
    wait_for_network_idle(mobile_page)
    
    # Test menu interactions
    menu_button = ".menu-toggle"
    nav_menu = ".navigation-menu"
    
    # Initial state - menu should be hidden on mobile
    verify_menu_state(mobile_page, False)
    
    # Open menu and verify
    page_actions["click_element"](menu_button)
    verify_menu_state(mobile_page, True)
    
    # Verify all nav items are present
    nav_items = mobile_page.locator(".nav-item").all()
    assert len(nav_items) == 4, "Navigation menu should contain 4 items"
    
    # Close menu by clicking outside
    page_actions["click_element"](".main")
    verify_menu_state(mobile_page, False)

@pytest.mark.browser_specific
@pytest.mark.parametrize("mobile_context", get_mobile_devices().keys(), indirect=True)
def test_mobile_search(mobile_page: Page) -> None:
    """Test search functionality on mobile devices.
    
    This test verifies search works across different devices:
    - iPhone 12
    - Pixel 5
    - iPad Pro
    """
    page_actions = base_page(mobile_page)
    
    # Navigate to homepage
    mobile_page.goto(get_base_url())
    wait_for_network_idle(mobile_page)
    
    # Test search input
    search_input = ".search-input"
    search_button = ".search-button"
    results_container = ".search-results"
    
    # Fill and submit search
    page_actions["fill_input"](search_input, "mobile test")
    page_actions["click_element"](search_button)
    
    # Wait for network idle after search
    wait_for_network_idle(mobile_page)
    
    # Verify results appear
    results = mobile_page.locator(results_container)
    expect(results).to_contain_text("Result")

@pytest.mark.browser_specific
@pytest.mark.parametrize("mobile_context", get_mobile_devices().keys(), indirect=True)
def test_mobile_form(mobile_page: Page) -> None:
    """Test form submission on mobile devices.
    
    This test verifies forms work across different devices:
    - iPhone 12
    - Pixel 5
    - iPad Pro
    """
    page_actions = base_page(mobile_page)
    
    # Navigate to contact page
    mobile_page.goto(f"{get_base_url()}/contact")
    wait_for_network_idle(mobile_page)
    
    # Fill form fields
    form_fields: Dict[str, str] = {
        "name": ".name-input",
        "email": ".email-input",
        "message": ".message-input"
    }
    
    page_actions["fill_input"](form_fields["name"], "Mobile User")
    page_actions["fill_input"](form_fields["email"], "mobile@example.com")
    page_actions["fill_input"](form_fields["message"], "Test from mobile")
    
    # Submit form
    submit_button = ".submit-button"
    success_message = ".success-message"
    
    # Click submit and wait for network idle
    page_actions["click_element"](submit_button)
    wait_for_network_idle(mobile_page)
    
    # Verify success message appears
    expect(mobile_page.locator(success_message)).to_be_visible(timeout=get_timeout())
