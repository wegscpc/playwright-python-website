from typing import Optional, Dict, Any, Callable
from playwright.sync_api import Page, Locator

def base_page(page: Page) -> Dict[str, Callable]:
    """Base page object with common functionality."""
    
    def wait_for_element(selector: str, timeout: Optional[float] = None) -> Locator:
        """Wait for element to be visible."""
        element = page.locator(selector)
        element.wait_for(timeout=timeout)
        return element
    
    def get_element_text(selector: str) -> str:
        """Get text content of element."""
        element = page.locator(selector)
        return element.text_content() or ""
    
    def click_element(selector: str) -> None:
        """Click element with retry logic."""
        try:
            element = page.locator(selector)
            element.click()
        except Exception as e:
            # Retry with force if initial click fails
            element.click(force=True)
            
    def fill_input(selector: str, value: str) -> None:
        """Fill input field with value."""
        element = page.locator(selector)
        element.fill(value)
        
    def is_element_visible(selector: str) -> bool:
        """Check if element is visible."""
        element = page.locator(selector)
        return element.is_visible()
    
    return {
        "wait_for_element": wait_for_element,
        "get_element_text": get_element_text,
        "click_element": click_element,
        "fill_input": fill_input,
        "is_element_visible": is_element_visible
    }
