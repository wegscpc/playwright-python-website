"""
Configuration and fixtures for BDD tests.
Type-safe implementation with proper error handling.
"""
from typing import Dict, Any, Generator
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

@pytest.fixture(scope="session")
def browser_context_args() -> Dict[str, Any]:
    """Configure browser context arguments."""
    return {
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        "locale": "en-US"
    }

@pytest.fixture(scope="session")
def browser() -> Generator[Browser, None, None]:
    """Create a browser instance for the test session."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture
def context(browser: Browser, browser_context_args: Dict[str, Any]) -> Generator[BrowserContext, None, None]:
    """Create a fresh browser context for each test."""
    context = browser.new_context(**browser_context_args)
    yield context
    context.close()

@pytest.fixture
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """Create a fresh page for each test."""
    page = context.new_page()
    yield page
    page.close()
