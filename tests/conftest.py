"""Pytest configuration and fixtures."""

import sys
from unittest.mock import MagicMock

# Mock heavy dependencies before importing any test modules
sys.modules['torch'] = MagicMock()
sys.modules['torchvision'] = MagicMock()
sys.modules['transformers'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.Image'] = MagicMock()

# Mock pydantic_settings if not installed
try:
    import pydantic_settings  # noqa: F401
except ImportError:
    sys.modules['pydantic_settings'] = MagicMock()
