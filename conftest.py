"""
Configuration and fixtures for BDD tests.
Type-safe implementation with proper error handling.
"""
import os
import logging
import pytest
from typing import Dict, Any, Generator
from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    sync_playwright
)

# Configure logging with descriptive format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s (%(filename)s:%(lineno)d)'
)
logger = logging.getLogger(__name__)

# Browser configuration
BROWSER_TYPE = "chromium"
BROWSER_CONFIG = {
    "headless": True,
    "slow_mo": 50,
}

@pytest.fixture(scope="session")
def browser_context_args() -> Dict[str, Any]:
    """Configure browser context."""
    return {
        "viewport": {
            "width": 1920,
            "height": 1080
        },
        "ignore_https_errors": True,
        "java_script_enabled": True
    }

@pytest.fixture(scope="session")
def playwright() -> Generator[Playwright, None, None]:
    """Create Playwright instance."""
    with sync_playwright() as playwright:
        yield playwright

@pytest.fixture(scope="session")
def browser(playwright: Playwright) -> Generator[Browser, None, None]:
    """Create browser instance."""
    browser = playwright[BROWSER_TYPE].launch(**BROWSER_CONFIG)
    yield browser
    browser.close()

@pytest.fixture
def context(browser: Browser, browser_context_args: Dict[str, Any]) -> Generator[BrowserContext, None, None]:
    """Create browser context."""
    context = browser.new_context(**browser_context_args)
    yield context
    context.close()

@pytest.fixture
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """Create page instance."""
    page = context.new_page()
    yield page
    page.close()

# Import step definitions
from tests.features.steps.search_steps import (  # noqa: E402
    visit_search_page,
    enter_search_text,
    click_search_button,
    verify_search_results,
    verify_first_result,
    verify_page_title
)
