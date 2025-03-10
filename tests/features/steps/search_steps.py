"""
Step definitions for search functionality following BDD patterns.
Type-safe implementation with proper error handling.
"""
from typing import Dict, Any, Callable
import pytest
from pytest_bdd import given, when, then, parsers
from playwright.sync_api import Page, expect, Error as PlaywrightError
import logging

# Configure logging with descriptive format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s (%(filename)s:%(lineno)d)'
)
logger = logging.getLogger(__name__)

# Constants
BASE_URL = "https://www.google.com"
DEFAULT_TIMEOUT = 60000  # Increased timeout for network issues
DEFAULT_EXPECT_TIMEOUT = 30000  # Increased timeout for expect operations
RETRY_COUNT = 3  # Number of retries for network operations

def wait_for_element(page: Page, selector: str, timeout: int = DEFAULT_TIMEOUT) -> None:
    """Wait for element to be visible and stable."""
    try:
        # Wait for network to be idle first
        page.wait_for_load_state("networkidle", timeout=timeout)
        page.wait_for_load_state("domcontentloaded", timeout=timeout)
        
        # Now wait for the element
        page.wait_for_selector(selector, state="visible", timeout=timeout)
    except PlaywrightError as e:
        logger.error(f"Failed to wait for element {selector}: {str(e)}")
        raise

def handle_consent_dialog(page: Page) -> None:
    """Handle Google's consent dialog if present."""
    try:
        consent_selectors = [
            'button:has-text("Accept all")',
            'button:has-text("Aceptar todo")',
            'button:has-text("I agree")',
            'button:has-text("Acepto")',
            'div[role="dialog"] button:has-text("Accept")',
            'div[role="dialog"] button:has-text("Aceptar")'
        ]
        
        for selector in consent_selectors:
            try:
                if page.locator(selector).is_visible(timeout=5000):  # Quick check
                    page.locator(selector).click()
                    logger.info(f"Clicked consent button with selector: {selector}")
                    wait_for_element(page, 'input[name="q"]')
                    return
            except PlaywrightError:
                continue
                
        logger.info("No consent dialog found or already accepted")
    except PlaywrightError as e:
        logger.warning(f"Consent dialog handling failed: {str(e)}")

@given("I am on the search page", target_fixture="search_page")
def visit_search_page(page: Page) -> Page:
    """Navigate to the search page and handle initial dialogs."""
    try:
        # Configure page timeouts
        page.set_default_timeout(DEFAULT_TIMEOUT)
        page.set_default_navigation_timeout(DEFAULT_TIMEOUT)
        
        # Retry navigation with exponential backoff
        for attempt in range(RETRY_COUNT):
            try:
                # Navigate and wait for initial load
                logger.info(f"Attempt {attempt + 1} to navigate to {BASE_URL}")
                page.goto(BASE_URL, wait_until="networkidle")
                
                # Wait for key elements
                wait_for_element(page, 'input[name="q"]')
                
                # Handle consent dialog that might block interaction
                handle_consent_dialog(page)
                
                # Verify page is ready
                expect(page).to_have_title("Google", timeout=DEFAULT_EXPECT_TIMEOUT)
                logger.info("Successfully navigated to search page")
                return page
            except PlaywrightError as e:
                if attempt == RETRY_COUNT - 1:
                    logger.error(f"Failed to visit search page after {RETRY_COUNT} attempts: {str(e)}")
                    raise
                logger.warning(f"Attempt {attempt + 1} failed, retrying...")
                page.wait_for_timeout(1000 * (2 ** attempt))  # Exponential backoff
    except Exception as e:
        logger.error(f"Failed to visit search page: {str(e)}")
        raise

@when(parsers.parse('I enter "{text}" in the search box'))
def enter_search_text(search_page: Page, text: str) -> None:
    """Enter text in the search box and wait for suggestions."""
    try:
        search_input = search_page.locator('input[name="q"]')
        search_input.click()  # Ensure focus
        search_input.fill(text)
        search_input.press("Tab")  # Trigger suggestions
        wait_for_element(search_page, 'input[name="btnK"]')
        logger.info(f"Successfully entered search text: {text}")
    except PlaywrightError as e:
        logger.error(f"Failed to enter search text: {str(e)}")
        raise

@when("I click the search button")
def click_search_button(search_page: Page) -> None:
    """Click the search button and wait for results."""
    try:
        # Use more reliable button selector
        search_button = search_page.locator('input[name="btnK"], button[name="btnK"]').first
        search_button.wait_for(state="visible", timeout=DEFAULT_TIMEOUT)
        search_button.click()
        
        # Wait for search results
        wait_for_element(search_page, "#search", timeout=DEFAULT_TIMEOUT)
        logger.info("Successfully clicked search button")
    except PlaywrightError as e:
        logger.error(f"Failed to click search button: {str(e)}")
        raise

@then("I should see search results")
def verify_search_results(search_page: Page) -> None:
    """Verify search results are displayed."""
    try:
        expect(search_page.locator("#search")).to_be_visible(timeout=DEFAULT_EXPECT_TIMEOUT)
        logger.info("Successfully verified search results are visible")
    except PlaywrightError as e:
        logger.error(f"Failed to verify search results: {str(e)}")
        raise

@then(parsers.parse('the first result should contain "{text}"'))
def verify_first_result(search_page: Page, text: str) -> None:
    """Verify first result contains expected text."""
    try:
        first_result = search_page.locator("#search").get_by_role("heading").first
        expect(first_result).to_contain_text(text, ignore_case=True, timeout=DEFAULT_EXPECT_TIMEOUT)
        logger.info(f"Successfully verified first result contains: {text}")
    except PlaywrightError as e:
        logger.error(f"Failed to verify first result: {str(e)}")
        raise

@then(parsers.parse('the page title should contain "{text}"'))
def verify_page_title(search_page: Page, text: str) -> None:
    """Verify page title contains expected text."""
    try:
        expect(search_page).to_have_title(text, timeout=DEFAULT_EXPECT_TIMEOUT)
        logger.info(f"Successfully verified page title contains: {text}")
    except PlaywrightError as e:
        logger.error(f"Failed to verify page title: {str(e)}")
        raise
