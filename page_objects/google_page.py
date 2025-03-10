from typing import Dict, Any, Callable
from playwright.sync_api import Page, expect, TimeoutError
import time
import random

def get_google_page_actions(page: Page) -> Dict[str, Callable]:
    """
    Returns a dictionary of actions that can be performed on the Google search page.
    
    Args:
        page: Page object
        
    Returns:
        Dict of action functions for Google page interactions
    """
    
    def add_human_delay() -> None:
        """Adds a small random delay to simulate human behavior."""
        time.sleep(random.uniform(0.5, 1.5))

    def is_captcha_present() -> bool:
        """Checks if we're on a CAPTCHA page."""
        try:
            return any([
                "sorry/index" in page.url,
                page.get_by_text("Our systems have detected unusual traffic").is_visible(timeout=1000),
                page.get_by_text("Nuestros sistemas han detectado tráfico inusual").is_visible(timeout=1000),
                # More reliable CAPTCHA detection that handles multiple iframes
                page.locator("iframe[title*='reCAPTCHA']").count() > 0
            ])
        except Exception:
            # If any check fails, assume no CAPTCHA to avoid false positives
            return False
    
    def handle_consent_dialog() -> None:
        """Handles the initial Google consent dialog."""
        try:
            # Wait for any dialog to appear with random delay
            add_human_delay()
            
            # Try direct button click first (most common case)
            for text in ["Aceptar todo", "Accept all", "Rechazar todo", "Reject all"]:
                try:
                    button = page.get_by_role("button", name=text, exact=True)
                    if button.is_visible(timeout=1000):
                        # Move mouse to button naturally
                        button.hover()
                        add_human_delay()
                        button.click()
                        page.wait_for_load_state("networkidle", timeout=5000)
                        return
                except:
                    continue
            
            # If direct button didn't work, try iframe
            iframe = page.frame_locator('iframe[src*="consent.google.com"]').first
            if iframe:
                for text in ["Aceptar todo", "Accept all", "Rechazar todo", "Reject all"]:
                    try:
                        button = iframe.get_by_role("button", name=text, exact=True)
                        if button.is_visible(timeout=1000):
                            # Move mouse to button naturally
                            button.hover()
                            add_human_delay()
                            button.click()
                            page.wait_for_load_state("networkidle", timeout=5000)
                            return
                    except:
                        continue
                        
        except TimeoutError:
            # If we timeout, the dialog might not be present, which is fine
            pass
        except Exception as e:
            # Log error but don't fail - dialog might not be present
            print(f"Warning: Failed to handle consent dialog: {str(e)}")

    def perform_search(search_term: str) -> None:
        """Performs a search on Google and waits for results."""
        try:
            # Handle consent dialog first
            handle_consent_dialog()
            
            # Check for CAPTCHA before proceeding
            if is_captcha_present():
                raise Exception("CAPTCHA detected before search - manual intervention needed")
            
            # Enter search term and submit
            search_input = page.locator('textarea[name="q"]')
            search_input.wait_for(state="visible", timeout=5000)
            
            # Move mouse to search box naturally
            search_input.hover()
            add_human_delay()
            search_input.click()
            
            # Type search term with human-like delays
            for char in search_term:
                search_input.type(char, delay=random.uniform(50, 150))
                time.sleep(random.uniform(0.1, 0.3))
            
            # Add natural delay before pressing Enter
            add_human_delay()
            search_input.press("Enter")
            
            # Wait for navigation and check for CAPTCHA
            page.wait_for_load_state("networkidle", timeout=10000)
            
            # Check for CAPTCHA after search
            if is_captcha_present():
                raise Exception("CAPTCHA detected after search - manual intervention needed")
            
            # Wait for search results
            page.wait_for_selector('xpath=//div[@id="search"] | //div[@id="main"] | //div[@id="rso"]', timeout=10000)
            
        except Exception as e:
            raise Exception(f"Failed to perform Google search: {str(e)}")
    
    def get_search_results() -> list[str]:
        """Returns list of search result titles."""
        try:
            # More reliable selector that works across different Google versions
            results = page.query_selector_all('xpath=//h3[contains(@class, "r") or contains(@class, "LC20lb") or @role="heading"]')
            return [result.inner_text() for result in results if result.inner_text()]
        except Exception as e:
            raise Exception(f"Failed to get search results: {str(e)}")
    
    return {
        "perform_search": perform_search,
        "get_search_results": get_search_results,
        "handle_consent_dialog": handle_consent_dialog,
        "is_captcha_present": is_captcha_present
    }
