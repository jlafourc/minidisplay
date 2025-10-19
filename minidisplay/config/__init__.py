"""Configuration utilities for MiniDisplay."""

from pathlib import Path
from typing import Dict, Any, Optional

from .loader import (
    load_config,
    load_mock_data,
    get_default_config_path,
    DEFAULT_CONFIG_FILENAME,
    DEFAULT_MOCK_FILENAME,
)

__all__ = [
    "load_config",
    "load_mock_data",
    "get_default_config_path",
    "DEFAULT_CONFIG_FILENAME",
    "DEFAULT_MOCK_FILENAME",
]
