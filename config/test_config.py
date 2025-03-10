"""Test configuration module."""
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_base_url() -> str:
    """Get base URL for tests."""
    return os.getenv('BASE_URL', 'http://localhost:5000')

def get_timeout() -> int:
    """Get timeout value for tests."""
    return int(os.getenv('TIMEOUT', '30000'))

def get_viewport_size() -> Dict[str, int]:
    """Get viewport size for tests."""
    return {
        'width': int(os.getenv('VIEWPORT_WIDTH', '1280')),
        'height': int(os.getenv('VIEWPORT_HEIGHT', '720'))
    }

def get_mobile_devices() -> Dict[str, Dict[str, Any]]:
    """Get mobile device configurations for testing."""
    return {
        'iPhone_12': {
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
            'viewport': {'width': 390, 'height': 844},
            'device_scale_factor': 3,
            'is_mobile': True,
            'has_touch': True
        },
        'Pixel_5': {
            'user_agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36',
            'viewport': {'width': 393, 'height': 851},
            'device_scale_factor': 2.75,
            'is_mobile': True,
            'has_touch': True
        },
        'iPad_Pro': {
            'user_agent': 'Mozilla/5.0 (iPad; CPU OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
            'viewport': {'width': 1024, 'height': 1366},
            'device_scale_factor': 2,
            'is_mobile': True,
            'has_touch': True
        }
    }

def get_browser_config() -> Dict[str, Any]:
    """Get browser configuration."""
    return {
        'headless': os.getenv('HEADLESS', 'false').lower() == 'true',
        'slow_mo': int(os.getenv('SLOW_MO', '0'))
    }
