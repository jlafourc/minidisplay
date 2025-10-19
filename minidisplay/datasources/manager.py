"""
Data Source Manager

This module implements the DataSourceManager class that coordinates multiple
data sources and provides a unified interface for the main application.
"""

import time
from typing import Dict, List, Optional, Any
from nob import Nob

from .base import DataSource
from .idelis import IdelisTransportSource


class DataSourceManager:
    """
    Manager for coordinating multiple data sources.

    This class manages a collection of data sources, providing methods to
    initialize them, fetch data from available sources, and maintain
    compatibility with the existing application structure.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the data source manager.

        Args:
            config: Configuration dictionary containing data source configurations
        """
        self.config = config
        self.data_sources: Dict[str, DataSource] = {}
        self._last_fetch_time: Optional[float] = None
        self._last_successful_source: Optional[str] = None

    def initialize_data_sources(self) -> None:
        """
        Initialize all configured data sources.

        This method creates instances of all configured data sources.
        Currently starts with just the Idelis transport source to maintain
        compatibility with the existing system.
        """
        # Initialize Idelis transport source (maintains existing functionality)
        if "api_url" in self.config:
            idelis_source = IdelisTransportSource(self.config)
            self.data_sources["idelis"] = idelis_source
            print(f"Initialized data source: {idelis_source.name}")

    def get_data_source(self, name: str) -> Optional[DataSource]:
        """
        Get a specific data source by name.

        Args:
            name: The name of the data source to retrieve

        Returns:
            The requested data source, or None if not found
        """
        return self.data_sources.get(name)

    def get_available_sources(self) -> List[str]:
        """
        Get list of available data sources.

        Returns:
            List of data source names that are currently available
        """
        available = []
        for name, source in self.data_sources.items():
            if source.is_available():
                available.append(name)
        return available

    def fetch_from_source(self, source_name: str) -> Optional[Nob]:
        """
        Fetch data from a specific data source.

        Args:
            source_name: Name of the data source to fetch from

        Returns:
            Nob object containing fetched data, or None if fetching failed

        Note:
            This method maintains compatibility with the original fetch_arrival_data
            function behavior - it returns None on failure, following the same
            error handling pattern used throughout the codebase.
        """
        source = self.get_data_source(source_name)
        if not source:
            print(f"Data source '{source_name}' not found.")
            return None

        if not source.is_available():
            print(f"Data source '{source_name}' is not available.")
            return None

        data = source.fetch_data()
        if data:
            self._last_fetch_time = time.time()
            self._last_successful_source = source_name

        return data

    def fetch_primary_data(self) -> Optional[Nob]:
        """
        Fetch data from the primary data source.

        For now, this defaults to the Idelis source to maintain exact
        compatibility with the existing system behavior.

        Returns:
            Nob object containing fetched data, or None if fetching failed
        """
        # Default to Idelis source for compatibility
        return self.fetch_from_source("idelis")

    def get_status(self) -> Dict[str, Any]:
        """
        Get the status of all data sources.

        Returns:
            Dictionary containing status information for all data sources
        """
        status = {
            "total_sources": len(self.data_sources),
            "available_sources": self.get_available_sources(),
            "last_fetch_time": self._last_fetch_time,
            "last_successful_source": self._last_successful_source,
            "sources": {}
        }

        for name, source in self.data_sources.items():
            status["sources"][name] = {
                "name": source.name,
                "available": source.is_available(),
                "last_error": source.last_error,
                "last_fetch_time": source.last_fetch_time,
                "refresh_interval": source.get_refresh_interval()
            }

        return status

    def get_mock_data(self, source_name: str, mock_time) -> Optional[Nob]:
        """
        Get mock data from a specific source for testing.

        Args:
            source_name: Name of the data source
            mock_time: datetime object for mock data generation

        Returns:
            Nob object containing mock data, or None if not supported
        """
        source = self.get_data_source(source_name)
        if not source:
            return None

        # Currently only IdelisTransportSource supports mock data
        if hasattr(source, 'get_mock_data'):
            return source.get_mock_data(mock_time)

        return None

    def __len__(self) -> int:
        """Return the number of configured data sources."""
        return len(self.data_sources)

    def __str__(self) -> str:
        """String representation of the data source manager."""
        available_count = len(self.get_available_sources())
        return f"DataSourceManager({len(self.data_sources)} sources, {available_count} available)"

    def __repr__(self) -> str:
        """Detailed string representation of the data source manager."""
        return (f"DataSourceManager(total={len(self.data_sources)}, "
                f"available={len(self.get_available_sources())}, "
                f"last_fetch={self._last_fetch_time})")
