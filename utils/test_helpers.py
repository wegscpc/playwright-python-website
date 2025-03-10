from typing import Any, Dict, Optional
from playwright.sync_api import Page, Response
import json
import time

def wait_for_network_idle(page: Page, timeout: int = 5000):
    """Wait for network to be idle."""
    return page.wait_for_load_state("networkidle", timeout=timeout)

def intercept_request(page: Page, url_pattern: str) -> Dict[str, Any]:
    """Intercept and return network request data."""
    data = {}
    
    def handle_response(response: Response):
        if response.ok:
            data["response"] = response.json()
    
    page.on("response", handle_response)
    return data

def take_screenshot(page: Page, name: str, full_page: bool = True):
    """Take screenshot with timestamp."""
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"screenshots/{name}_{timestamp}.png"
    page.screenshot(path=filename, full_page=full_page)
    return filename

def load_test_data(file_path: str) -> Dict[str, Any]:
    """Load test data from JSON file."""
    with open(file_path, "r") as f:
        return json.load(f)

def retry_on_failure(func: callable, max_attempts: int = 3, delay: float = 1.0):
    """Retry function on failure with exponential backoff."""
    def wrapper(*args, **kwargs):
        last_exception = None
        for attempt in range(max_attempts):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt < max_attempts - 1:
                    time.sleep(delay * (2 ** attempt))
        raise last_exception
    return wrapper
