"""
Test scenarios for search functionality following BDD patterns.
Type-safe implementation with proper error handling.
"""
import os
from pathlib import Path
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page, expect

# Import step definitions
from tests.features.steps.search_steps import (
    wait_for_element,
    handle_consent_dialog,
    visit_search_page,
    enter_search_text,
    click_search_button,
    verify_search_results,
    verify_first_result,
    verify_page_title
)

# Register scenarios from feature files
FEATURE_DIR = Path(__file__).parent
scenarios(str(FEATURE_DIR / 'search.feature'))

# Re-register step definitions for pytest-bdd
@given("I am on the search page", target_fixture="search_page")
def test_visit_search_page(page: Page) -> Page:
    """Navigate to the search page."""
    return visit_search_page(page)

@when(parsers.cfparse('I enter "{text}" in the search box'))
def test_enter_search_text(search_page: Page, text: str) -> None:
    """Enter text in the search box."""
    enter_search_text(search_page, text)

@when("I click the search button")
def test_click_search_button(search_page: Page) -> None:
    """Click the search button."""
    click_search_button(search_page)

@then("I should see search results")
def test_verify_search_results(search_page: Page) -> None:
    """Verify search results are displayed."""
    verify_search_results(search_page)

@then(parsers.cfparse('the first result should contain "{text}"'))
def test_verify_first_result(search_page: Page, text: str) -> None:
    """Verify first result contains expected text."""
    verify_first_result(search_page, text)

@then(parsers.cfparse('the page title should contain "{text}"'))
def test_verify_page_title(search_page: Page, text: str) -> None:
    """Verify page title contains expected text."""
    verify_page_title(search_page, text)
