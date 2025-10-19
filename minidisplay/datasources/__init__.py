"""
Core data-source abstractions for MiniDisplay.

This package gathers the reusable interfaces and implementations used to
retrieve external information feeds for the project.
"""

from .base import DataSource
from .idelis import IdelisTransportSource
from .manager import DataSourceManager

__all__ = ["DataSource", "DataSourceManager", "IdelisTransportSource"]
